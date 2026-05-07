evs = [
    {"id": "EV1", "arrival": 0, "duration": 6, "departure": 12},
    {"id": "EV2", "arrival": 1, "duration": 3, "departure": 5},   
    {"id": "EV3", "arrival": 2, "duration": 4, "departure": 6},   
    {"id": "EV4", "arrival": 3, "duration": 2, "departure": 15},
]

max_charging = 2
time = 0

charging = []   # currently charging EVs
waiting = []    # queue
completed = []

schedule_priority = []   # (time, number of EVs charging)

while len(completed) < len(evs):
    
    # Add arriving EVs to waiting queue
    for ev in evs:
        if ev["arrival"] == time:
            waiting.append(ev)

    # Remove completed EVs
    for ev in charging[:]:
        if ev["end"] == time:
            charging.remove(ev)
            completed.append(ev)

    # Compute urgency dynamically
    waiting.sort(key=lambda x: x["departure"] - time)
    
    while len(charging) < max_charging and waiting:
        ev = waiting.pop(0)
        ev["start"] = time
        ev["end"] = time + ev["duration"]
        charging.append(ev)

    # Record load
    schedule_priority.append((time, len(charging)))

    print(f"Time {time} | Charging: {[ev['id'] for ev in charging]} | Waiting sorted: {[ev['id'] for ev in waiting]}")
    time += 1

# Print results
print("\nPriority Scheduling:")
for ev in completed:
    print(f"{ev['id']}: Start={ev['start']}, End={ev['end']}, Departure={ev['departure']}")