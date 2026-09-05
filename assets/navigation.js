(function () {
  // Every page sets data-root to the path back to the repository root
  // ("" at the root, "../" one level down, "../../" two levels down).
  const root = document.body.dataset.root || "";
  const pages = [
    ["home", "Structure", "index.html"],
    ["foundations", "Foundations", "foundations/index.html"],
    ["emotions", "Emotions", "00-emotions-as-information/index.html"],
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
  const model2Groups = [
    [
      ['Model overview', 'index.html'],
      ['Original Gradient table', 'positions.html'],
      ['Position records', 'position.html']
    ],
    [
      ['Governing premise', 'premise.html'],
      ['Fluid / Chronic', 'fluid-chronic.html'],
      ['Depth', 'depth.html'],
      ['Intermediate patterns', 'intermediate-layers.html'],
      ['Biological participation', 'autonomic.html'],
      ['Return and recovery', 'return.html']
    ]
  ];

  if (header) {
    header.className = "site-header";
    header.innerHTML = `
      <div class="shell site-header__inner">
        <a class="brand" href="${root}index.html" aria-label="TEG-Blue Emotional Science home">
          <span class="brand__mark" aria-hidden="true"></span>
          <span><strong>TEG-Blue</strong><br><span>Emotional Science</span></span>
        </a>
        <nav class="primary-nav" aria-label="Primary architecture">
          ${pages.map(([id, label, href]) => {
            if (id === 'emotions') return `<div class="primary-nav__dropdown">
              <button class="primary-nav__trigger" type="button" aria-expanded="false" aria-controls="emotions-navigation"${['emotions','signal-map'].includes(current) ? ' data-active="true"' : ''}>Emotions <span aria-hidden="true">▾</span></button>
              <div class="primary-nav__submenu" id="emotions-navigation" hidden>
                <a href="${root}00-emotions-as-information/index.html"${current === 'emotions' ? ' aria-current="page"' : ''}>Emotions as Information</a>
                <a href="${root}01-signal-map/index.html"${current === 'signal-map' ? ' aria-current="location"' : ''}>Signal Map</a>
              </div>
            </div>`;
            if (id === 'model-2') return `<div class="primary-nav__dropdown">
              <button class="primary-nav__trigger" type="button" aria-expanded="false" aria-controls="model-2-navigation"${current === 'model-2' ? ' data-active="true"' : ''}>Model 2 <span aria-hidden="true">▾</span></button>
              <div class="primary-nav__submenu" id="model-2-navigation" hidden>
                ${model2Groups.map(group => `<div class="primary-nav__submenu-group">${group.map(([title, page]) => {
                  const target = `${root}03-model-2-gradient/${page}`;
                  const selected = new URL(target, location.href).pathname === location.pathname;
                  return `<a href="${target}"${current === 'model-2' ? ` data-gradient-page="${page}"` : ''}${selected ? ' aria-current="page"' : ''}>${title}</a>`;
                }).join('')}</div>`).join('')}
              </div>
            </div>`;
            return `<a href="${root}${href}"${id === current ? ' aria-current="page"' : ''}>${label}</a>`;
          }).join("")}
        </nav>
      </div>`;
  }

  if (header) {
    const dropdowns = [...header.querySelectorAll('.primary-nav__dropdown')];
    function closeDropdown(dropdown) {
      dropdown.querySelector('.primary-nav__submenu').hidden = true;
      dropdown.querySelector('button').setAttribute('aria-expanded', 'false');
    }
    dropdowns.forEach(dropdown => {
      const trigger = dropdown.querySelector('button');
      const submenu = dropdown.querySelector('.primary-nav__submenu');
      function positionSubmenu() {
        if (submenu.hidden) return;
        submenu.style.left = '0px';
        const box = submenu.getBoundingClientRect();
        const shift = Math.min(0, window.innerWidth - 12 - box.right) + Math.max(0, 12 - box.left);
        submenu.style.left = `${shift}px`;
        submenu.style.maxHeight = `${Math.max(80, window.innerHeight - box.top - 12)}px`;
      }
      function close() { closeDropdown(dropdown); }
      function open() {
        dropdowns.forEach(other => { if (other !== dropdown) closeDropdown(other); });
        submenu.hidden = false;
        trigger.setAttribute('aria-expanded', 'true');
        positionSubmenu();
      }
      trigger.addEventListener('click', () => {
        if (submenu.hidden) open();
        else close();
      });
      dropdown.addEventListener('keydown', event => {
        if (event.key === 'Escape' && !submenu.hidden) { event.preventDefault(); close(); trigger.focus(); }
        if (event.key === 'ArrowDown' && event.target === trigger) { event.preventDefault(); open(); submenu.querySelector('a').focus(); }
      });
      dropdown.addEventListener('focusout', event => { if (!dropdown.contains(event.relatedTarget)) close(); });
      document.addEventListener('click', event => { if (!dropdown.contains(event.target)) close(); });
      submenu.addEventListener('click', event => { if (event.target.closest('a')) close(); });
      window.addEventListener('resize', positionSubmenu);
    });
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
