(() => {
  const root = document.querySelector('#work .context-window');
  if (!root) return;

  const sections = [...root.querySelectorAll('section')].slice(0, 6);
  if (sections.length !== 6) return;

  const noteFields = [];
  for (const section of sections) {
    const heading = section.querySelector('h2');
    const question = section.querySelector('strong');
    if (!heading || !question) continue;

    const wrap = document.createElement('p');
    const label = document.createElement('label');
    const textarea = document.createElement('textarea');
    const id = 'work-note-' + noteFields.length;

    label.htmlFor = id;
    label.textContent = 'Your notes';
    label.style.display = 'block';
    label.style.fontWeight = '700';
    label.style.marginBottom = '.35rem';

    textarea.id = id;
    textarea.rows = 6;
    textarea.setAttribute('aria-label', 'Notes for ' + heading.textContent.trim());
    textarea.style.width = '100%';
    textarea.style.maxWidth = '70ch';
    textarea.style.padding = '.75rem';
    textarea.style.font = 'inherit';
    textarea.style.lineHeight = '1.5';
    textarea.style.background = 'var(--panel)';
    textarea.style.color = 'var(--foreground)';
    textarea.style.border = '1px solid var(--border)';

    wrap.append(label, textarea);
    section.append(wrap);
    noteFields.push({
      heading: heading.textContent.trim(),
      question: question.textContent.trim(),
      textarea,
    });
  }

  if (noteFields.length !== 6) return;

  const privacy = document.createElement('p');
  privacy.className = 'status';
  privacy.textContent = 'Optional local scratchpad: this page does not submit or save what you type. Copy your notes before leaving if you want to keep them.';
  root.insertBefore(privacy, sections[0]);

  const controls = document.createElement('div');
  controls.className = 'journey-exits';
  controls.setAttribute('aria-label', 'Local note controls');

  const copy = document.createElement('button');
  copy.type = 'button';
  copy.textContent = 'Copy notes as Markdown';

  const clear = document.createElement('button');
  clear.type = 'button';
  clear.textContent = 'Clear notes';

  for (const button of [copy, clear]) {
    button.style.font = 'inherit';
    button.style.padding = '.65rem 1rem';
    button.style.cursor = 'pointer';
  }

  const status = document.createElement('span');
  status.setAttribute('role', 'status');
  status.setAttribute('aria-live', 'polite');

  controls.append(copy, clear, status);
  const exits = root.querySelector('nav.journey-exits');
  root.insertBefore(controls, exits ?? null);

  const renderMarkdown = () => {
    const lines = ['# Work with a situation — notes', ''];
    for (const item of noteFields) {
      lines.push('## ' + item.heading, '', '**' + item.question + '**', '', item.textarea.value.trim(), '');
    }
    lines.push('Generated locally from Please Start From Here. Nothing was submitted to the site.', '');
    return lines.join('\n');
  };

  copy.addEventListener('click', async () => {
    try {
      await navigator.clipboard.writeText(renderMarkdown());
      status.textContent = 'Copied.';
    } catch {
      status.textContent = 'Copy was blocked by this browser. Select and copy the notes manually.';
    }
  });

  clear.addEventListener('click', () => {
    if (!noteFields.some(item => item.textarea.value)) {
      status.textContent = 'Nothing to clear.';
      return;
    }
    if (!window.confirm('Clear all six local note fields?')) return;
    for (const item of noteFields) item.textarea.value = '';
    status.textContent = 'Cleared.';
    noteFields[0].textarea.focus();
  });
})();
