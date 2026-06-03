# Health Prediction Application

A professional web application for managing patient blood test records and generating AI-powered health risk predictions using Google Gemini.

---

## Project Overview

The Health Prediction Application allows healthcare staff to:
- Manage patient records (create, view, update, delete)
- Search patients by name or email
- Automatically generate AI health risk predictions from blood test values (Glucose, Haemoglobin, Cholesterol)
- View a dashboard with summary statistics and recent predictions

All data is stored locally in a SQLite database. Predictions are generated via the Google Gemini API and saved alongside each patient record.

---

## Features

- **Dashboard** — total patient count, recent patients table, latest AI predictions
- **Add Patient** — form with full validation and instant AI prediction on submit
- **Patient Records** — searchable table with edit and delete functionality
- **Input Validation** — name, email, date of birth, and numeric blood value checks
- **AI Prediction** — Gemini API generates a short health risk summary (under 40 words)
- **Graceful Error Handling** — fallback message if the API is unavailable
- **Medical Disclaimer** — displayed alongside every AI-generated remark

---

## Technology Stack

| Technology | Purpose |
|---|---|
| Python 3.9+ | Core language |
| Streamlit | Web UI framework |
| SQLite | Local database |
| Google Gemini API | AI health predictions |
| python-dotenv | Environment variable management |
| Hypothesis | Property-based testing |
| pytest | Test runner |

---

## Installation

### 1. Clone the repository

```bash
git clone <repository-url>
cd health_prediction_app
```

### 2. Create a virtual environment (recommended)

```bash
python -m venv venv
# Windows
venv\Scripts\activate
# macOS / Linux
source venv/bin/activate
```

### 3. Install dependencies

```bash
pip install -r requirements.txt
```

### 4. Configure environment variables

Copy the example environment file and add your API key:

```bash
cp .env.example .env
```

Open `.env` and set your Gemini API key:

```
GEMINI_API_KEY=your_actual_api_key_here
```

---

## Gemini API Setup

1. Go to [Google AI Studio](https://aistudio.google.com/)
2. Sign in with your Google account
3. Click **Get API Key** → **Create API Key**
4. Copy the key and paste it into your `.env` file as `GEMINI_API_KEY`

> The free tier is sufficient for development and testing.

---

## Running the Application

From the `health_prediction_app/` directory (or the project root):

```bash
# From the project root
streamlit run health_prediction_app/app.py

# Or from inside health_prediction_app/
streamlit run app.py
```

The app will open automatically in your browser at `http://localhost:8501`.

---

## Running Tests

From the project root:

```bash
pytest tests/
```

The test suite includes:
- Unit tests for database CRUD operations
- Unit tests for the AI service (mocked API calls)
- Property-based tests (Hypothesis) covering 11 correctness properties

---

## Project Structure

```
health_prediction_app/
├── app.py              # Streamlit UI — pages, forms, navigation
├── database.py         # SQLite CRUD layer
├── ai_service.py       # Google Gemini API integration
├── requirements.txt    # Pinned dependencies
├── README.md           # This file
├── .env.example        # Environment variable template
└── patients.db         # SQLite database (auto-created on first run)

tests/
├── test_database.py    # Database unit + property tests
├── test_ai_service.py  # AI service unit + property tests
└── test_validator.py   # Validator property tests
```

---

## Screenshots

> Add screenshots of the running application here.

| Page | Description |
|---|---|
| Dashboard | Summary stats and recent predictions |
| Add Patient | Patient form with AI prediction result |
| Patient Records | Searchable table with edit/delete |

---

## Disclaimer

> This application is for demonstration and educational purposes only. AI-generated health predictions are **not a substitute for professional medical advice**. Always consult a qualified healthcare professional for medical decisions.
