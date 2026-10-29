
import tkinter as tk
from tkinter import ttk
from datetime import datetime
import random
import json
import os

DATA_FILE = os.path.join(
    os.path.dirname(os.path.abspath(__file__)),
    "rainguard_data.json"
)



# 1. RAINGUARD CONFIGURATION


APP_TITLE = "RainGuard - Landfill Overflow Monitoring Simulator"

CRITICAL_LEVEL = 90       # Simulated critical level, in cm
TANK_CAPACITY = 100       # Simulated maximum level, in cm
NORMAL_RISE_RATE = 1.0    # Simulated rise rate, in cm per minute





# 2. SIMULATED SENSOR DATA


water_level = 35.0
rainfall = "Moderate"
blockage = False
pump_failure = False
sensor_fault = False

previous_level = water_level
rise_rate = 0.0
estimated_time = None

simulation_running = False
after_id = None

incident_log = []


# ============================================================
# 3. MAIN WINDOW
# ============================================================

root = tk.Tk()
root.title(APP_TITLE)
root.geometry("850x720")
root.minsize(760, 650)
root.configure(bg="#0B132B")



# 4. HELPER FUNCTIONS


def log_event(message):
    """Add a timestamped message to the incident log."""

    timestamp = datetime.now().strftime("%H:%M:%S")
    entry = f"[{timestamp}] {message}"

    incident_log.append(entry)
    log_text.configure(state="normal")
    log_text.insert("end", entry + "\n")
    log_text.see("end")
    log_text.configure(state="disabled")


def update_display():
    """Refresh all dashboard readings and status messages."""

    level_label.config(text=f"{water_level:.1f} cm")
    level_bar["value"] = max(0, min(water_level, TANK_CAPACITY))

    rainfall_label.config(text=rainfall)

    blockage_label.config(
        text="DETECTED" if blockage else "Not detected",
        fg="#FF6B6B" if blockage else "#4CC9F0"
    )

    pump_label.config(
        text="FAILURE" if pump_failure else "Operating",
        fg="#FF6B6B" if pump_failure else "#4CC9F0"
    )

    sensor_label.config(
        text="FAULT" if sensor_fault else "OK",
        fg="#FF6B6B" if sensor_fault else "#4CC9F0"
    )

    rise_label.config(text=f"{rise_rate:.1f} cm/min")

    if sensor_fault:
        risk = "UNKNOWN — SENSOR FAULT"
        colour = "#FF6B6B"
        time_text = "Unavailable"
    elif water_level >= CRITICAL_LEVEL:
        risk = "CRITICAL"
        colour = "#FF6B6B"
        time_text = "Critical level reached"
    elif blockage or pump_failure:
        risk = "HIGH — CHECK SYSTEM"
        colour = "#FF9F1C"
        time_text = (
            f"{estimated_time:.1f} min"
            if estimated_time is not None
            else "Unavailable"
        )
    elif estimated_time is not None and estimated_time <= 10:
        risk = "HIGH"
        colour = "#FF9F1C"
        time_text = f"{estimated_time:.1f} min"
    elif estimated_time is not None and estimated_time <= 30:
        risk = "MODERATE"
        colour = "#FFD166"
        time_text = f"{estimated_time:.1f} min"
    else:
        risk = "LOWER — KEEP MONITORING"
        colour = "#4CC9F0"
        time_text = (
            f"{estimated_time:.1f} min"
            if estimated_time is not None
            else "Not currently rising"
        )

    risk_label.config(text=risk, fg=colour)
    time_label.config(text=time_text)

    if sensor_fault:
        recommendation = (
            "Check the sensor and verify the reading "
            "before relying on the dashboard."
        )
    elif water_level >= CRITICAL_LEVEL:
        recommendation = (
            "Critical threshold reached. Follow the site's "
            "approved emergency response procedure."
        )
    elif blockage or pump_failure:
        recommendation = (
            "Possible system problem detected. Notify the "
            "responsible operator and follow site procedures."
        )
    elif rainfall == "Heavy":
        recommendation = (
            "Heavy rainfall scenario: monitor readings closely "
            "and check approved drainage procedures."
        )
    else:
        recommendation = (
            "Continue monitoring. This is a simulated reading, "
            "not a real site safety assessment."
        )

    recommendation_label.config(
        text=recommendation,
        wraplength=730
    )


def calculate_rise_rate(old_level, new_level):
    """Calculate the change in simulated level per minute."""

    return new_level - old_level


