# DRRT Loss Calculator

A web application for calculating recognized losses from custodian confirmation data for securities litigation at DRRT.

## Features

- Upload Excel files containing transaction data
- Automatic loss calculation based on purchase and sale prices
- Support for different case types (Twitter, Kraft, etc.)
- Download processed files with calculated losses
- Web interface built with FastAPI and HTML/JS

## Tech Stack

- **Backend**: Python, FastAPI
- **Data Processing**: Pandas
- **Frontend**: HTML, JavaScript
- **Styling**: CSS
- **Testing**: Pytest

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

## Loss Calculation

Recognized Loss = max(0, (Purchase Price - Sale Price) * Quantity)

- Only positive losses are recognized
- If sale_price is missing, assumes no sale (loss = 0)
- Quantity defaults to 1 if missing

## API Endpoints

- `GET /`: Home page
- `POST /upload`: Upload and process file
- `GET /download/{filename}`: Download processed file