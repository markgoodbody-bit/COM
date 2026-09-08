import {parentPort,workerData} from 'node:worker_threads';
import {SqliteAdapter} from '../src/sqlite-adapter.js';
import {Store} from '../src/store.js';
const db=new SqliteAdapter(workerData.path),store=new Store(db,()=>workerData.now);
const gate=new Int32Array(workerData.gate);parentPort.postMessage({ready:true});
Atomics.wait(gate,0,0);
try{const result=await store.submit(workerData.input,workerData.client);parentPort.postMessage({ok:true,id:result.id});}
catch(e){parentPort.postMessage({ok:false,code:e.code??e.message});}
finally{db.close();}
