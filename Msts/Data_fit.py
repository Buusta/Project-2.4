import numpy as np
import matplotlib.pyplot as plt
from scipy.optimize import curve_fit

# Data
_1Hz = np.array([4.13, 3.96, 3.64, 3.39, 3.76])
_12Hz = np.array([5.21, 5.11, 5.75, 5.86, 5.24])
_14Hz = np.array([7.26, 7.35, 7.71, 7.11, 7.26])
_15Hz = np.array([8.58, 10.2, 8.93])

# Berekeningen
means = [
    0,
    np.mean(_1Hz),
    np.mean(_12Hz),
    np.mean(_14Hz),
    np.mean(_15Hz)
]
stds = [
    0.13,  # handmatig gegeven
    np.std(_1Hz, ddof=1),
    np.std(_12Hz, ddof=1),
    np.std(_14Hz, ddof=1),
    np.std(_15Hz, ddof=1)
]

x = np.array([0, 1.0, 1.2, 1.4, 1.5])
y = np.array(means)
y_err = np.array(stds)

# Kwadratische functie
def quadratic(f, a, b, c):
    return a * f**2 + b * f + c

# Curve fit met standaarddeviaties als gewichten
popt, pcov = curve_fit(quadratic, x, y, sigma=y_err, absolute_sigma=True)

# Genereer gladde curve voor plot
x_fit = np.linspace(min(x), max(x), 200)
y_fit = quadratic(x_fit, *popt)

# Plot
plt.figure(figsize=(8, 5))
plt.errorbar(x, y, yerr=y_err, fmt='o', capsize=5, label='Gemiddelde ± STD', color='royalblue')
plt.plot(x_fit, y_fit, label='Kwadratische fit', color='darkorange')
plt.xticks(x)
plt.xlabel('Frequentie (Hz)')
plt.ylabel('Verplaatsing (cm)')
plt.title('Gebouwverplaatsing bij verschillende frequenties')
plt.legend()
plt.grid(True)
plt.tight_layout()
plt.show()

# Print fit parameters (optioneel)
print(f"Fit parameters: a = {popt[0]:.4f}, b = {popt[1]:.4f}, c = {popt[2]:.4f}")
