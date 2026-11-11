function milliseconds(text) {
  const match = /^(\d{2}):([0-5]\d):([0-5]\d),(\d{3})$/.exec(text)
  if (!match) throw new TypeError('Invalid SRT timestamp')
  const [hours, minutes, seconds, ms] = match.slice(1).map(Number)
  return ((hours * 60 + minutes) * 60 + seconds) * 1000 + ms
}

export async function operation({ srt }, quality) {
  if (typeof srt !== 'string' || !srt.trim()) throw new TypeError('Expected SRT text')
  const cues = srt.trim().replace(/\r\n/g, '\n').split(/\n[ \t]*\n+/).map(block => {
    const [number, timing, ...lines] = block.split('\n')
    const times = timing?.trim().split(/\s+-->\s+/)
    if (!/^\d+$/.test(number) || times?.length !== 2 || !lines.length) throw new TypeError('Invalid SRT block')
    return { start: milliseconds(times[0]), end: milliseconds(times[1]), lines }
  })
  return quality({ cues })
}
