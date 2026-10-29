import json
import os

import tkinter as tk
DATA_FILE = os.path.join(
    os.path.dirname(os.path.abspath(__file__)),
    "rainguard_data.json"
)

# ==================================================
# 1. WINDOW
# ==================================================

root = tk.Tk()
root.title("RainGuard - Landfill Cross-Section")
root.geometry("1050x700")
root.configure(bg="#0B132B")

title = tk.Label(
    root,
    text="RainGuard | Physical Environment",
    font=("Arial", 22, "bold"),
    fg="#4CC9F0",
    bg="#0B132B"
)
title.pack(pady=(12, 2))

subtitle = tk.Label(
    root,
    text="By ASD",
    font=("Arial", 11),
    fg="white",
    bg="#0B132B"
)
subtitle.pack(pady=(0, 8))

canvas = tk.Canvas(
    root,
    width=1000,
    height=570,
    bg="#DCEAF2",
    highlightthickness=0
)
canvas.pack(padx=10, pady=5)


# ==================================================
# 2. BACKGROUND AND GROUND
# ==================================================

# Distant hills
canvas.create_polygon(
    0, 150, 100, 90, 200, 130, 310, 75,
    420, 125, 540, 85, 680, 130, 810, 80,
    1000, 130, 1000, 240, 0, 240,
    fill="#B9D3A2",
    outline=""
)

# Ground surface
canvas.create_rectangle(
    0, 240, 1000, 390,
    fill="#A78B66",
    outline=""
)

canvas.create_text(
    65, 365,
    text="Ground",
    font=("Arial", 11, "bold"),
    fill="white"
)


# ==================================================
# 3. LANDFILL MOUND
# ==================================================

# Main mound
canvas.create_polygon(
    105, 240,
    195, 195,
    290, 145,
    400, 170,
    500, 225,
    560, 255,
    560, 300,
    105, 300,
    fill="#647C49",
    outline="#334D32",
    width=3
)

# Visible waste layers
canvas.create_polygon(
    120, 245,
    205, 207,
    295, 160,
    395, 183,
    485, 230,
    540, 258,
    540, 272,
    120, 272,
    fill="#685B50",
    outline=""
)

canvas.create_polygon(
    120, 273,
    540, 273,
    540, 290,
    120, 290,
    fill="#89715B",
    outline=""
)

# Simple waste symbols
for x, y in [
    (220, 235), (260, 216), (305, 225),
    (355, 205), (400, 226), (450, 244)
]:
    canvas.create_rectangle(
        x, y, x + 17, y + 9,
        fill="#B9A58B",
        outline="#40372E"
    )

canvas.create_text(
    320, 180,
    text="Landfill waste",
    font=("Arial", 12, "bold"),
    fill="white"
)

canvas.create_text(
    325, 305,
    text="Simplified waste layers",
    font=("Arial", 10),
    fill="white"
)


# ==================================================
# 4. CLEAN-WATER DIVERSION CHANNEL
# ==================================================

# Blue channel curves around the outside of the mound.
canvas.create_line(
    20, 220,
    85, 220,
    110, 230,
    150, 255,
    smooth=True,
    fill="#075985",
    width=15
)

canvas.create_line(
    20, 220,
    85, 220,
    110, 230,
    150, 255,
    smooth=True,
    fill="#38BDF8",
    width=8
)

canvas.create_text(
    125, 165,
    text="Clean-water diversion",
    font=("Arial", 10, "bold"),
    fill="#075985"
)

canvas.create_text(
    125, 181,
    text="Rainwater routed away",
    font=("Arial", 9),
    fill="#075985"
)


# ==================================================
# 5. LINER AND LEACHATE COLLECTION LAYER
# ==================================================

# Protective liner under the waste.
canvas.create_line(
    110, 300,
    560, 300,
    fill="#E76F51",
    width=10
)

canvas.create_text(
    330, 326,
    text="Protective liner (schematic)",
    font=("Arial", 10, "bold"),
    fill="#8A3524"
)

# Gravel/drainage layer beneath the waste.
canvas.create_rectangle(
    115, 312, 560, 343,
    fill="#C7BCA7",
    outline="#6B6256",
    width=2
)

# Perforated collection pipe, represented as a blue pipe.
canvas.create_line(
    135, 325,
    545, 325,
    fill="#075985",
    width=12
)

canvas.create_line(
    135, 325,
    545, 325,
    fill="#38BDF8",
    width=6
)

