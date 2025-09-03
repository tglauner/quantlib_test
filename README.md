# QuantLib Test

This repository showcases small examples of using [QuantLib](https://www.quantlib.org/) from Python.  It includes a simple Flask web app for repricing a portfolio and several stand‑alone scripts that construct or price instruments.

## Repository Structure

| Path | Description |
| --- | --- |
| `app.py` | Flask application that displays a valuation blotter and lets users edit SOFR curve rates through a form. It uses the `price_portfolio` helper to compute NPVs. |
| `portfolio.py` | Functions for building a SOFR zero curve, creating interest‑rate swaps and swaptions, and pricing a small portfolio consisting of a swap, a European swaption, and a Bermudan swaption. |
| `build_SOFR_curve.py` | Script that constructs a SOFR term structure from OIS swap quotes and prints discount factors for select maturities along with a DataFrame of daily factors. |
| `price_bermudan_swaption.py` | Demonstrates pricing a Bermudan swaption using the Hull–White short‑rate model and a tree swaption engine. |
| `read_rates_vols_from_Excel.py` | Placeholder for future functionality to load market data from Excel. |
| `today.py` | Minimal example showing how to set QuantLib's evaluation date. |
| `templates/` | HTML templates used by the web app. `blotter.html` renders the portfolio table and a rate‑editing form, while `index.html` is an alternate view showing instrument NPVs. |
| `requirements.txt` | Python dependencies. |
| `LICENSE` | Apache 2.0 license. |

## Installation

1. Create and activate a virtual environment (optional):

   ```bash
   python -m venv .venv
   source .venv/bin/activate
   ```

2. Install dependencies:

   ```bash
   pip install -r requirements.txt
   ```

## Usage

### Web Application

Run the Flask app and open `http://localhost:5000` in a browser:

```bash
python app.py
```

The page displays the NPVs of a swap, a European swaption, and a Bermudan swaption.  You can adjust the SOFR zero‑curve rates in the form and reprice the portfolio.

### Stand‑alone Scripts

- **Build SOFR Curve**

  ```bash
  python build_SOFR_curve.py
  ```
  Prints sample discount factors and a table of daily factors.

- **Price Bermudan Swaption**

  ```bash
  python price_bermudan_swaption.py
  ```
  Computes the NPV of a Bermudan swaption using the Hull–White model.

- **Show Today's Date**

  ```bash
  python today.py
  ```
  Outputs the evaluation date currently set in QuantLib.

## License

This project is licensed under the terms of the [Apache License 2.0](LICENSE).

## Contributing

Issues and pull requests are welcome.  The repository is intended as a lightweight sandbox for experimenting with QuantLib in Python.

## Testing

Run the test suite (none are included yet) with:

```bash
python -m pytest
```

