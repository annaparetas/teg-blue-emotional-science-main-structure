(() => {
  const currentReading = location.pathname.match(/\/emotion\/(fluid|chronic)\.html$/)?.[1];
  if (currentReading) {
    const syncSignal = () => {
      const signal = location.hash.startsWith('#signal-') ? location.hash.slice(8) : '';
      const row = signal && document.getElementById(`signal-${signal}`);
      document.querySelectorAll('.signal-depth a, .signal-reading-route').forEach(link => {
        const url = new URL(link.href);
        if (/\/emotion\/(fluid|chronic)\.html$/.test(url.pathname)) {
          // Body signals have no individual Chronic records.
          const bodySlugs = ['breathlessness', 'pain', 'overheating', 'cold', 'thirst', 'needing-to-urinate', 'needing-to-empty-the-bowels', 'hunger', 'tiredness'];
          url.hash = row && !(url.pathname.endsWith('/chronic.html') && bodySlugs.includes(signal)) ? `signal-${signal}` : '';
          link.href = url.href;
        } else if (url.pathname.endsWith('/grounding/neurochemistry.html')) {
          url.hash = row ? signal : '';
          link.href = url.href;
        }
      });
    };
    syncSignal();
    addEventListener('hashchange', syncSignal);
  }
  const reading = new URLSearchParams(location.search).get('reading');
  const isGrounding = location.pathname.endsWith('/grounding/neurochemistry.html');
  if (!isGrounding || !['fluid', 'chronic'].includes(reading)) return;
  // Derive return targets only from the page's own links, never from a supplied URL.
  function updateReturns() {
    const target = document.getElementById(location.hash.slice(1));
    const entry = target?.closest('.entry');
    const source = entry?.querySelector(`[data-reading="${reading}"]`);
    document.querySelectorAll('[data-reading-return]').forEach(link => {
      link.href = source?.getAttribute('href') || `../emotion/${reading}.html`;
      link.textContent = `← Return to ${entry ? entry.querySelector('h3').textContent + ' · ' : ''}${reading === 'fluid' ? 'Fluid' : 'Chronic'}`;
    });
    document.querySelectorAll('.signal-depth a').forEach(link => {
      if (new URL(link.href).pathname.endsWith(`/emotion/${reading}.html`) && source) link.href = source.href;
    });
    document.querySelectorAll(`[data-reading="${reading}"]`).forEach(link => link.setAttribute('aria-current', 'location'));
  }
  updateReturns();
  addEventListener('hashchange', updateReturns);
})();
