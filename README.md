# Primatif Astrology 🌪️✨🐺🌲

A professional-grade, high-precision Vedic astrology engine built for deep research and professional cosmic blueprinting. This system utilizes NASA JPL ephemeris data to generate arc-second accurate Jyotish calculations.

## Core Philosophy (Primatif)

Combining mental precision (🌪️), animalistic drive (🐺), and animistic connection to natural roots (🌲).

## Features

- **High-Precision Engine:** Powered by `jyotishganit` and NASA DE421 ephemeris.
- **Modular Architecture:** Clean separation between calculation, visualization, and reporting.
- **Visual Chart Generation:** Automated SVG and PNG rendering of D1, D9, D10, and D7 charts in North Indian style.
- **Professional Reporting:** Generates a comprehensive PDF "Cosmic Blueprint" including planetary strengths (Shadbala) and Panchanga details.
- **Multi-Profile Support:** Easily generate reports for different individuals via simple JSON configuration.

## Setup

1. **Clone the repository.**
2. **Initialize environment:**

    ```bash
    just setup
    ```

    *Or manually:*

    ```bash
    pip install -r requirements.txt
    mkdir -p profiles charts data src
    ```

## Usage

### 1. Create a Profile

Place a JSON file in the `profiles/` directory (e.g., `profiles/my_details.json`):

```json
{
  "name": "Key",
  "birth_date": "1995-03-03 03:33:33",
  "latitude": 37.7850,
  "longitude": -122.4391,
  "timezone_offset": -7.0
}
```

### 2. Generate Blueprint

```bash
python3 main.py profiles/my_details.json
```

*Using Just:* `just run profiles/my_details.json`

## Project Structure

- `main.py`: Entry point for the system.
- `src/`: Core logic (Engine, Visuals, Reporter, Utils).
- `profiles/`: User configuration files (Gitignored).
- `charts/`: Generated blueprints and images (Gitignored).
- `data/`: Large astronomical data files (Gitignored).
- `Justfile`: Automation tasks.

## License

This project is licensed under the [MIT License](LICENSE).

---
*Built for the observation of the stars and the grounding of the spirit.* 🌲🌀🐺✨
