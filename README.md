# AI-Powered Securities Loss Recovery System

A web-based application that automates the calculation of recognized losses from financial transaction data for securities litigation and settlement claims.

This system processes client transaction datasets, applies rule-based logic, and generates structured financial summaries to support loss recovery analysis.

---

## 🚀 Features

- Upload Excel files containing transaction data  
- Automatic case detection (Twitter / Kraft settlements)  
- Rule-based loss calculation with eligibility conditions  
- Summary metrics:
  - Total Recognized Loss  
  - Total Investment  
  - Total Sale  
  - Eligible Records  
- Download processed files with calculated results  
- Clean web interface built with FastAPI and HTML/JS  

---

## 🛠 Tech Stack

- Backend Python, FastAPI  
- Data Processing: Pandas  
- Frontend: HTML, JavaScript  
- Styling: CSS  
- Testing: Pytest  

---

## Installation

1. Clone the repository
2. Create virtual environment: `python -m venv .venv`
3. Activate venv: `.venv\Scripts\activate` (Windows)
4. Install dependencies: `pip install -r requirements.txt`

## Usage

1. Run the application: `python run.py`
2. Open browser to `http://127.0.0.1:8000`
3. Upload an Excel file with columns: `purchase_price`, `sale_price` (optional), `quantity` (optional)
4. Download the processed file with `recognized_loss` column

## Project Structure

```
drrt-loss-calculator/
├── app/
│   ├── main.py              # FastAPI app
│   ├── routes/
│   │   └── upload.py        # Upload and download routes
│   ├── services/
│   │   ├── loss_calculator.py  # Main processing logic
│   │   ├── twitter_logic.py    # Twitter case logic
│   │   └── kraft_logic.py      # Kraft case logic
│   ├── models/
│   │   └── schemas.py       # Data schemas (empty)
│   ├── utils/
│   │   ├── file_handler.py  # File utilities
│   │   └── validators.py    # Data validation
│   └── config/
│       └── settings.py      # Configuration (empty)
├── data/
│   ├── input/               # Input files
│   └── output/              # Processed files
├── static/
│   ├── css/
│   └── js/
│       └── script.js        # Frontend JS
├── templates/
│   └── index.html           # Main page
├── tests/
│   └── test_logic.py        # Unit tests
├── prompts/
│   └── ai_prompts.md        # AI prompts (empty)
├── requirements.txt          # Dependencies
├── run.py                   # Entry point
└── README.md
```

---

## 📊 Output Metrics

The system generates:

- Recognized Loss
- Total Investment
- Total Sale Value
- Eligible Records Count

## 🧠 Loss Calculation Logic

The system uses rule-based logic including:

- Class period eligibility checks
- Pre/Post disclosure handling
- Capped loss scenarios
- Handling of missing or incomplete data

> Note: Actual settlement calculations may involve complex allocation tables. This implementation provides a simplified, extendable model for demonstration.

---

## 🔗 API Endpoints

- `GET /` → Web UI
- `POST /upload` → Upload and process file
- `GET /download/{filename}` → Download result

---

## 💡 Key Highlights

- Designed for financial data processing workflows
- Handles both row-level and aggregated datasets
- Modular architecture for extending new settlement cases
- Focused on automation, accuracy, and usability

---

## 📌 Future Improvements

- Integration with real settlement allocation tables
- Advanced validation and reporting
- Enhanced UI with data preview
