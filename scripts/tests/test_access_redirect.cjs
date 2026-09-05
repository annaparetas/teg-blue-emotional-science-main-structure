// Exercise compatibility navigation as a pure script, without browser state.
const fs = require('node:fs');
const vm = require('node:vm');
const path = require('node:path');
const assert = require('node:assert/strict');
const code = fs.readFileSync(path.join(__dirname, '../../assets/access-redirect.js'), 'utf8');
function route(page, address, siteRoot) {
  let result;
  const url = new URL(address);
  const fallback = {};
  vm.runInNewContext(code, {
    URL, URLSearchParams,
    document: { baseURI:address, currentScript:{dataset:{accessPage:page,siteRoot}}, querySelector:()=>fallback },
    location:{hash:url.hash,search:url.search,replace:value=>{result=value;}}
  });
  return result;
}
const origin = 'http://example.test';
assert.equal(route('access',origin+'/02-model-1-ess-cls-me/access.html?bia=1&asa=2&mau=3#functional-sequence','../'),origin+'/04-model-3-esc/cycle.html?bia=1&asa=2&mau=3#operating-sequence');
assert.equal(route('access',origin+'/02-model-1-ess-cls-me/access.html#signal-organisation-completion','../'),origin+'/04-model-3-esc/shared-event-record.html#signal-organisation-completion');
assert.equal(route('gradient',origin+'/03-model-2-gradient/positions.html#chronic','../'),undefined);
assert.equal(route('gradient',origin+'/03-model-2-gradient/positions.html?bia=1&asa=0&mau=3&position=x&reading=fluid#me-mentalizing-access','../'),origin+'/02-model-1-ess-cls-me/me-access.html?bia=1&asa=0&mau=3&position=x&reading=fluid#mentalizing-access');
for (const n of ['000','001','010','011','100','101','110','111']) {
  assert.equal(route('configuration',origin+'/inner-compass-nervous-system-organization-gradient/models/01-information-systems/relational-capacities.html#config-'+n,'../../../teg-blue-emotional-science-main-structure/'),origin+'/teg-blue-emotional-science-main-structure/02-model-1-ess-cls-me/me-access.html#config-'+n);
}
assert.equal(route('configuration',origin+'/old.html#capacity-interoceptive','/'),origin+'/02-model-1-ess-cls-me/me-access.html#bodily-access');
assert.equal(route('access',origin+'/old.html#%E0%A4','/'),origin+'/02-model-1-ess-cls-me/me-access.html#coordinated-access');
assert.equal(route('sequence','file:///workspace/inner-compass-nervous-system-organization-gradient/models/01-information-systems/inner-compass-sequence.html','../../../teg-blue-emotional-science-main-structure/'),'file:///workspace/teg-blue-emotional-science-main-structure/04-model-3-esc/cycle.html#operating-sequence');
console.log('15 compatibility cases passed: owner, fragment, state, filesystem and ordinary Gradient routes.');
