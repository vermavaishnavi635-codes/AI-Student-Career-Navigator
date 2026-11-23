
# AI-Powered Student Career Navigator

An AI-powered web application that helps students explore suitable career paths based on their interests and skills.

## Project Overview

The AI-Powered Student Career Navigator is a web-based application developed using Python and Flask. It helps students assess their interests, evaluate their current skills, identify skill gaps, and explore career-related learning roadmaps.

## Features

- Student Registration and Login
- Interest-Based Career Assessment
- Rule-Based Career Recommendations
- ML-Based Career Prediction
- Skill Assessment
- Skill Gap Analysis
- Personalized Learning Roadmap
- Student Dashboard

## Technology Stack

**Frontend**
- HTML
- CSS
- JavaScript
- Bootstrap (if used)

**Backend**
- Python
- Flask

**Database**
- SQLite
- Flask-SQLAlchemy

**Machine Learning**
- Pandas
- NumPy
- Scikit-learn
- Random Forest Classifier
- Joblib

## Project Structure

```text
AI_Student_Career_Navigator/
├── main.py
├── database.py
├── models.py
├── career_engine.py
├── requirements.txt
├── career_model.pkl
├── career_encoder.pkl
├── templates/
├── static/
└── data/
    ├── career_dataset.csv
    └── careers.json
```

## Installation and Setup

1. Clone the repository:

```bash
git clone YOUR_GITHUB_REPOSITORY_URL
```

2. Open the project folder:

```bash
cd AI_Student_Career_Navigator
```

3. Create a virtual environment:

```bash
python -m venv .venv
```

4. Activate the virtual environment on Windows:

```powershell
.venv\Scripts\Activate.ps1
```

5. Install dependencies:

```bash
pip install -r requirements.txt
```

6. Run the application:

```bash
python main.py
```

7. Open in your browser:

```text
http://127.0.0.1:5000/
```

## Machine Learning Note

The current machine learning model uses a small synthetic dataset for academic demonstration. Its reported test accuracy should not be considered evidence of real-world career prediction performance.

## Future Enhancements

- Improve the ML model using a larger, validated dataset.
- Add more career paths and skill categories.
- Improve personalized career guidance.
- Enhance the user interface.

## Author

Student Project  
Pranveer Singh Institute of Technology, Kanpur
