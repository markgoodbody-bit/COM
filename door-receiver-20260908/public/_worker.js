// Pages advanced-mode entry. All non-loopback requests are refused by design.
// For local Wrangler/D1 verification only; removal of that guard requires review.
import {handle} from '../src/handler.js';
export default {fetch(request,env){return handle(request,env);}};
