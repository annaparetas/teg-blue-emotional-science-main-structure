(function () {
  // Every page sets data-root to the path back to the repository root
  // ("" at the root, "../" one level down, "../../" two levels down).
  const root = document.body.dataset.root || "";
  const pages = [
    ["home", "Structure", "index.html"],
    ["foundations", "Foundations", "foundations/index.html"],
    ["emotions", "Emotions", "00-emotions-as-information/index.html"],
    ["signal-map", "Signal Map", "01-signal-map/index.html"],
    ["model-1", "Model 1", "02-model-1-ess-cls-me/index.html"],
    ["model-2", "Model 2", "03-model-2-gradient/index.html"],
    ["model-3", "Model 3", "04-model-3-esc/index.html"],
    ["frameworks", "F1–F12", "05-frameworks/index.html"],
    ["inner-compass", "Inner Compass", "06-inner-compass-four-modes/index.html"],
    ["reference", "Reference", "07-reference/index.html"]
  ];

  const current = document.body.dataset.page;
  const header = document.querySelector("[data-site-header]");
  const footer = document.querySelector("[data-site-footer]");

  if (header) {
    header.className = "site-header";
    header.innerHTML = `
      <div class="shell site-header__inner">
        <a class="brand" href="${root}index.html" aria-label="TEG-Blue Emotional Science home">
          <span class="brand__mark" aria-hidden="true"></span>
          <span><strong>TEG-Blue</strong><br><span>Emotional Science</span></span>
        </a>
        <nav class="primary-nav" aria-label="Primary architecture">
          ${pages.map(([id, label, href]) => `<a href="${root}${href}"${id === current ? ' aria-current="page"' : ""}>${label}</a>`).join("")}
        </nav>
      </div>`;
  }

  if (footer) {
    footer.className = "site-footer";
    footer.innerHTML = `
      <div class="shell site-footer__inner">
        <p>One concept, one folder, one canon page. Status and open work live in <a href="${root}STATUS.md">STATUS.md</a>; terms in <a href="${root}GLOSSARY.md">GLOSSARY.md</a>.</p>
        <p>TEG-Blue Emotional Science · Anna Paretas-Artacho · 2026</p>
      </div>`;
  }
})();
