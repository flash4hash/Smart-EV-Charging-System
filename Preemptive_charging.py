evs = [
    {"id": "EV1", "arrival": 0, "duration": 6, "departure": 12},
    {"id": "EV2", "arrival": 1, "duration": 3, "departure": 5},   # urgent
    {"id": "EV3", "arrival": 2, "duration": 4, "departure": 6},   # urgent
    {"id": "EV4", "arrival": 3, "duration": 2, "departure": 15},
]

max_charging = 2
time = 0

waiting = []      # EVs that have arrived but not charging
charging = []     # EVs currently charging
completed = []    # EVs that finished

schedule_preemptive = []   # (time, number of EVs charging)

# Add remaining_time to each EV
for ev in evs:
    ev["remaining"] = ev["duration"]
    ev["start"] = None   # will be assigned when first charged

while len(completed) < len(evs):

    # Add newly arrived EVs to waiting list
    for ev in evs:
        if ev["arrival"] == time:
            waiting.append(ev)

    # Combine all candidates (waiting + currently charging)
    candidates = waiting + charging

    # Sort by urgency
    # Urgency = (departure - current time)
    candidates.sort(key=lambda x: x["departure"] - time)

    # Select top EVs to charge (PREEMPTIVE STEP)
    new_charging = candidates[:max_charging]

    # Update waiting list (others go to waiting)
    waiting = [ev for ev in candidates if ev not in new_charging]

    # Assign start time (only first time)
    for ev in new_charging:
        if ev["start"] is None:
            ev["start"] = time

    # Update charging list
    charging = new_charging

    # Reduce remaining charging time
    for ev in charging:
        ev["remaining"] -= 1

    # Remove completed EVs
    for ev in charging[:]:
        if ev["remaining"] == 0:
            ev["end"] = time + 1   # finished at end of this time step
            charging.remove(ev)
            completed.append(ev)

    # Record system load
    schedule_preemptive.append((time, len(charging)))

    print(f"Time {time} | Charging: {[ev['id'] for ev in charging]} | Waiting: {[ev['id'] for ev in waiting]}")
    time += 1

print("\nPreemptive Priority Scheduling Results:")
for ev in completed:
    print(f"{ev['id']}: Start={ev['start']}, End={ev['end']}, Departure={ev['departure']}")