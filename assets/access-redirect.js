/* Compatibility only: current navigation links directly to the owning page. */
(function () {
  "use strict";
  var script = document.currentScript;
  var page = script.dataset.accessPage;
  var root = new URL(script.dataset.siteRoot, document.baseURI);
  var dials = "02-model-1-ess-cls-me/me-access.html";
  var hash = location.hash.slice(1);
  try { hash = decodeURIComponent(hash); } catch (_) { /* Keep an unreadable old fragment as-is. */ }
  var controls = {"me-participation-title": "capacity-key", "me-interoceptive-access": "bodily-access", "me-affective-sharing-access": "affective-sharing-access", "me-mentalizing-access": "mentalizing-access", "access-interoceptive": "bodily-access", "access-affective": "affective-sharing-access", "access-mentalizing": "mentalizing-access", "me-access-summary": "configuration", "me-access-reveal": "configuration"};
  var configAnchors = {
    "capacity-interoceptive": "bodily-access", "capacity-affective-sharing": "affective-sharing-access",
    "capacity-mentalizing": "mentalizing-access", "configuration-field": "field", "field-title": "field",
    "quality-title": "quality", "capacity-key-title": "capacity-key"
  };
  var path = dials, anchor = "coordinated-access";
  if (page === "gradient") {
    if (!Object.prototype.hasOwnProperty.call(controls, hash)) return;
    anchor = controls[hash];
  } else if (page === "sequence" || hash === "functional-sequence") {
    path = "04-model-3-esc/cycle.html"; anchor = "operating-sequence";
  } else if (hash === "signal-organisation-completion") {
    path = "04-model-3-esc/shared-event-record.html"; anchor = hash;
  } else if (page === "configuration") {
    anchor = ["capacity-key", "quality", "field", "configuration"].indexOf(hash) >= 0 ? hash : "field";
    if (/^config-[01]{3}$/.test(hash)) anchor = hash;
    if (Object.prototype.hasOwnProperty.call(configAnchors, hash)) anchor = configAnchors[hash];
  }
  var destination = new URL(path, root);
  var current = new URLSearchParams(location.search);
  ["bia", "asa", "mau", "position", "reading"].forEach(function (key) {
    if (current.has(key)) destination.searchParams.set(key, current.get(key));
  });
  destination.hash = anchor;
  var fallback = document.querySelector("[data-current-destination]");
  if (fallback) fallback.href = destination.href;
  location.replace(destination.href);
})();
