(() => {
  const signals = window.TEG_SIGNALS?.signals || {};
  const readingPage = location.pathname.match(/\/emotion\/(fluid|chronic)\.html$/)?.[1];
  const isRecords = location.pathname.endsWith('/01-signal-map/map.html');
  const isBiology = location.pathname.endsWith('/grounding/neurochemistry.html');
  const links = [...document.querySelectorAll('[data-signal-target], [data-signal-return], .signal-reading-route')];
  const bases = new Map(links.map(link => [link, link.href]));

  function context() {
    const params = new URLSearchParams(location.search);
    let hash = '';
    try { hash = decodeURIComponent(location.hash.slice(1)); } catch (_) {}
    const entry = isBiology ? document.getElementById(hash)?.closest('.entry') : null;
    // Read identifiers from the generated registry; query values never become arbitrary routes.
    const candidate = isRecords ? document.body.dataset.signalId
      : entry?.id || (readingPage && hash.startsWith('signal-') ? hash.slice(7) : params.get('signal'));
    const signal = Object.hasOwn(signals, candidate) ? signals[candidate] : null;
    let reading = readingPage || (isRecords && document.body.dataset.signalReading) || params.get('reading');
    if (reading !== 'chronic' || (signal && !signal.chronic)) reading = 'fluid';
    return { signal, reading, entry };
  }

  function sync() {
    const { signal, reading, entry } = context();
    links.forEach(link => {
      const url = new URL(bases.get(link));
      const target = link.dataset.signalTarget || (link.hasAttribute('data-signal-return') ? 'records'
        : url.pathname.endsWith('/chronic.html') ? 'chronic' : 'fluid');
      if (['fluid', 'chronic'].includes(target)) {
        url.searchParams.set('reading', target);
        if (signal) {
          url.searchParams.set('signal', signal.id);
          url.hash = target === 'chronic' && !signal.chronic ? 'top' : `signal-${signal.id}`;
        }
      } else {
        url.searchParams.set('reading', reading);
        if (signal) {
          if (target === 'records' || target === 'biology') url.hash = signal.id;
          else {
            url.searchParams.set('signal', signal.id);
            if (target === 'families') url.hash = `family-meaning-${signal.family}`;
          }
        }
      }
      link.href = url.href;
      if (link.dataset.signalTarget === 'chronic') link.textContent = signal && !signal.chronic ? 'Chronic overview' : 'Chronic';
      if (link.hasAttribute('data-signal-return')) {
        link.hidden = !signal || isRecords;
        if (signal) link.textContent = `← Return to ${signal.name} · ${reading === 'chronic' ? 'Chronic' : 'Fluid'} signal record`;
      }
    });

    // Keep the biology page's existing links back to the source roster.
    if (isBiology) {
      const source = entry?.querySelector(`[data-reading="${reading}"]`);
      document.querySelectorAll('[data-reading-return]').forEach(link => {
        link.href = source?.getAttribute('href') || `../emotion/${reading}.html`;
        link.textContent = `← Return to ${entry ? entry.querySelector('h3').textContent + ' · ' : ''}${reading === 'chronic' ? 'Chronic' : 'Fluid'}`;
      });
      document.querySelectorAll('[data-reading]').forEach(link => {
        if (link.dataset.reading === reading) link.setAttribute('aria-current', 'location');
        else link.removeAttribute('aria-current');
      });
    }
  }
  sync();
  addEventListener('hashchange', sync);
  addEventListener('signalcontextchange', sync);
})();
