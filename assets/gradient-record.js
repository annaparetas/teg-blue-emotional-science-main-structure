(() => {
  'use strict';
  const data = window.TEG_GRADIENT;
  const escape = value => String(value ?? '').replace(/[&<>"']/g, c => ({'&':'&amp;','<':'&lt;','>':'&gt;','"':'&quot;',"'":'&#39;'}[c]));
  const params = new URLSearchParams(location.search);
  let position = data.positions.includes(params.get('position')) ? params.get('position') : 'x';
  let reading = params.get('reading') === 'chronic' ? 'chronic' : 'fluid';
  const article = document.getElementById('position-record');
  const href = path => `${path}?position=${position}&reading=${reading}`;
  function render() {
    document.body.dataset.gradientPosition = position;
    document.body.dataset.gradientReading = reading;
    const expanded = new Set([...article.querySelectorAll('details[open]')].map(el => el.id));
    const item = data.records[position], record = item.readings[reading];
    document.querySelectorAll('[data-position]').forEach(a => {
      a.href = `position.html?position=${a.dataset.position}&reading=${reading}`;
      if (a.dataset.position === position) a.setAttribute('aria-current','page'); else a.removeAttribute('aria-current');
    });
    document.querySelectorAll('button[data-reading]').forEach(b => b.setAttribute('aria-pressed', String(b.dataset.reading === reading)));
    article.innerHTML = `<h2 id="record-title">${escape(item.position)} · ${escape(record.name)}</h2>
      <p class="position-note">Working position description. Position names and reading rules retain their existing approval status. These records bring source explanations together; they do not assign a person an emotion, behaviour, diagnosis or level of conscious access.</p>
      <p class="position-summary">${escape(record.summary?.text || record.biology.fields['Functional autonomic task'])}</p>
      <nav class="position-sources" aria-label="Go deeper or return to the original table">
        <a href="${record.source}">Original Gradient table · ${escape(item.position)} · ${reading}</a>
        <a href="${href('fluid-chronic.html')}">What Fluid and Chronic mean</a>
        <a href="${href('depth.html')}">Depth and intermediate patterns</a>
        <a href="${href('autonomic.html')}#${reading}-${position}">Biological participation</a>
        <a href="${href('return.html')}${reading === 'fluid' ? '#return-position-' + position : ''}">Return and recovery</a>
      </nav>
      <h2>Sixteen questions for this position</h2>
      <p class="position-note">Questions come from the <a href="premise.html#lenses">governing premise</a>. Each answer keeps its source and its limits. Several bodily systems share an initial description; separate accounts remain open.</p>
      <div class="position-lenses">${record.lenses.map((lens,i) => `<details class="position-lens" id="lens-${i+1}"${expanded.has(`lens-${i+1}`) || (!expanded.size && i === 0) ? ' open' : ''}>
        <summary><strong>${escape(lens.title)}</strong><span>${escape(lens.question)}</span></summary>
        <div><p class="position-note">${escape(lens.note)}</p>${lens.fragments.map(f => `<h3>${escape(f.label)}</h3><p>${escape(f.text)}</p><a href="${escape(f.source)}">Read the exact source</a>`).join('')}</div></details>`).join('')}</div>
      <section class="position-evidence"><h2>Evidence and open work</h2><p>${escape(record.biology.status)}</p><p>${escape(record.grounding.text)}</p><p><a href="${record.grounding.source}">Read the table’s grounding</a> · <a href="grounding.md">Model 2 evidence status</a></p><p class="position-note">Return conditions in the autonomic entries are working descriptions. The Return workbench has incomplete Fluid fields and no completed Chronic route matrix. Do not treat missing fields as completed evidence.</p></section>`;
    const target = /^#lens-\d+$/.test(location.hash) && document.getElementById(location.hash.slice(1));
    if (target) target.open = true;
    document.title = `${item.position} · ${record.name} · Nervous System Gradient`;
    dispatchEvent(new Event('gradientcontextchange'));
  }
  document.querySelectorAll('button[data-reading]').forEach(button => button.addEventListener('click', () => {
    reading = button.dataset.reading;
    history.replaceState(null, '', `?position=${position}&reading=${reading}${location.hash}`);
    render();
  }));
  addEventListener('popstate', () => {
    const p = new URLSearchParams(location.search);
    position = data.positions.includes(p.get('position')) ? p.get('position') : 'x';
    reading = p.get('reading') === 'chronic' ? 'chronic' : 'fluid'; render();
  });
  render();
})();