# Pipe perforations
for x in range(155, 530, 35):
    canvas.create_oval(
        x, 321, x + 5, 326,
        fill="#075985",
        outline=""
    )

canvas.create_text(
    330, 357,
    text="Leachate collection pipe",
    font=("Arial", 10, "bold"),
    fill="#075985"
)


# ==================================================
# 6. COLLECTION TANK
# ==================================================

# Tank body
canvas.create_rectangle(
    650, 280, 800, 425,
    fill="#8296A5",
    outline="#334155",
    width=3
)

# Tank top
canvas.create_oval(
    650, 268, 800, 292,
    fill="#AFC1CE",
    outline="#334155",
    width=3
)

# Simulated water inside the tank

# Simulated water inside the tank
water_surface_y = 350

water_rect = canvas.create_rectangle(
    657, water_surface_y, 793, 419,
    fill="#38BDF8",
    outline=""
)

water_surface = canvas.create_oval(
    657, water_surface_y - 10,
    793, water_surface_y + 10,
    fill="#38BDF8",
    outline=""
)


canvas.create_text(
    725, 305,
    text="Collection tank",
    font=("Arial", 12, "bold"),
    fill="#0B132B"
)

canvas.create_text(
    725, 390,
    text="Stored liquid",
    font=("Arial", 10, "bold"),
    fill="#0B132B"
)

# Pipe from collection layer to tank
canvas.create_line(
    545, 325,
    600, 325,
    600, 370,
    650, 370,
    fill="#075985",
    width=9
)

canvas.create_line(
    545, 325,
    600, 325,
    600, 370,
    650, 370,
    fill="#38BDF8",
    width=4
)


# ==================================================
# 7. VIRTUAL WATER-LEVEL SENSOR
# ==================================================

# Sensor support
canvas.create_line(
    830, 195,
    830, 350,
    fill="#334155",
    width=5
)

# Sensor head
canvas.create_rectangle(
    814, 190, 846, 216,
    fill="#334155",
    outline="#0B132B",
    width=2
)

# Sensor measurement line
canvas.create_line(
    830, 216,
    830, 340,
    fill="#E63946",
    width=2,
    dash=(5, 4)
)

canvas.create_text(
    880, 180,
    text="Water-level",
    font=("Arial", 10, "bold"),
    fill="#0B132B"
)

canvas.create_text(
    880, 195,
    text="sensor",
    font=("Arial", 10, "bold"),
    fill="#0B132B"
)

canvas.create_line(
    850, 210,
    865, 200,
    fill="#334155",
    width=1
)


# 8. RAINFALL INDICATOR

# Cloud
canvas.create_oval(
    650, 90, 705, 125,
    fill="#64748B",
    outline=""
)

canvas.create_oval(
    675, 72, 725, 120,
    fill="#64748B",
    outline=""
)

canvas.create_oval(
    700, 90, 750, 125,
    fill="#64748B",
    outline=""
)

canvas.create_text(
    700, 58,
    text="Rainfall",
    font=("Arial", 12, "bold"),
    fill="#0B132B"
)

# Rain streaks (illustrative)

# Animated raindrops
raindrops = []

for x in [665, 685, 705, 725, 745]:
    drop = canvas.create_line(
        x, 130,
        x - 5, 142,
        fill="#168AAD",
        width=3
    )
    raindrops.append(drop)


def animate_rain():
    for drop in raindrops:
        # Get the current coordinates of this raindrop.
        coords = canvas.coords(drop)

        # Move it downward.
        canvas.move(drop, 0, 5)

        # If it reaches the bottom of the rain area,
        # move it back to the cloud.
        coords = canvas.coords(drop)

        if coords[1] >= 150:
            canvas.move(drop, 0, 130 - coords[1])

    # Schedule the next animation frame.
    root.after(100, animate_rain)


canvas.create_text(
    700, 155,
    text="Rain gauge / forecast",
    font=("Arial", 9),
    fill="#075985"
)

# 9. INFORMATION PANEL

canvas.create_rectangle(
    25, 440, 975, 545,
    fill="#FFFFFF",
    outline="#94A3B8",
    width=2
)

canvas.create_text(
    45, 458,
    text="HOW THE SYSTEM WORKS",
    anchor="w",
    font=("Arial", 12, "bold"),
    fill="#075985"
)

canvas.create_text(
    45, 482,
    text="1. Divert clean rainwater away from the waste.",
    anchor="w",
    font=("Arial", 10),
    fill="#0B132B"
)

