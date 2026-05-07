def scheduler_step(evs, time, charging, waiting, max_charging, peak_range):
    for ev in evs:
        if ev["arrival"] == time:
            waiting.append(ev)
    
    candidates = waiting + charging
    candidates.sort(key=lambda x: x["departure"] - time)
    
    filtered = []

    for ev in candidates:
        urgency = ev["departure"] - time
        if time in peak_range:
            if urgency <= ev["remaining"]:
                filtered.append(ev)
        else:
            filtered.append(ev)

    if not filtered:
        filtered = candidates

    new_charging = filtered[:max_charging]
    new_waiting = [ev for ev in candidates if ev not in new_charging]

    for ev in new_charging:
        if ev["start"] is None:
            ev["start"] = time

    return new_charging, new_waiting

def smart_scheduler(evs, max_charging, peak_hours):
    for ev in evs:
        ev["remaining"] = ev["duration"]
        ev["start"] = None

    time = 0
    charging = []
    waiting = []
    completed = []
    schedule_smart = []

    while len(completed) < len(evs):
        charging, waiting = scheduler_step(evs, time, charging, waiting, max_charging, peak_hours)

        for ev in charging:
            ev["remaining"] -= 1

        for ev in charging[:]:
            if ev["remaining"] == 0:
                ev["end"] = time + 1
                charging.remove(ev)
                completed.append(ev)

        schedule_smart.append((time, len(charging)))
        time += 1

    return schedule_smart