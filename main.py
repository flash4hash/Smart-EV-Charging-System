import copy
import matplotlib.pyplot as plt

# Import all scheduling strategies
from Uncontrolled_charging import uncontrolled_scheduler
from Simple_scheduler import basic_scheduler
from Smart_scheduler import smart_scheduler

# EV dataset
evs = [
    {"id": "EV1", "arrival": 0, "duration": 6, "departure": 12},
    {"id": "EV2", "arrival": 1, "duration": 3, "departure": 5},
    {"id": "EV3", "arrival": 2, "duration": 4, "departure": 6},
    {"id": "EV4", "arrival": 3, "duration": 2, "departure": 15},
]

# System settings
max_charging = 2
PEAK_HOURS = range(2, 6)

# Run uncontrolled charging simulation
schedule_uncontrolled = uncontrolled_scheduler(copy.deepcopy(evs))

# Run basic scheduler
schedule_basic = basic_scheduler(copy.deepcopy(evs), max_charging)

# Run smart scheduler
schedule_smart = smart_scheduler(copy.deepcopy(evs), max_charging, PEAK_HOURS)

# Extract time and load values
times_u = [t for t, _ in schedule_uncontrolled]
loads_u = [l for _, l in schedule_uncontrolled]

times_b = [t for t, _ in schedule_basic]
loads_b = [l for _, l in schedule_basic]

times_s = [t for t, _ in schedule_smart]
loads_s = [l for _, l in schedule_smart]

# Plot uncontrolled charging
plt.plot(times_u, loads_u, marker='o', linestyle='--', label="Uncontrolled")

# Plot basic scheduling
plt.plot(times_b, loads_b, marker='o', label="Basic Controlled")

# Plot smart scheduling
plt.plot(times_s, loads_s, marker='o', linestyle='-.', label="Smart Scheduling")

# Graph labels
plt.xlabel("Time")
plt.ylabel("Number of EVs Charging")

# Graph title
plt.title("EV Charging Load Comparison")

# Show grid and legend
plt.grid()
plt.legend()

# Save graph image
plt.savefig("comparison_graph.png")

# Display graph
plt.show()