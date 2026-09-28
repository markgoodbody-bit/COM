"""Single disclosure source; its digest identifies text, not comprehension."""
import hashlib

TEXT = ('Shared experimental room. Use synthetic or already-public material only. '
        'The host and other processes under this Windows user can inspect or alter it. '
        'Retrieval may send content to your model provider. Names and acceptance handles '
        'are not verified identities. Carry choices control whole-thread export only. '
        'Access expires within 24 hours; expiry is not deletion. Normal shutdown deletes '
        'this room\'s database files. It does not delete exported copies, does not securely '
        'erase the disk, and a crash can leave the files behind.')


def identifier(text):
    return hashlib.sha256(text.encode('utf-8')).hexdigest()
