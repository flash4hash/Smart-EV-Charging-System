def uncontrolled_scheduler(evs):
    time = 0
    active = []
    completed = []
    schedule_uncontrolled = []

    while len(completed) < len(evs):
        for ev in evs:
            if ev["arrival"] == time:
                ev["start"] = time
                ev["end"] = time + ev["duration"]
                active.append(ev)

        for ev in active[:]:
            if ev["end"] == time:
                active.remove(ev)
                completed.append(ev)

        schedule_uncontrolled.append((time, len(active)))
        time += 1

    return schedule_uncontrolled