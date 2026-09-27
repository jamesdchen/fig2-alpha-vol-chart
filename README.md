# Figure 2–style alpha vs volatility chart

Recreates the trained-component **alpha vs book volatility** scatter from Zhu, He, and Cucuringu (2026), *Quantifying the Contributions of Clustering to Statistical Arbitrage*, using the authors’ public Zenodo replication file `alpha_vol_points_v3_cal6913.csv`.

- Blue circles: 12 clusterizers  
- Red squares: controls — no clustering (`K=1`) and random partition  

Paper / data: [doi:10.5281/zenodo.22241254](https://doi.org/10.5281/zenodo.22241254)  
Authors’ full replication code: [lzwbh/clustering-statarb-replication](https://github.com/lzwbh/clustering-statarb-replication)

## Setup

```bash
python3 -m venv .venv
source .venv/bin/activate
pip install matplotlib
```

## Run

```bash
python plot_alpha_vol.py
# or:
python plot_alpha_vol.py --csv data/alpha_vol_points_v3_cal6913.csv --out fig2_alpha_vol_recreated.png
```

A small copy of the Zenodo CSV is included under `data/` so the plot runs without a separate download. For the full package (PnL series, partitions, etc.), use the Zenodo record above.

## License

Plotting script: MIT.  
Source CSV: CC BY 4.0 (Zhu et al., 2026 Zenodo replication data).