def calculate_time_to_critical(level, rate):
    """Estimate time to the critical threshold if the rate stays constant."""

    if rate <= 0:
        return None

    if level >= CRITICAL_LEVEL:
        return 0.0

    return (CRITICAL_LEVEL - level) / rate


# ============================================================
# 5. SIMULATION CONTROLS
# ============================================================


def simulate_reading():
    """Read the environment data or generate simulated readings."""

    global water_level, previous_level
    global rise_rate, estimated_time, after_id, rainfall

    if not simulation_running:
        return

    if os.path.exists(DATA_FILE):
        try:
            with open(DATA_FILE, "r") as file:
                data = json.load(file)

            old_level = water_level
            water_level = float(data["water_level"])
            rainfall = data["rainfall"]

            # Convert the change over 2 seconds to a per-minute rate.
            rise_rate = (water_level - old_level) * 30
            previous_level = old_level

            estimated_time = calculate_time_to_critical(
                water_level, rise_rate
            )

            update_display()

        except (OSError, ValueError, KeyError, json.JSONDecodeError):
            log_event("Environment data unavailable; checking again.")

        after_id = root.after(2000, simulate_reading)
        return

    # Fallback: use the original dashboard simulation if the
    # environment has not created its data file yet.
    previous_level = water_level

    if rainfall == "Light":
        rise = random.uniform(0.0, 1.0)
    elif rainfall == "Moderate":
        rise = random.uniform(0.2, 2.0)
    else:
        rise = random.uniform(1.0, 4.0)

    if blockage:
        rise += random.uniform(0.5, 1.5)

    if pump_failure:
        rise += random.uniform(0.5, 2.0)

    if sensor_fault:
        rise_rate = 0.0
        estimated_time = None
        log_event("Sensor fault: reading marked unreliable.")
    else:
        water_level = min(
            TANK_CAPACITY,
            max(0.0, water_level + rise)
        )

        rise_rate = calculate_rise_rate(previous_level, water_level)
        estimated_time = calculate_time_to_critical(
            water_level, rise_rate
        )

        log_event(
            f"Level: {water_level:.1f} cm | "
            f"Rise: {rise_rate:.1f} cm/min | "
            f"Rain: {rainfall}"
        )

        if water_level >= CRITICAL_LEVEL:
            log_event("ALERT: Simulated critical level reached!")

    update_display()
    after_id = root.after(2000, simulate_reading)

def start_simulation():
    """Start the repeating simulation."""

    global simulation_running

    if not simulation_running:
        simulation_running = True
        status_label.config(text="SIMULATION RUNNING", fg="#4CC9F0")
        log_event("Simulation started.")
        simulate_reading()


def stop_simulation():
    """Stop generating new readings."""

    global simulation_running
    global after_id

    simulation_running = False

    if after_id is not None:
        root.after_cancel(after_id)
        after_id = None

    status_label.config(text="SIMULATION STOPPED", fg="#FFD166")
    log_event("Simulation stopped.")


def reset_simulation():
    """Restore the initial simulated conditions."""

    global water_level
    global previous_level
    global rise_rate
    global estimated_time

    stop_simulation()

    water_level = 35.0
    previous_level = water_level
    rise_rate = 0.0
    estimated_time = None

    log_event("Simulation reset to initial conditions.")
    update_display()


def change_rainfall(event=None):
    """Update the simulated rainfall condition."""

    global rainfall

    rainfall = rainfall_choice.get()
    log_event(f"Rainfall changed to {rainfall}.")
    update_display()


def toggle_blockage():
    """Switch the simulated blockage condition on or off."""

    global blockage

    blockage = blockage_var.get()
    log_event(
        "Blockage detected." if blockage
        else "Blockage simulation cleared."
    )
    update_display()


def toggle_pump_failure():
    """Switch the simulated pump-failure condition on or off."""

    global pump_failure

    pump_failure = pump_var.get()
    log_event(
        "Pump failure simulated." if pump_failure
        else "Pump operation restored in simulation."
    )
    update_display()


def toggle_sensor_fault():
    """Switch the simulated sensor fault on or off."""

    global sensor_fault

    sensor_fault = sensor_var.get()
    log_event(
        "Sensor fault enabled." if sensor_fault
        else "Sensor fault cleared."
    )
    update_display()


