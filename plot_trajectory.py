import pandas as pd
import matplotlib.pyplot as plt

data = pd.read_csv("tracked_positions.csv")
serve_data = data[
    (data["Frame"] >= 165) &
    (data["Frame"] <= 170)
]

x_positions = data["X"]
y_positions = data["Y"]

plt.plot(
    serve_data["X"],
    serve_data["Y"],
    marker="o",
    markersize=5,
    linewidth=1
)

plt.gca().invert_yaxis()

plt.xlabel("X Position (pixels)")
plt.ylabel("Y Position (pixels)")
plt.title("Tracked Tennis Ball Trajectory")

plt.grid()
plt.show()