import streamlit as st
import copy
import matplotlib.pyplot as plt
import random

# Import all scheduling strategies
from Uncontrolled_charging import uncontrolled_scheduler
from Simple_scheduler import basic_scheduler
from Smart_scheduler import smart_scheduler

# Generate random EV dataset
def generate_evs(num_evs):
    evs = []
    for i in range(num_evs):
        arrival = random.randint(0, 10)
        duration = random.randint(1, 6)
        departure = arrival + duration + random.randint(1, 6)
        evs.append({"id": f"EV{i+1}", "arrival": arrival, "duration": duration, "departure": departure})
    return evs

# Page title
st.title("Smart EV Charging System ⚡")
st.write(
    "This simulator compares uncontrolled, basic, "
    "and smart EV charging strategies."
)

# Sidebar controls
st.sidebar.header("Simulation Settings")
max_charging = st.sidebar.slider("Max Charging Capacity", 1, 5, 3)
num_evs = st.sidebar.slider("Number of EVs", 3, 15, 7)
peak_start, peak_end = st.sidebar.slider("Peak Hour Range", 0, 12, (2, 6))

# Generate random EV dataset
evs = generate_evs(num_evs)
PEAK_HOURS = range(peak_start, peak_end)

# Run all scheduling simulations
schedule_uncontrolled = uncontrolled_scheduler(copy.deepcopy(evs))

schedule_basic = basic_scheduler(copy.deepcopy(evs), max_charging)

schedule_smart = smart_scheduler(copy.deepcopy(evs), max_charging, PEAK_HOURS)

# Extract graph data
times_u = [t for t, _ in schedule_uncontrolled]
loads_u = [l for _, l in schedule_uncontrolled]

times_b = [t for t, _ in schedule_basic]
loads_b = [l for _, l in schedule_basic]

times_s = [t for t, _ in schedule_smart]
loads_s = [l for _, l in schedule_smart]

# Quick stats cards
col1, col2, col3 = st.columns(3)
col1.metric("Total EVs", len(evs))
col2.metric("Max Capacity", max_charging)
col3.metric("Peak Hours", f"{peak_start} - {peak_end}")

# Dataset viewer
st.subheader("EV Dataset")
with st.expander("View EV Dataset"):
    st.dataframe(evs)

# Graph section
st.subheader("Load Comparison Graph")
st.caption("Graph updates automatically when settings change.")

fig, ax = plt.subplots() # Create graph canvas

ax.plot(times_u, loads_u, marker='o', linestyle='--', label="Uncontrolled") # Plot uncontrolled charging
ax.plot(times_b, loads_b, marker='o', label="Basic Controlled") # Plot basic scheduling
ax.plot(times_s, loads_s, marker='o', linestyle='-.', label="Smart Scheduling") # Plot smart scheduling

# Graph labels and styling
ax.set_xlabel("Time")
ax.set_ylabel("Number of EVs Charging")
ax.set_title("EV Charging Load Comparison")
ax.grid()
ax.legend()

st.pyplot(fig) # Display graph in Streamlit