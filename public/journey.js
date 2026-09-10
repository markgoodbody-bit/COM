/* Optional navigation only. Native fragment links and CSS remain the fallback.
   Browser history holds page positions, not an answer log or a visitor profile. */
(() => {
  const windowElement = document.querySelector('.context-window');
  if (!windowElement) return;
  const back = windowElement.querySelector('[data-journey-back]');
  const reference = document.getElementById('full-introduction');
  function target(hash = location.hash) {
    try { return document.getElementById(decodeURIComponent(hash.slice(1))); }
    catch { return null; }
  }
  function step(hash) { return target(hash)?.closest('[data-step]'); }
  function revealReference(element) {
    for (let parent = element?.parentElement; parent; parent = parent.parentElement) {
      if (parent.tagName === 'DETAILS') parent.open = true;
    }
  }
  function update(moveFocus = false) {
    const destination = target();
    revealReference(destination);
    const active = step(location.hash) || document.getElementById('step-welcome');
    windowElement.setAttribute('data-enhanced', '');
    for (const panel of windowElement.querySelectorAll('[data-step]')) panel.hidden = panel !== active;
    const previous = history.state?.psfhJourney?.previous;
    back.href = previous || '#top';
    back.textContent = previous ? 'Back' : 'Back to the painting';
    if (!moveFocus) return;
    const heading = step(location.hash)?.querySelector('h2') || destination || (!location.hash && document.querySelector('#step-welcome h2'));
    if (!heading) return;
    if (!heading.hasAttribute('tabindex')) heading.setAttribute('tabindex', '-1');
    heading.focus({ preventScroll: true });
    (step(location.hash) || (!location.hash && document.querySelector('#step-welcome')) || heading).scrollIntoView({ block: 'start' });
  }
  // Without this enhancement the full introduction remains expanded.
  reference.open = !!target()?.closest('#full-introduction');
  document.addEventListener('click', event => {
    if (event.defaultPrevented || event.button !== 0 || event.metaKey || event.ctrlKey || event.shiftKey || event.altKey) return;
    const link = event.target.closest('a[href]');
    if (!link || link.target || link.hasAttribute('download')) return;
    if (link === back && history.state?.psfhJourney?.previous) {
      event.preventDefault();
      history.back();
      return;
    }
    const href = link.getAttribute('href');
    if (!href.startsWith('#')) return;
    revealReference(target(href));
    if (!step(href)) return;
    event.preventDefault();
    if (location.hash !== href) {
      history.pushState({ psfhJourney: { previous: location.hash || '#step-welcome' } }, '', href);
    }
    update(true);
  });
  window.addEventListener('popstate', () => update(true));
  window.addEventListener('hashchange', () => update(true));
  window.addEventListener('pageshow', () => update(false));
  update(false);
})();
