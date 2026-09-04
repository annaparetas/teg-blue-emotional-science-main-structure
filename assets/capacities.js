/* TEG-Blue · shared state for the three ME access capacities.
 *
 * Model 1 owns the controls (02-model-1-ess-cls-me/me-access.html, the add-on).
 * The Inner Compass reads the same state; Model 2 pages only echo it.
 * The state lives in the viewer's browser only (localStorage) and can be
 * carried in a link as ?bia=3&asa=1&mau=2 (bands 0–3). It never leaves
 * the browser and never describes another person. */
(function () {
  var KEY = "teg.capacities.v1";
  var KEYS = ["bodily", "affective", "mentalizing"];
  var PARAMS = { bodily: "bia", affective: "asa", mentalizing: "mau" };
  var NAMES = {
    bodily: "Bodily information access and use",
    affective: "Affective-sharing access",
    mentalizing: "Mentalizing access and use"
  };
  var SHORT = { bodily: "Feel myself", affective: "Feel another", mentalizing: "Read and revise another" };
  var BANDS = [
    "Not reliably available to ME",
    "Fragments may become readable",
    "Partly available and usable",
    "Broadly available to ME"
  ];
  var CONFIGS = {
    "000": "Relational unavailability",
    "001": "The mentalizing-only configuration",
    "010": "The absorbed-other configuration",
    "011": "The other-centred configuration",
    "100": "The self-contained configuration",
    "101": "The interoceptive–mentalizing configuration",
    "110": "The shared-affect configuration",
    "111": "The integrated configuration"
  };
  var DEFAULT = { bodily: 3, affective: 3, mentalizing: 3 };
  var listeners = [];

  function clamp(n) { n = Number(n); return isFinite(n) ? Math.max(0, Math.min(3, Math.round(n))) : null; }

  function fromStorage() {
    try {
      var raw = localStorage.getItem(KEY);
      if (!raw) return null;
      var obj = JSON.parse(raw), out = {};
      KEYS.forEach(function (k) { var v = clamp(obj[k]); out[k] = v === null ? DEFAULT[k] : v; });
      return out;
    } catch (e) { return null; }
  }

  function fromUrl() {
    var q = new URLSearchParams(location.search), out = null;
    KEYS.forEach(function (k) {
      if (q.has(PARAMS[k])) { var v = clamp(q.get(PARAMS[k])); if (v !== null) { out = out || {}; out[k] = v; } }
    });
    return out;
  }

  function get() {
    var state = fromStorage() || Object.assign({}, DEFAULT);
    var url = fromUrl();
    if (url) { Object.assign(state, url); persist(state); }
    return state;
  }

  function persist(state) { try { localStorage.setItem(KEY, JSON.stringify(state)); } catch (e) {} }

  function set(partial) {
    var state = get();
    Object.keys(partial || {}).forEach(function (k) { if (KEYS.indexOf(k) > -1) { var v = clamp(partial[k]); if (v !== null) state[k] = v; } });
    persist(state);
    listeners.forEach(function (fn) { fn(state); });
    return state;
  }

  function reset() { return set(Object.assign({}, DEFAULT)); }

  function code(state) { state = state || get(); return KEYS.map(function (k) { return state[k] >= 2 ? "1" : "0"; }).join(""); }

  function link(href, state) {
    state = state || get();
    var join = href.indexOf("?") > -1 ? "&" : "?";
    return href + join + KEYS.map(function (k) { return PARAMS[k] + "=" + state[k]; }).join("&");
  }

  function subscribe(fn) { listeners.push(fn); return function () { listeners = listeners.filter(function (f) { return f !== fn; }); }; }

  window.TEG = window.TEG || {};
  window.TEG.capacities = {
    KEYS: KEYS, PARAMS: PARAMS, NAMES: NAMES, SHORT: SHORT, BANDS: BANDS, CONFIGS: CONFIGS, DEFAULT: DEFAULT,
    get: get, set: set, reset: reset, code: code, link: link, subscribe: subscribe
  };
})();
