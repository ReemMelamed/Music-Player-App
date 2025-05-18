def format_time(seconds):
    if seconds is None or seconds < 0:
        return "0:00"
    m = int(seconds) // 60
    s = int(seconds) % 60
    return f"{m}:{s:02d}"