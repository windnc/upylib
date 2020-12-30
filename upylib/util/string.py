def substr(s, start, end, contain_patt=True):
    start_pos = s.find(start)
    if start_pos < 0:
        return None, None, None

    end_pos = s.find(end, start_pos+len(start))
    if end_pos < 0:
        return None, None, None

    if contain_patt:
        return s[0:start_pos], s[start_pos:end_pos+len(end)], s[end_pos+len(end):]
    else:
        return s[0:start_pos], s[start_pos+len(start):end_pos], s[end_pos+len(end):]