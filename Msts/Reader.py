import numpy as np
from scipy.optimize import curve_fit
import pandas as pd
import matplotlib.pyplot as plt

# Data inlezen
df = pd.read_csv("1.5Hz_4.csv")

hz = 1.5

# Modeldefinitie
def model(x, A, f, c):
    return A * np.sin(2 * np.pi * f * x + c)

# Positiemodel (dubbele integratie van versnelling)
def position_model(x, A, f, c):
    return -A / (2 * np.pi * f)**2 * np.sin(2 * np.pi * f * x + c)

# Curve fitting
popt1, pcov1 = curve_fit(model, df['t'], df['a1'], p0=[1.7, hz, 0])
popt2, pcov2 = curve_fit(model, df['t'], df['a2'], p0=[1.9, hz, 0])

# Bereken fitted curves
curve1 = model(df['t'], *popt1)
curve2 = model(df['t'], *popt2)

# Plot originele data en fits
plt.figure(figsize=(10, 5))
plt.scatter(df['t'], df['a1'], s=3, label='a1 (data)', alpha=0.5)
plt.scatter(df['t'], df['a2'], s=3, label='a2 (data)', alpha=0.5)
plt.plot(df['t'], curve1, color='blue', label='Fit a1')
plt.plot(df['t'], curve2, color='red', label='Fit a2')
plt.xlabel("Tijd (s)")
plt.ylabel("Versnelling in (m/s^2)")
plt.title("Versnelling vs tijd")
plt.legend()
plt.grid(True)

# Print de parameters
# print("a1 fit parameters:", popt1)
# print("a2 fit parameters:", popt2)

# Bereken posities uit de fitparameters
pos1 = position_model(df['t'], *popt1)
pos2 = position_model(df['t'], *popt2)

# Maxima en verschil
max1 = np.max(pos1)
max2 = np.max(pos2)
verschil = max2 - max1


# Plot afstand
plt.figure(figsize=(10, 5))
plt.plot(df['t'], pos1, label='Positie a1', color='blue')
plt.plot(df['t'], pos2, label='Positie a2', color='red')
plt.xlabel("Tijd (s)")
plt.ylabel("Afstand (m)")
plt.title("Afstand vs tijd")
plt.legend()
plt.grid(True)

# # Voeg tekst toe linksonder in de grafiek
# plt.text(
#     0.02, 0.02,  # x en y in as-coördinaten (relatief)
#     f"Max Δ uitwijking tussen boven en beneden = {verschil:.4f} m",
#     fontsize=10,
#     transform=plt.gca().transAxes,
#     verticalalignment='bottom',
#     horizontalalignment='left',
#     bbox=dict(boxstyle="round,pad=0.3", facecolor="white", edgecolor="gray")
# )


max_d_plaat = np.max(pos2)
max_d_gebouw = np.max(pos1)

max_d_gebouw_norm = max_d_gebouw / max_d_plaat * .05


verschil = (max_d_gebouw_norm - .05) * 1e3
# Print verschil
# print("Max uitwijking a2 =", np.max(pos2), "m")
# print("Max uitwijking a1 =", np.max(pos1), "m")
print(f"uitwijking verschil = {verschil:.3} mm")

plt.show()