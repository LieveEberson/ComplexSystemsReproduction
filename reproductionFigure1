""" This code is created for the purpose of reproducing 
Figure 1 of the Early Warning signals paper (Scheffer at al., 2009).
The code is now set to the values applied in our review and reproduction. 
You can adjust the parameters stated in the beginning to alter constants in the simulations.
"""

import numpy as np
import matplotlib.pyplot as plt
from scipy.integrate import cumulative_trapezoid
from scipy.optimize import brentq

# set parameters, can be adjusted
K = 10.0
highres_c = 1.8
lowres_c = 2.6
static_sigma = 0.02
high_sigma = 0.05

# differential equation
def f(X, c): return X*(1 - X/K) - c*X**2/(X**2 + 1)

# create simulations for 1000 samples 
def simulate(c, sigma, x0, n_samples=1000, dt=0.05, sub=20, seed=1):
    rng = np.random.default_rng(seed)
    x, out = x0, []
    for _ in range(n_samples):
        for _ in range(sub):
            x += f(x, c)*dt + sigma*np.sqrt(dt)*rng.standard_normal()
        out.append(x)
    return np.array(out)

# find equilibrium
def equilibrium(c):
    xs = np.linspace(K, 0.5, 2000)
    s = np.sign(f(xs, c))
    i = np.where(s[:-1] * s[1:] < 0)[0][0]
    return brentq(lambda x: f(x, c), xs[i+1], xs[i])

# distinguish between cases
cases = [dict(c=highres_c, sigma=static_sigma, title="High resilience"),
         dict(c=lowres_c, sigma=static_sigma, title="Low resilience"),
         dict(c=highres_c, sigma=high_sigma, title="High resilience, higher noise")]

for case in cases:
    case["xeq"] = equilibrium(case["c"])
    case["ts"] = simulate(case["c"], case["sigma"], case["xeq"])

# Shared state-space window across all rows
span = 1.1 * max(np.ptp(case["ts"]) for case in cases)

# create figures and save
fig, axes = plt.subplots(len(cases), 3, figsize=(12, 3.5*len(cases)))
for row, case in zip(axes, cases):
    c, ts = case["c"], case["ts"]
    lim = (ts.mean() - span/2, ts.mean() + span/2)

    X = np.linspace(0.01, 10, 1000)
    V = -cumulative_trapezoid(f(X, c), X, initial=0)
    row[0].plot(X, V); row[0].set(xlabel="State", ylabel="Potential", title=case["title"])

    row[1].plot(ts, lw=0.7)
    row[1].set(xlabel="Time, t", ylabel="State", ylim=lim)

    row[2].scatter(ts[:-1], ts[1:], s=6)
    r = np.corrcoef(ts[:-1], ts[1:])[0, 1]
    row[2].set(xlabel="State$_t$", ylabel="State$_{t+1}$", xlim=lim, ylim=lim)
    row[2].set_aspect("equal", adjustable="box")
    row[2].text(0.05, 0.95, f"s.d., {ts.std():.3f}\nCorrelation, {r:.2f}",
                transform=row[2].transAxes, va="top")
plt.tight_layout()
plt.savefig("figure1.png", dpi=300, bbox_inches="tight")
plt.show()
