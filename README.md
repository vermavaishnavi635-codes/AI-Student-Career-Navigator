
# 🎓 AI-Powered Student Career Navigator

A web-based career guidance platform designed to help students understand their interests, evaluate their skills, explore suitable career options, identify skill gaps, and follow a structured learning roadmap.

## 📌 Project Overview

AI-Powered Student Career Navigator is a Flask-based web application that combines career assessment, machine learning-based career recommendations, skill gap analysis, and personalized learning roadmaps.

The platform helps students make more informed career decisions based on their assessment responses and self-reported skills.

## ✨ Features

### 1. Student Registration & Login
- Student account registration.
- Secure login and logout.
- Personalized student dashboard.

### 2. Career Assessment
- 15 interest-based assessment questions.
- Collects student responses.
- Generates career assessment results.

### 3. Career Recommendations
- Random Forest machine learning classifier.
- Top 3 career recommendations.
- Model-based career ranking.

### 4. Skills Assessment
- Students can evaluate their current skills.
- Beginner, Intermediate and Advanced skill levels.

### 5. Skill Gap Analysis
- Compares current skill levels with target levels.
- Identifies skills requiring improvement.
- Displays career readiness percentage.

### 6. Learning Roadmap
- Structured learning topics.
- Skill-based learning guidance.
- Practical learning steps.

## 🛠️ Technology Stack

| Category | Technologies |
|---|---|
| Programming Language | Python |
| Backend | Flask |
| Frontend | HTML, CSS, JavaScript |
| Database | SQLite |
| ORM | Flask-SQLAlchemy |
| Machine Learning | Scikit-learn |
| ML Algorithm | Random Forest Classifier |
| Data Processing | Pandas, NumPy |
| Model Storage | Joblib |
| Development Tool | VS Code |
| Version Control | Git & GitHub |

## 📂 Project Structure

```text
AI-Student-Career-Navigator/
│
├── main.py
├── database.py
├── models.py
├── career_engine.py
├── career_model.pkl
├── career_encoder.pkl
├── career_feature_info.pkl
├── requirements.txt
├── README.md
│
├── data/
│   ├── career_dataset.csv
│   └── careers.json
│
├── templates/
│   ├── index.html
│   ├── register.html
│   ├── login.html
│   ├── dashboard.html
│   ├── assessment.html
│   ├── result.html
│   ├── skills.html
│   ├── skill_result.html
│   └── learning_roadmap.html
│
└── static/
    ├── style.css
    └── script.js
```

## ⚙️ Installation & Setup

### Step 1: Clone the Repository

```bash
git clone https://github.com/vermavaishnavi635-codes/AI-Student-Career-Navigator.git
```

### Step 2: Open the Project Folder

```bash
cd AI-Student-Career-Navigator
```

### Step 3: Create Virtual Environment

```bash
python -m venv .venv
```

### Step 4: Activate Virtual Environment

For Windows PowerShell:

```powershell
.\.venv\Scripts\Activate.ps1
```

### Step 5: Install Dependencies

```bash
pip install -r requirements.txt
```

### Step 6: Run the Application

```bash
python main.py
```

### Step 7: Open in Browser

```text
http://127.0.0.1:5000/
```

## 🤖 Machine Learning Implementation

The project uses a Random Forest Classifier for career recommendations.

### Input Features

- Python
- SQL
- Problem Solving
- Data Structures
- Web Development
- Creativity
- Communication
- Analytical Thinking

### Career Categories

The current training dataset contains five career categories:

1. Data Scientist
2. Software Developer
3. Web Developer
4. Graphic Designer
5. Business Analyst

### Dataset Information

| Parameter | Value |
|---|---:|
| Total Records | 44 |
| Input Features | 8 |
| Career Categories | 5 |
| Evaluation | 5-Fold Stratified Cross-Validation |

**Important:** The current dataset is small and synthetic. Model evaluation scores should not be interpreted as real-world career success probabilities.

## 🔄 Application Workflow

1. Student registers and logs in.
2. Student completes the career assessment.
3. Assessment responses are saved in SQLite.
4. Student completes the skills assessment.
5. Random Forest generates career recommendations.
6. The system displays skill gaps and readiness feedback.
7. Student views the learning roadmap.

## 🚀 Future Enhancements

The following features are planned for future development:

- Expand the assessment to 33 questions.
- Integrate Gemini AI API.
- Dynamic career discovery beyond predefined career categories.
- AI-powered career counselling.
- Career comparison functionality.
- AI-generated personalized learning roadmaps.
- Expanded career knowledge base.

These features are planned and are not part of the current implementation.

## 🔐 Data & Security Notes

- Student records are stored in a local SQLite database.
- Keep database files and personal credentials private.
- Do not commit passwords, API keys or secret configuration files to GitHub.
- Use environment variables for future API integrations.

## 👩‍💻 Author

**Project:** AI-Powered Student Career Navigator

**Developer:** Vaishnavi Verma

## 📄 License

This project was developed for academic and educational purposes.
