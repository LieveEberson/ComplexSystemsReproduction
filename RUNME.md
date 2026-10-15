# RUNME

Reproduction of Figure 1 from the Early Warning Signals paper (Scheffer et al., 2009), plus an interactive live demo.

## Files

| File | Purpose |
|------|---------|
| `environment.yml` | Conda environment with all dependencies |
| `reproductionFigure1.py` | Reproduces Figure 1 and saves it as `figure1.png` |
| `livedemo.py` | Interactive demo with sliders for harvesting capacity (`c`) and noise (`sigma`) |

## 1. Set up the environment

```
conda env create -f environment.yml
conda activate early-warning-signals
```

## 2. Reproduce Figure 1

```
python reproductionFigure1.py
```

This simulates three cases (high resilience, low resilience, high resilience with higher noise) and shows a 3x3 figure: potential landscape, time series, and lag-1 return plot with standard deviation and correlation. The figure is also saved as `figure1.png` (300 dpi) in the current folder.

Parameters you can change at the top of the file:

- `K`: carrying capacity (default 10.0)
- `highres_c`: harvesting capacity, high resilience case (default 1.8)
- `lowres_c`: harvesting capacity, low resilience case (default 2.6)
- `static_sigma`: baseline noise level (default 0.02)
- `high_sigma`: higher noise level (default 0.05)

## 3. Run the live demo

The demo uses `ipywidgets`, so it only works inside Jupyter (not with plain `python livedemo.py`).

```
jupyter lab
```

Then, in a new notebook, either paste the contents of `livedemo.py` into a cell, or run:

```
%run livedemo.py
```

Controls:

- **c**: maximum harvesting capacity (0.5 to 4.0, default 2.6)
- **sigma**: noise strength (0.005 to 0.06, default 0.03)
- **autoscale_potential**: tick to autoscale the potential plot, untick for a fixed y-axis

Sliders update the plot when you release them. The text in the third panel shows "(system tipped)" or "(collapsed state)" when the simulation has left the upper equilibrium.

## Troubleshooting

- **Sliders do not appear:** you are not running in Jupyter, or `ipywidgets` is not installed in the active environment. Check that `early-warning-signals` is activated and selected as the notebook kernel.
- **`ModuleNotFoundError`:** the environment is not activated. Run `conda activate early-warning-signals`.
