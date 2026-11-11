def operation(data, _):
    cues = data["cues"]
    if not isinstance(cues, list):
        raise ValueError("Expected cues array")
    for cue in cues:
        start, end, lines = cue["start"], cue["end"], cue["lines"]
        if (type(start) is not int or type(end) is not int or not 0 <= start < end
                or not isinstance(lines, list) or not lines or any(not isinstance(line, str) for line in lines)):
            raise ValueError("Invalid cue")
    diagnostics, latest_end = [], 0
    overlaps, fast, long_lines = 0, 0, 0
    for index, cue in sorted(enumerate(cues, 1), key=lambda pair: pair[1]["start"]):
        start, end, lines = cue["start"], cue["end"], cue["lines"]
        rate = sum(map(len, lines)) * 1000 / (end - start)
        overlap = start < latest_end
        too_long = sum(len(line) > 42 for line in lines)
        latest_end = max(latest_end, end)
        overlaps += overlap
        fast += rate > 20
        long_lines += too_long
        diagnostics.append({"cue": index, "charactersPerSecond": round(rate, 1),
                            "overlap": overlap, "longLines": too_long})
    return {"cues": len(cues), "overlaps": overlaps, "fastCues": fast,
            "longLines": long_lines, "diagnostics": diagnostics}
