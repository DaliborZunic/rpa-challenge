# RPA Challenge — Input Forms

Python + Playwright solution for the [RPA Challenge](https://rpachallenge.com/) — Input Forms task.

The script reads data from an Excel file and automatically fills a web form across 10 rounds. Since form fields change position after each submission, fields are located by **label** rather than by position or order - ensuring correct input regardless of element layout.

## Setup & Run

```bash
python -m venv .venv
.venv\Scripts\activate
pip install -r requirements.txt
playwright install chromium
python rpa_challenge.py
```