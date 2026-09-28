"""Loopback-only disposable Campfire experiment. Standard library; no accounts."""
import argparse
import json
import secrets
import tempfile
import time
from http.server import BaseHTTPRequestHandler, HTTPServer
from pathlib import Path

from capsule import inspect_capsule, MAX_BYTES
from store import Store
from disclosure import TEXT, identifier

DISCLOSURE = TEXT


class App:
    def __init__(self, folder, clock=time.time):
        self.folder = Path(folder)
        self.path = self.folder / 'encounters.sqlite'
        self.clock = clock
        self.token = secrets.token_urlsafe(32)
        self.closed = False
        with self.store() as s:
            self.room = s.encounter(accepts=True, now=int(clock()), ttl=86400)

    def store(self):
        from contextlib import contextmanager

        @contextmanager
        def opened():
            s = Store(self.path, disclosure=identifier(DISCLOSURE))
            try:
                yield s
            finally:
                s.close()
        return opened()

    def dispatch(self, operation, data):
        if self.closed:
            raise ValueError('Room is closed')
        fields = {'accept': {'producer', 'disclosure', 'accepts'},
                  'read': {'acceptance'}, 'export': {'acceptance'},
                  'append': {'acceptance', 'request', 'body', 'relation', 'target', 'carry'},
                  'inspect': {'acceptance', 'capsule'}}
        if operation not in fields or not isinstance(data, dict) or set(data) != fields[operation]:
            raise ValueError('Unsupported request shape')
        now = int(self.clock())
        with self.store() as s:
            if operation == 'accept':
                return {'acceptance': s.accept(self.room, data['producer'],
                        disclosure=data['disclosure'], accepts=data['accepts'], now=now)}
            acceptance = data['acceptance']
            if not isinstance(acceptance, str):
                raise ValueError('Invalid acceptance')
            a = s.db.execute('SELECT * FROM acceptances WHERE id=? AND encounter=?',
                             (acceptance, self.room)).fetchone()
            if a is None:
                raise ValueError('Accept the disclosure before retrieving content')
            s._live(self.room, now)
            if operation == 'append':
                return {'id': s.append(self.room, data['request'], a['participant_claim'],
                        data['body'], now=now, acceptance=acceptance, carry=data['carry'],
                        relation=data['relation'], target=data['target'])}
            if operation == 'read':
                return {'entries': s.read(self.room, now=now), 'identity_verified': False}
            if operation == 'export':
                return {'capsule': s.export(self.room, now=now)}
            if not isinstance(data['capsule'], str):
                raise ValueError('Capsule must be text')
            return inspect_capsule(data['capsule'].encode('utf-8'))

    def dispose(self):
        # Only this App's exact disposable paths. No recursive deletion.
        self.closed = True
        for suffix in ('', '-wal', '-shm', '-journal'):
            target = Path(str(self.path) + suffix)
            if target.is_symlink():
                raise ValueError('Refusing to remove a symlink')
            target.unlink(missing_ok=True)


def make_server(app, port=0):
    class Handler(BaseHTTPRequestHandler):
        def setup(self):
            super().setup()
            self.connection.settimeout(3)

        def log_message(self, *args):
            pass  # Do not log bodies or query strings.

        def reply(self, status, body, kind='application/json'):
            raw = body.encode('utf-8') if isinstance(body, str) else json.dumps(body).encode('utf-8')
            self.send_response(status)
            self.send_header('Content-Type', kind + '; charset=utf-8')
            self.send_header('Content-Length', str(len(raw)))
            self.send_header('Cache-Control', 'no-store')
            self.send_header('X-Content-Type-Options', 'nosniff')
            self.send_header('Referrer-Policy', 'no-referrer')
            self.send_header('Content-Security-Policy', "default-src 'none'; script-src 'self'; style-src 'self'; connect-src 'self'; frame-ancestors 'none'; base-uri 'none'; form-action 'none'")
            self.end_headers()
            self.wfile.write(raw)

        def host_ok(self):
            expected = f'127.0.0.1:{self.server.server_port}'
            return self.headers.get_all('Host') == [expected]

        def do_GET(self):
            if not self.host_ok():
                return self.reply(403, {'error': 'Host rejected'})
            if self.path == '/api/disclosure':
                return self.reply(200, {'text': DISCLOSURE, 'id': identifier(DISCLOSURE)})
            asset = {'/': ('index.html', 'text/html'), '/app.js': ('app.js', 'text/javascript'),
                     '/style.css': ('style.css', 'text/css')}.get(self.path)
            if not asset:
                return self.reply(404, {'error': 'Not found'})
            body = (Path(__file__).parent / asset[0]).read_text(encoding='utf-8')
            if self.path == '/':
                body = body.replace('TOKEN_PLACEHOLDER', app.token).replace('DISCLOSURE_PLACEHOLDER', DISCLOSURE)
                body = body.replace('DISCLOSURE_ID_PLACEHOLDER', identifier(DISCLOSURE))
            self.reply(200, body, asset[1])

        def do_POST(self):
            origin = f'http://127.0.0.1:{self.server.server_port}'
            if (not self.host_ok() or self.headers.get_all('Origin') != [origin]
                    or self.headers.get_all('X-Campfire-Token') != [app.token]):
                return self.reply(403, {'error': 'Host, origin or local session token rejected'})
            if (self.headers.get('Content-Type') != 'application/json'
                    or self.headers.get('Transfer-Encoding') is not None
                    or len(self.headers.get_all('Content-Length') or []) != 1):
                return self.reply(400, {'error': 'Expected bounded JSON request'})
            try:
                size = int(self.headers['Content-Length'])
                if not 0 < size <= MAX_BYTES:
                    return self.reply(413, {'error': 'Request too large or empty'})
                self.connection.settimeout(3)
                from capsule import _object
                data = json.loads(self.rfile.read(size).decode('utf-8'), object_pairs_hook=_object)
                result = app.dispatch(self.path.removeprefix('/api/'), data) if self.path.startswith('/api/') else None
                if result is None:
                    return self.reply(404, {'error': 'Not found'})
                self.reply(200, result)
            except (ValueError, TypeError, RecursionError, TimeoutError):
                self.reply(400, {'error': 'Request rejected: check consent, expiry, fields, targets and carry permissions'})

    return HTTPServer(('127.0.0.1', port), Handler)


def main():
    parser = argparse.ArgumentParser()
    parser.add_argument('--port', type=int, default=8876)
    args = parser.parse_args()
    # A generated local temporary directory, never the repo or a synced store.
    with tempfile.TemporaryDirectory(prefix='campfire-disposable-') as folder:
        app = App(folder)
        server = make_server(app, args.port)
        print(f'Campfire experimental room: http://127.0.0.1:{server.server_port}/', flush=True)
        print('Synthetic/public text only. Ctrl+C closes the disposable room.', flush=True)
        try:
            server.serve_forever()
        except KeyboardInterrupt:
            pass
        finally:
            server.server_close()
            app.dispose()


if __name__ == '__main__':
    main()
