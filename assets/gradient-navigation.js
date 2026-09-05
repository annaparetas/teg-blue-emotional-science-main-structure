(() => {
  const keys = ['x','a','ab','b','c','d','z'];
  const names = {x:'X',a:'A',ab:'A↔B',b:'B',c:'C',d:'D',z:'Z'};
  function sync() {
    const params = new URLSearchParams(location.search);
    const hash = location.hash.slice(1);
    const match = /^(fluid|chronic)-(?:.*-)?(x|a|ab|b|c|d|z)$/.exec(hash);
    let position = document.body.dataset.gradientPosition || params.get('position') || (match && match[2]);
    if (!keys.includes(position)) position = null;
    let reading = document.body.dataset.gradientReading || document.body.dataset.gradientMode || params.get('reading') || (match && match[1]);
    reading = reading === 'chronic' ? 'chronic' : 'fluid';
    document.querySelectorAll('[data-gradient-page]').forEach(link => {
      const page = link.dataset.gradientPage;
      const url = new URL(page, location.href);
      if (position) {
        url.searchParams.set('position',position);url.searchParams.set('reading',reading);
        if (page === 'positions.html') url.hash = `${reading}-position-${position}`;
        if (page === 'autonomic.html') url.hash = `${reading}-${position}`;
        if (page === 'return.html' && reading === 'fluid') url.hash = `return-position-${position}`;
      }
      link.href = url.href;
    });
    document.querySelectorAll('[data-gradient-return]').forEach(link => {
      link.hidden = !position || location.pathname.endsWith('/position.html');
      if (position) {
        link.href = `position.html?position=${position}&reading=${reading}`;
        link.textContent = `← Return to ${names[position]} · ${reading === 'chronic' ? 'Chronic' : 'Fluid'} position record`;
      }
    });
  }
  sync();
  addEventListener('hashchange',sync);addEventListener('gradientcontextchange',sync);addEventListener('popstate',sync);
  new MutationObserver(sync).observe(document.body,{attributes:true,attributeFilter:['data-gradient-mode']});
})();
