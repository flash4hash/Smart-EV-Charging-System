def basic_scheduler(evs, max_charging):
    time = 0
    charging = []
    waiting = []
    completed = []
    schedule = []

    while len(completed) < len(evs):
        for ev in evs:
            if ev["arrival"] == time:
                waiting.append(ev)

        for ev in charging[:]:
            if ev["end"] == time:
                charging.remove(ev)
                completed.append(ev)

        while len(charging) < max_charging and waiting:
            ev = waiting.pop(0)
            ev["start"] = time
            ev["end"] = time + ev["duration"]
            charging.append(ev)

        schedule.append((time, len(charging)))
        time += 1

    return schedule