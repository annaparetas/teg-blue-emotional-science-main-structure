/* Preserve the reader's diagram context without assigning a Gradient Position. */
(() => {
  const box = document.querySelector('[data-evidence-context]');
  const params = new URLSearchParams(location.search);
  if (!box || params.get('from') !== 'evidence-connections') return;
  const signals = window.TEG_SIGNALS?.signals || {};
  const id = params.get('signal');
  const signal = Object.hasOwn(signals, id) ? signals[id] : null;
  const data = window.TEG_SIGNAL_EVIDENCE;
  const node = data?.nodes.find(n => n.id === params.get('node'));
  const returnPage = location.pathname.endsWith('/03-model-2-gradient/return.html');
  const base = returnPage ? '../01-signal-map/grounding/' : './';
  const url = new URL(base + 'evidence-connections.html', location.href);
  url.searchParams.set('reading', params.get('reading') === 'chronic' && signal?.chronic ? 'chronic' : 'fluid');
  if (signal) url.searchParams.set('signal', signal.id);
  if (node) url.hash = node.id;
  const p = document.createElement('p');
  p.textContent = signal
    ? 'Reading from the evidence map: ' + signal.name + '. The question concerns what changes in a particular episode. The emotion alone does not establish a Gradient Position.'
    : 'Reading from the working evidence map. Recovery and renewed usable capacities need to be examined separately.';
  box.append(p);
  if (node?.review?.return_question) {
    const question = document.createElement('p');
    question.textContent = 'Question about Return: ' + node.review.return_question;
    box.append(question);
  }
  if (returnPage && params.get('reading') === 'chronic') {
    const scope = document.createElement('p');
    scope.textContent = 'Your Chronic reading is saved for the trip back. This Return page currently examines the Fluid Gradient.';
    box.append(scope);
  }
  const a = document.createElement('a');
  a.href = url.href;
  a.textContent = '← Return to ' + (node?.label || signal?.name || 'the diagram') + ' in the evidence map';
  box.append(a);
  box.hidden = false;
})();