def add_manual_rise():
    """Increase the simulated level to test alert thresholds."""

    global water_level
    global previous_level
    global rise_rate
    global estimated_time

    if sensor_fault:
        log_event("Manual rise ignored: sensor fault is active.")
        return

    previous_level = water_level
    water_level = min(TANK_CAPACITY, water_level + 10.0)

    rise_rate = calculate_rise_rate(previous_level, water_level)
    estimated_time = calculate_time_to_critical(
        water_level,
        rise_rate
    )

    log_event("Manual test: level increased by 10 cm.")
    update_display()


# ============================================================
# 6. BUILD THE DASHBOARD
# ============================================================

title_label = tk.Label(
    root,
    text="RainGuard",
    font=("Arial", 25, "bold"),
    fg="#4CC9F0",
    bg="#0B132B"
)
title_label.pack(pady=(15, 2))

subtitle_label = tk.Label(
    root,
    text="Smart Landfill Overflow Prevention Simulator",
    font=("Arial", 11),
    fg="white",
    bg="#0B132B"
)
subtitle_label.pack(pady=(0, 5))

status_label = tk.Label(
    root,
    text="SIMULATION STOPPED",
    font=("Arial", 10, "bold"),
    fg="#FFD166",
    bg="#0B132B"
)
status_label.pack(pady=4)


# ------------------ SENSOR READINGS --------------------------

readings_frame = tk.LabelFrame(
    root,
    text="Simulated Sensor Readings",
    font=("Arial", 11, "bold"),
    fg="white",
    bg="#1C2541",
    padx=15,
    pady=10
)
readings_frame.pack(fill="x", padx=20, pady=8)

level_title = tk.Label(
    readings_frame,
    text="Water Level",
    fg="white",
    bg="#1C2541"
)
level_title.grid(row=0, column=0, sticky="w")

level_label = tk.Label(
    readings_frame,
    text="35.0 cm",
    font=("Arial", 17, "bold"),
    fg="#4CC9F0",
    bg="#1C2541"
)
level_label.grid(row=0, column=1, sticky="w", padx=10)

level_bar = ttk.Progressbar(
    readings_frame,
    maximum=TANK_CAPACITY,
    length=280,
    mode="determinate"
)
level_bar.grid(row=1, column=0, columnspan=2, sticky="ew", pady=8)

rise_title = tk.Label(
    readings_frame,
    text="Rate of Rise:",
    fg="white",
    bg="#1C2541"
)
rise_title.grid(row=2, column=0, sticky="w")

rise_label = tk.Label(
    readings_frame,
    text="0.0 cm/min",
    fg="#4CC9F0",
    bg="#1C2541"
)
rise_label.grid(row=2, column=1, sticky="w", padx=10)

rainfall_title = tk.Label(
    readings_frame,
    text="Rainfall:",
    fg="white",
    bg="#1C2541"
)
rainfall_title.grid(row=3, column=0, sticky="w", pady=5)

rainfall_label = tk.Label(
    readings_frame,
    text="Moderate",
    fg="#4CC9F0",
    bg="#1C2541"
)
rainfall_label.grid(row=3, column=1, sticky="w", padx=10)


# ------------------ RISK ASSESSMENT -------------------------

risk_frame = tk.LabelFrame(
    root,
    text="Risk Assessment",
    font=("Arial", 11, "bold"),
    fg="white",
    bg="#1C2541",
    padx=15,
    pady=10
)
risk_frame.pack(fill="x", padx=20, pady=8)

risk_label = tk.Label(
    risk_frame,
    text="LOWER — KEEP MONITORING",
    font=("Arial", 14, "bold"),
    fg="#4CC9F0",
    bg="#1C2541"
)
risk_label.pack(anchor="w")

time_row = tk.Frame(risk_frame, bg="#1C2541")
time_row.pack(fill="x", pady=5)

tk.Label(
    time_row,
    text="Estimated time to critical level:",
    fg="white",
    bg="#1C2541"
).pack(side="left")

time_label = tk.Label(
    time_row,
    text="Not currently rising",
    fg="#4CC9F0",
    bg="#1C2541"
)
time_label.pack(side="left", padx=8)

recommendation_label = tk.Label(
    risk_frame,
    text="Continue monitoring.",
    justify="left",
    anchor="w",
    fg="white",
    bg="#1C2541"
)
recommendation_label.pack(fill="x", pady=5)


# ------------------ FAULT INDICATORS ------------------------

