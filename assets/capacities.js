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
  var READINGS = {
    bodily: [
      "Own feeling, need, limit and preference are not reliably readable. The body keeps regulating even when ME cannot use much of its information.",
      "Fragments reach ME, such as tension, unease or urgency, without a clear reading of what they are about.",
      "Much of one's own state is readable and partly usable, though quieter needs and limits may still be missed.",
      "Own bodily and emotional information is broadly readable, differentiated and usable, including limits and needs."
    ],
    affective: [
      "Another person's feeling is not reliably readable as affective resonance. ME may still detect or understand it in other ways.",
      "Brief or unclear fragments of another person's feeling reach ME, but the resonance is difficult to recognise or use while self and other stay distinct.",
      "Another person's feeling resonates and is partly usable while self and other mostly stay distinct.",
      "Another person's feeling can resonate broadly while self and other remain distinct."
    ],
    mentalizing: [
      "Another mind is not reliably represented. Their behaviour, movement or demand may be present without a usable understanding of their perspective.",
      "Another person's perspective is guessed in fragments, or fixed in advance, without being checked reliably.",
      "Another person's perspective can be represented and partly revised as new information arrives.",
      "Another person's perspective, intention and feeling can be represented broadly and revised through new information."
    ]
  };
  var CONFIGS = {
    "000": "All three in the lower bands",
    "001": "Mentalizing in an upper band",
    "010": "Affective sharing in an upper band",
    "011": "Affective sharing and mentalizing in the upper bands",
    "100": "Bodily information in an upper band",
    "101": "Bodily information and mentalizing in the upper bands",
    "110": "Bodily information and affective sharing in the upper bands",
    "111": "All three in the upper bands"
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
    KEYS: KEYS, PARAMS: PARAMS, NAMES: NAMES, SHORT: SHORT, BANDS: BANDS, READINGS: READINGS, CONFIGS: CONFIGS, DEFAULT: DEFAULT,
    get: get, set: set, reset: reset, code: code, link: link, subscribe: subscribe
  };
})();
