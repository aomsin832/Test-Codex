# Cyber Risk Register Dashboard

A simple, beginner-friendly Streamlit dashboard for viewing a fictional cyber risk register. The project uses **only synthetic data** and does not connect to external services or APIs.

## What the dashboard includes

- 10 fictional cybersecurity risks
- Summary cards for open, Critical/High, and overdue risks
- Severity and status filters
- A full, filterable risk table
- A bar chart of risks by severity

An **open risk** is any risk whose status is not `Closed`. An **overdue risk** is open and has a due date before the current date.

## Run locally

1. Make sure Python 3.10 or newer is installed.
2. Create and activate a virtual environment:

   ```bash
   python -m venv .venv
   source .venv/bin/activate
   ```

   On Windows PowerShell, activate it with `.venv\Scripts\Activate.ps1` instead.

3. Install the dependencies:

   ```bash
   pip install -r requirements.txt
   ```

4. Start the dashboard:

   ```bash
   streamlit run app.py
   ```

5. Open the local address printed by Streamlit (usually `http://localhost:8501`).

## Project structure

```text
.
├── app.py             # Streamlit dashboard
├── data/
│   └── risks.csv      # Synthetic risk register
├── requirements.txt   # Python dependencies
└── README.md          # Setup and usage instructions
```

> **Note:** The people, departments, situations, and records in this project are entirely fictional and are intended only for demonstration and learning.
