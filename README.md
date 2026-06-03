# Health Prediction Application

A professional web application for managing patient blood test records and generating AI-powered health risk predictions using Google Gemini.

## Screenshots
 Patient Records 
<img width="1905" height="859" alt="image" src="https://github.com/user-attachments/assets/6671f6c1-a545-41c1-a43d-f49806ad9c6c" />

The Health Prediction Application allows healthcare staff to:
- Manage patient records (create, view, update, delete)
- Search patients by name or email
- Automatically generate AI health risk predictions from blood test values (Glucose, Haemoglobin, Cholesterol)
- View a dashboard with summary statistics and recent predictions
All data is stored locally in a SQLite database. Predictions are generated via the Google Gemini API and saved alongside each patient record.
Features
- **Dashboard** — total patient count, recent patients table, latest AI predictions
- **Add Patient** — form with full validation and instant AI prediction on submit
- **Patient Records** — searchable table with edit and delete functionality
- **Input Validation** — name, email, date of birth, and numeric blood value checks
- **AI Prediction** — Gemini API generates a short health risk summary (under 40 words)
- **Graceful Error Handling** — fallback message if the API is unavailable
- **Medical Disclaimer** — displayed alongside every AI-generated remark

