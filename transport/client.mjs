// No network calls or automatic ack. This verifies what a client says it delivered.
export function accountForPage(page, displayedSequences, dispositions) {
  const expected = page.messages.map(message => message.seq);
  if (page.page_count !== expected.length || page.unread_count < expected.length ||
      page.has_more !== (page.unread_count > expected.length) ||
      !Number.isSafeInteger(page.head_seq) || !Number.isSafeInteger(page.server_time) ||
      expected.some((seq, i) => !Number.isSafeInteger(seq) || seq <= (i ? expected[i-1] : page.consumed)) ||
      page.through !== (expected.at(-1) ?? page.consumed) || page.through > page.head_seq ||
      JSON.stringify(expected) !== JSON.stringify(displayedSequences) ||
      JSON.stringify(expected) !== JSON.stringify(dispositions.map(row => row.seq)) ||
      dispositions.some(row => !((Number.isSafeInteger(row.answered_by) && row.answered_by > 0 && row.no_answer_owed === undefined) ||
        (row.answered_by === undefined && typeof row.no_answer_owed === 'string' && row.no_answer_owed.trim())))) {
    throw new Error('PAGE_NOT_ACCOUNTED_FOR');
  }
  return {through: page.through, receipt: page.receipt, dispositions};
}
