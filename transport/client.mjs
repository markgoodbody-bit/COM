// No network calls or automatic ack. This verifies what a client says it delivered.
export function accountForPage(page, displayedSequences, dispositions) {
  const expected = page.messages.map(message => message.seq);
  if (!/^[a-f0-9]{32}$/.test(page.epoch??'') || page.page_count !== expected.length || page.unread_count < expected.length ||
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
  // Caller must bind the POST's X-COM-Epoch to this observed page epoch.
  return {epoch:page.epoch,through: page.through, receipt: page.receipt, dispositions};
}
