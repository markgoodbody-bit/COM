/** Disk-backed local test adapter. This is NOT evidence that remote D1 was exercised. */
import { DatabaseSync } from 'node:sqlite';
import { readFileSync } from 'node:fs';
export class SqliteAdapter {
  constructor(path) {
    this.sql=new DatabaseSync(path,{timeout:5000});
    this.sql.exec('PRAGMA foreign_keys=ON; PRAGMA journal_mode=WAL; PRAGMA synchronous=FULL;');
    const exists=this.sql.prepare("SELECT name FROM sqlite_master WHERE type='table' AND name='service'").get();
    if(!exists) this.sql.exec(readFileSync(new URL('../migrations/0001.sql',import.meta.url),'utf8'));
    const corrections=this.sql.prepare("SELECT name FROM sqlite_master WHERE type='table' AND name='correction_requests'").get();
    if(!corrections) this.sql.exec(readFileSync(new URL('../migrations/0002_correction_requests.sql',import.meta.url),'utf8'));
  }
  prepare(sql) {
    const db=this, make=(args=[])=>({
      bind(...values){return make(values);},
      execute(){
        const stmt=db.sql.prepare(sql);
        const results=stmt.columns().length?stmt.all(...args):[];
        let changes;
        if(stmt.columns().length) changes=db.sql.prepare('SELECT changes() AS n').get().n;
        else changes=stmt.run(...args).changes;
        return {success:true,results,meta:{changes:Number(changes)}};
      },
      async first(){return this.execute().results[0]??null;},
      async all(){return this.execute();},
      async run(){return this.execute();}
    });
    return make();
  }
  async batch(statements) {
    this.sql.exec('BEGIN IMMEDIATE');
    try { const result=statements.map(s=>s.execute()); this.sql.exec('COMMIT'); return result; }
    catch(e){this.sql.exec('ROLLBACK');throw e;}
  }
  close(){this.sql.close();}
}
