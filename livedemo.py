""" This code is created for the purpose of showing a live demo in the presentation of the Review.
Running the code creates Figure 1 of the Early Warning signals paper (Scheffer at al., 2009),
with sliders for the maximum harvesting capacity (c) and the noise applied (sigma). """


import numpy as np
import matplotlib.pyplot as plt
from scipy.integrate import cumulative_trapezoid
from scipy.optimize import brentq
from ipywidgets import interact, FloatSlider

# set values
K = 10.0
DT, SUB, N = 0.05, 20, 1000
WINDOW = 0.6
NOISE = np.random.default_rng(1).standard_normal(N * SUB).tolist()

# differential equation
def f(X, c): return X*(1 - X/K) - c*X**2/(X**2 + 1)

# find equilibrium
def equilibrium(c):
    """Highest stable equilibrium: upper branch if it exists, else the lower one."""
    xs = np.linspace(0.01, K, 4000)
    fx = f(xs, c)
    idx = np.where(fx[:-1] * fx[1:] < 0)[0]
    roots = [brentq(lambda x: f(x, c), xs[i], xs[i+1]) for i in idx]
    stable = [r for r in roots if f(r + 1e-4, c) - f(r - 1e-4, c) < 0]
    return max(stable)

# run simulations
def simulate(c, sigma, x0):
    x, out, k = x0, np.empty(N), 0
    sq = sigma * np.sqrt(DT)
    for i in range(N):
        for _ in range(SUB):
            x += (x*(1 - x/K) - c*x*x/(x*x + 1))*DT + sq*NOISE[k]
            x = abs(x)                      # reflect at 0
            k += 1
        out[i] = x
    return out

X = np.linspace(0.01, 10, 1000)

# plot figures
def plot(c, sigma, autoscale_potential):
    xeq = equilibrium(c)
    ts = simulate(c, sigma, xeq)
    lim = (ts.mean() - WINDOW/2, ts.mean() + WINDOW/2)
    r = np.corrcoef(ts[:-1], ts[1:])[0, 1]

    fig, ax = plt.subplots(1, 3, figsize=(13, 4))

    V = -cumulative_trapezoid(f(X, c), X, initial=0)
    ax[0].plot(X, V)
    ax[0].plot(xeq, np.interp(xeq, X, V), "o", color="C3")
    ax[0].set(xlabel="State", ylabel="Potential", title=f"c = {c:.2f}")
    if not autoscale_potential:
        ax[0].set_ylim(-14, 18)

    ax[1].plot(ts, lw=0.7)
    ax[1].set(xlabel="Time, t", ylabel="State", ylim=lim)

    ax[2].scatter(ts[:-1], ts[1:], s=6)
    ax[2].set(xlabel="State$_t$", ylabel="State$_{t+1}$", xlim=lim, ylim=lim)
    ax[2].set_aspect("equal", adjustable="box")
    label = f"s.d., {ts.std():.3f}\nCorrelation, {r:.2f}"
    if xeq < 3:
        label += "\n(collapsed state)"
    elif ts.min() < 3:
        label += "\n(system tipped)"
    ax[2].text(0.05, 0.95, label, transform=ax[2].transAxes, va="top")

    plt.tight_layout()
    plt.show()

# add sliders
interact(plot,
         c=FloatSlider(value=2.6, min=0.5, max=4.0, step=0.05,
                       description="c", continuous_update=False,
                       readout_format=".2f", layout={"width": "500px"}),
         sigma=FloatSlider(value=0.03, min=0.005, max=0.06, step=0.005,
                           description="sigma", continuous_update=False,
                           readout_format=".3f", layout={"width": "500px"}),
         autoscale_potential=True);
