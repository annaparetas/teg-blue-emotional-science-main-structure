(function () {
  const pages = [
    ["home", "Structure", "index.html"],
    ["emotions", "Emotions", "emotions-as-information.html"],
    ["model-1", "Model 1", "model-1-two-biological-information-systems-and-me.html"],
    ["model-2", "Model 2", "model-2-nervous-system-organisation-gradient.html"],
    ["model-3", "Model 3", "model-3-emotional-somatic-cycle.html"],
    ["frameworks", "F1–F12", "twelve-frameworks-map.html"],
    ["inner-compass", "Inner Compass", "inner-compass-four-mode-gradient.html"]
  ];

  const current = document.body.dataset.page;
  const header = document.querySelector("[data-site-header]");
  const footer = document.querySelector("[data-site-footer]");

  if (header) {
    header.className = "site-header";
    header.innerHTML = `
      <div class="shell site-header__inner">
        <a class="brand" href="index.html" aria-label="TEG-Blue Emotional Science Architecture home">
          <span class="brand__mark" aria-hidden="true"></span>
          <span><strong>TEG-Blue</strong><br><span>Emotional Science Architecture</span></span>
        </a>
        <nav class="primary-nav" aria-label="Primary architecture">
          ${pages.map(([id, label, href]) => `<a href="${href}"${id === current ? ' aria-current="page"' : ""}>${label}</a>`).join("")}
        </nav>
      </div>`;
  }

  if (footer) {
    footer.className = "site-footer";
    footer.innerHTML = `
      <div class="shell site-footer__inner">
        <p>Approved synthesis is transferred here from the TEG-Blue development repository.</p>
        <p>Living architecture · Anna Paretas-Artacho · 2026</p>
      </div>`;
  }
})();