fault_frame = tk.LabelFrame(
    root,
    text="Simulated System Conditions",
    font=("Arial", 11, "bold"),
    fg="white",
    bg="#1C2541",
    padx=15,
    pady=10
)
fault_frame.pack(fill="x", padx=20, pady=8)

blockage_var = tk.BooleanVar(value=False)
pump_var = tk.BooleanVar(value=False)
sensor_var = tk.BooleanVar(value=False)

blockage_check = tk.Checkbutton(
    fault_frame,
    text="Simulate blockage",
    variable=blockage_var,
    command=toggle_blockage,
    fg="white",
    bg="#1C2541",
    selectcolor="#0B132B",
    activebackground="#1C2541",
    activeforeground="white"
)
blockage_check.grid(row=0, column=0, sticky="w", padx=5)

pump_check = tk.Checkbutton(
    fault_frame,
    text="Simulate pump failure",
    variable=pump_var,
    command=toggle_pump_failure,
    fg="white",
    bg="#1C2541",
    selectcolor="#0B132B",
    activebackground="#1C2541",
    activeforeground="white"
)
pump_check.grid(row=0, column=1, sticky="w", padx=5)

sensor_check = tk.Checkbutton(
    fault_frame,
    text="Simulate sensor fault",
    variable=sensor_var,
    command=toggle_sensor_fault,
    fg="white",
    bg="#1C2541",
    selectcolor="#0B132B",
    activebackground="#1C2541",
    activeforeground="white"
)
sensor_check.grid(row=0, column=2, sticky="w", padx=5)

blockage_label = tk.Label(
    fault_frame,
    text="Not detected",
    fg="#4CC9F0",
    bg="#1C2541"
)
blockage_label.grid(row=1, column=0, sticky="w", padx=5, pady=5)

pump_label = tk.Label(
    fault_frame,
    text="Operating",
    fg="#4CC9F0",
    bg="#1C2541"
)
pump_label.grid(row=1, column=1, sticky="w", padx=5, pady=5)

sensor_label = tk.Label(
    fault_frame,
    text="OK",
    fg="#4CC9F0",
    bg="#1C2541"
)
sensor_label.grid(row=1, column=2, sticky="w", padx=5, pady=5)


# ------------------ CONTROLS --------------------------------

control_frame = tk.Frame(root, bg="#0B132B")
control_frame.pack(fill="x", padx=20, pady=8)

tk.Button(
    control_frame,
    text="Start",
    command=start_simulation,
    bg="#4CC9F0",
    fg="#0B132B",
    width=10
).pack(side="left", padx=4)

tk.Button(
    control_frame,
    text="Stop",
    command=stop_simulation,
    bg="#FFD166",
    fg="#0B132B",
    width=10
).pack(side="left", padx=4)

tk.Button(
    control_frame,
    text="Reset",
    command=reset_simulation,
    bg="#E0E1DD",
    fg="#0B132B",
    width=10
).pack(side="left", padx=4)

tk.Button(
    control_frame,
    text="Test +10 cm",
    command=add_manual_rise,
    bg="#FF9F1C",
    fg="#0B132B",
    width=12
).pack(side="left", padx=4)

tk.Label(
    control_frame,
    text="Rain:",
    fg="white",
    bg="#0B132B"
).pack(side="left", padx=(12, 3))

rainfall_choice = ttk.Combobox(
    control_frame,
    values=["Light", "Moderate", "Heavy"],
    state="readonly",
    width=10
)
rainfall_choice.set("Moderate")
rainfall_choice.pack(side="left", padx=3)
rainfall_choice.bind("<<ComboboxSelected>>", change_rainfall)


# ------------------ INCIDENT LOG ----------------------------

log_frame = tk.LabelFrame(
    root,
    text="Incident Log",
    font=("Arial", 11, "bold"),
    fg="white",
    bg="#1C2541",
    padx=10,
    pady=5
)
log_frame.pack(fill="both", expand=True, padx=20, pady=(5, 15))

log_text = tk.Text(
    log_frame,
    height=6,
    bg="#0B132B",
    fg="#E0E1DD",
    insertbackground="white",
    state="disabled",
    wrap="word"
)
log_text.pack(fill="both", expand=True)


# ============================================================
# 7. INITIALIZE AND RUN
# ============================================================

update_display()
log_event("RainGuard simulator initialized.")
log_event("All readings are simulated, not from real sensors.")

root.mainloop()
