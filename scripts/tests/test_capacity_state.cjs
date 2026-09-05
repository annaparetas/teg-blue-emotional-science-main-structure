// Incoming bookmark values must not undo subsequent independent edits.
const fs = require('node:fs');
const vm = require('node:vm');
const path = require('node:path');
const assert = require('node:assert/strict');
let address = new URL('http://example.test/me-access.html?bia=1&asa=2&mau=3&position=x#affective-sharing-access');
let stored;
const window = {};
vm.runInNewContext(fs.readFileSync(path.join(__dirname,'../../assets/capacities.js'),'utf8'), {
  window,URL,URLSearchParams,
  location:{get search(){return address.search;},get href(){return address.href;}},
  localStorage:{getItem:()=>stored,setItem:(_,v)=>{stored=v;}},
  history:{replaceState:(_,__,url)=>{address=new URL(url);}}
});
const C=window.TEG.capacities;
assert.equal(C.code(C.get()),'011');
C.set({bodily:0});
C.set({affective:0});
assert.deepEqual(JSON.parse(JSON.stringify(C.get())),{bodily:0,affective:0,mentalizing:3});
assert.equal(address.searchParams.get('bia'),'0');
assert.equal(address.searchParams.get('position'),'x');
assert.equal(address.hash,'#affective-sharing-access');
assert.equal(C.code(C.reset()),'111');
console.log('Incoming URL, sequential edits, bookmark context and reset preserve shared settings.');