canvas.create_text(
    45, 502,
    text="2. Collect simulated liquid through a separate drainage system.",
    anchor="w",
    font=("Arial", 10),
    fill="#0B132B"
)

canvas.create_text(
    520, 482,
    text="3. Monitor the collection tank's water level.",
    anchor="w",
    font=("Arial", 10),
    fill="#0B132B"
)

canvas.create_text(
    520, 502,
    text="4. Send readings to RainGuard's risk dashboard (later lesson).",
    anchor="w",
    font=("Arial", 10),
    fill="#0B132B"
)

# Disclaimer
canvas.create_text(
    500, 558,
    text="Educational illustration only — not a real landfill engineering design.",
    font=("Arial", 9, "italic"),
    fill="#334155"
)


# 10. WATER ANIMATION

water_surface_y = 350
water_direction = -1
rainfall_intensity = "Light"
inflow_rate = 0.3
outflow_rate = 0.1
pump_on = False


def animate_water():
    global water_surface_y, water_direction

    # Rainfall determines how quickly the level rises.
    if rainfall_intensity == "Light":
        inflow_rate = 0.3
    else:
        inflow_rate = 1.2

    net_change = inflow_rate - outflow_rate
    water_surface_y -= net_change

    # Keep the level within the visible tank.
    if water_surface_y <= 290:
        water_surface_y = 290

    # Update the water shapes.
    canvas.coords(
        water_rect,
        657, water_surface_y,
        793, 419
    )
    canvas.coords(
        water_surface,
        657, water_surface_y - 10,
        793, water_surface_y + 10
    )


    root.after(80, animate_water)
    tank_bottom = 419
    tank_top = 280

    water_level = (
        (tank_bottom - water_surface_y)
        / (tank_bottom - tank_top)
    ) * 100

    water_level = max(0, min(100, water_level))

    with open(DATA_FILE, "w") as file:
        json.dump({
            "water_level": water_level,
            "rainfall": (
                "Heavy"
                if rainfall_intensity == "Heavy"
                else "Light"
            ),
            "pump_on": pump_on
        }, file)

# 11. START WINDOW

def toggle_rainfall():
    global rainfall_intensity

    if rainfall_intensity == "Light":
        rainfall_intensity = "Heavy"
        rain_button.config(text="Switch to Light Rain")
    else:
        rainfall_intensity = "Light"
        rain_button.config(text="Switch to Heavy Rain")


rain_button = tk.Button(
    root,
    text="Switch to Heavy Rain",
    command=toggle_rainfall,
    font=("Arial", 11, "bold"),
    bg="#4CC9F0",
    fg="#0B132B"
)

rain_button.pack(pady=5)
def toggle_pump():
    global pump_on, outflow_rate

    pump_on = not pump_on

    if pump_on:
        outflow_rate = 1.5
        pump_button.config(text="Pump: ON")
    else:
        outflow_rate = 0.1
        pump_button.config(text="Pump: OFF")


pump_button = tk.Button(
    root,
    text="Pump: OFF",
    command=toggle_pump,
    font=("Arial", 11)
)

pump_button.pack()

animate_water()
animate_rain()

# ==================================================
# 11. CHANNEL FLOW ANIMATION
# ==================================================

# Each marker represents water moving along a channel.
clean_flow_markers = []
leachate_flow_markers = []

# Clean-water diversion channel markers.
for x in [30, 55, 80]:
    marker = canvas.create_oval(
        x, 213, x + 9, 222,
        fill="#E0F7FF",
        outline="#075985"
    )
    clean_flow_markers.append(marker)

# Leachate collection pipe markers.
for x in [180, 230, 280]:
    marker = canvas.create_oval(
        x, 319, x + 9, 328,
        fill="#E0F7FF",
        outline="#075985"
    )
    leachate_flow_markers.append(marker)


def animate_channel_flow():
    # Move clean-water markers to the right.
    for marker in clean_flow_markers:
        canvas.move(marker, 3, 0)

        x1, y1, x2, y2 = canvas.coords(marker)

        # Loop back to the channel entrance.
        if x1 > 150:
            canvas.move(marker, 30 - x1, 0)

    # Move collection-pipe markers toward the tank.
    for marker in leachate_flow_markers:
        canvas.move(marker, 3, 0)

        x1, y1, x2, y2 = canvas.coords(marker)

        # Loop back to the beginning of the visible pipe.
        if x1 > 540:
            canvas.move(marker, 180 - x1, 0)

    root.after(80, animate_channel_flow)


animate_channel_flow()
root.mainloop()

