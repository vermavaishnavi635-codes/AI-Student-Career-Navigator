
import os
import json

from flask import (
    Flask, render_template, request,
    redirect, url_for, flash
)

from werkzeug.security import (
    generate_password_hash, check_password_hash
)

from flask_login import (
    LoginManager, login_user, login_required,
    logout_user, current_user
)

from database import db
from models import Student, AssessmentResult, SkillAssessment
from career_engine import predict_top_careers


# ==========================================
# FLASK CONFIGURATION
# ==========================================

app = Flask(__name__)

BASE_DIR = os.path.abspath(os.path.dirname(__file__))

app.config["SQLALCHEMY_DATABASE_URI"] = (
    "sqlite:///" + os.path.join(BASE_DIR, "career_navigator.db")
)

app.config["SQLALCHEMY_TRACK_MODIFICATIONS"] = False

app.config["SECRET_KEY"] = os.environ.get(
    "SECRET_KEY",
    "development-only-change-this-key"
)

db.init_app(app)


# ==========================================
# LOGIN MANAGER
# ==========================================

login_manager = LoginManager()
login_manager.init_app(app)

login_manager.login_view = "login"
login_manager.login_message = "Please log in to access this page."


@login_manager.user_loader
def load_user(user_id):
    return db.session.get(Student, int(user_id))


# ==========================================
# HOMEPAGE
# ==========================================

@app.route("/")
def home():
    return render_template("index.html")


# ==========================================
# REGISTRATION
# ==========================================

@app.route("/register", methods=["GET", "POST"])
def register():

    if request.method == "GET":
        return render_template("register.html")

    name = request.form.get("name", "").strip()
    email = request.form.get("email", "").strip().lower()
    password = request.form.get("password", "")
    confirm_password = request.form.get("confirm_password", "")

    age_input = request.form.get("age", "").strip()
    education = request.form.get("education", "").strip()
    course = request.form.get("course", "").strip()
    interests = request.form.get("interests", "").strip()

    if not name or not email or not password:
        flash("Name, email and password are required.", "error")
        return redirect(url_for("register"))

    if len(name) > 100 or len(email) > 120:
        flash("Name or email is too long.", "error")
        return redirect(url_for("register"))

    if len(education) > 100 or len(course) > 100:
        flash("Education or course is too long.", "error")
        return redirect(url_for("register"))

    if "@" not in email or "." not in email.split("@")[-1]:
        flash("Please enter a valid email address.", "error")
        return redirect(url_for("register"))

    if len(password) < 8:
        flash("Password must contain at least 8 characters.", "error")
        return redirect(url_for("register"))

    if password != confirm_password:
        flash("Passwords do not match.", "error")
        return redirect(url_for("register"))

    age = None

    if age_input:
        try:
            age = int(age_input)
        except ValueError:
            flash("Age must be a valid number.", "error")
            return redirect(url_for("register"))

        if age < 13 or age > 100:
            flash("Please enter an age between 13 and 100.", "error")
            return redirect(url_for("register"))

    existing_student = Student.query.filter_by(email=email).first()

    if existing_student:
        flash("This email is already registered.", "error")
        return redirect(url_for("register"))

    new_student = Student(
        name=name,
        email=email,
        password=generate_password_hash(password),
        age=age,
        education=education or None,
        course=course or None,
        interests=interests or None
    )

    try:
        db.session.add(new_student)
        db.session.commit()

    except Exception:
        db.session.rollback()
        app.logger.exception("Registration failed")
        flash("Registration failed. Please try again.", "error")
        return redirect(url_for("register"))

    flash("Account created successfully!", "success")
    return redirect(url_for("register"))


# ==========================================
# LOGIN
# ==========================================

@app.route("/login", methods=["GET", "POST"])
def login():

    if current_user.is_authenticated:
        return redirect(url_for("dashboard"))

    if request.method == "GET":
        return render_template("login.html")

    email = request.form.get("email", "").strip().lower()
    password = request.form.get("password", "")

    student = Student.query.filter_by(email=email).first()

    if student and check_password_hash(student.password, password):
        login_user(student)
        flash("Login successful!", "success")
        return redirect(url_for("dashboard"))

    flash("Invalid email or password.", "error")
    return redirect(url_for("login"))


# ==========================================
# DASHBOARD
# ==========================================

@app.route("/dashboard")
@login_required
def dashboard():
    return render_template(
        "dashboard.html",
        student=current_user
    )


# ==========================================
# LOGOUT
# ==========================================

@app.route("/logout")
@login_required
def logout():

    logout_user()
    flash("You have been logged out.", "success")

    return redirect(url_for("login"))


# ==========================================
# CAREER ASSESSMENT QUESTIONS
# ==========================================

CAREER_QUESTIONS = [

    {
        "id": 1,
        "question": "Which activity do you enjoy most?",
        "options": [
            {"label": "Solving mathematical problems", "value": "technology"},
            {"label": "Designing creative things", "value": "design"},
            {"label": "Understanding business and markets", "value": "business"},
            {"label": "Helping and teaching people", "value": "people"}
        ]
    },
    {
        "id": 2,
        "question": "Which subject interests you most?",
        "options": [
            {"label": "Computer Science", "value": "technology"},
            {"label": "Arts and Design", "value": "design"},
            {"label": "Economics and Commerce", "value": "business"},
            {"label": "Psychology and Biology", "value": "people"}
        ]
    },
    {
        "id": 3,
        "question": "What type of problems do you like solving?",
        "options": [
            {"label": "Technical problems", "value": "technology"},
            {"label": "Creative problems", "value": "design"},
            {"label": "Business problems", "value": "business"},
            {"label": "People-related problems", "value": "people"}
        ]
    },
    {
        "id": 4,
        "question": "Which task sounds most interesting?",
        "options": [
            {"label": "Building an application", "value": "technology"},
            {"label": "Creating a website design", "value": "design"},
            {"label": "Planning a business", "value": "business"},
            {"label": "Guiding a team", "value": "people"}
        ]
    },
    {
        "id": 5,
        "question": "Which skill would you like to improve?",
        "options": [
            {"label": "Programming", "value": "technology"},
            {"label": "Creativity", "value": "design"},
            {"label": "Leadership", "value": "business"},
            {"label": "Communication", "value": "people"}
        ]
    },
    {
        "id": 6,
        "question": "Which work environment do you prefer?",
        "options": [
            {"label": "Technology company", "value": "technology"},
            {"label": "Creative studio", "value": "design"},
            {"label": "Business organization", "value": "business"},
            {"label": "Educational or social organization", "value": "people"}
        ]
    },
    {
        "id": 7,
        "question": "What do you enjoy doing in your free time?",
        "options": [
            {"label": "Learning technology", "value": "technology"},
            {"label": "Drawing or editing", "value": "design"},
            {"label": "Exploring business ideas", "value": "business"},
            {"label": "Helping others", "value": "people"}
        ]
    },
    {
        "id": 8,
        "question": "Which project would you choose?",
        "options": [
            {"label": "Building an AI application", "value": "technology"},
            {"label": "Designing a mobile app", "value": "design"},
            {"label": "Creating a startup plan", "value": "business"},
            {"label": "Organizing a learning program", "value": "people"}
        ]
    },
    {
        "id": 9,
        "question": "Which strength describes you best?",
        "options": [
            {"label": "Analytical thinking", "value": "technology"},
            {"label": "Imagination", "value": "design"},
            {"label": "Decision making", "value": "business"},
            {"label": "Empathy", "value": "people"}
        ]
    },
    {
        "id": 10,
        "question": "Which tool would you prefer to work with?",
        "options": [
            {"label": "Python or other programming tools", "value": "technology"},
            {"label": "Figma or Photoshop", "value": "design"},
            {"label": "Excel or business tools", "value": "business"},
            {"label": "Teaching and communication tools", "value": "people"}
        ]
    },
    {
        "id": 11,
        "question": "How do you approach a difficult task?",
        "options": [
            {"label": "Break it into logical steps", "value": "technology"},
            {"label": "Try a creative approach", "value": "design"},
            {"label": "Plan resources and priorities", "value": "business"},
            {"label": "Discuss it with others", "value": "people"}
        ]
    },
    {
        "id": 12,
        "question": "Which achievement would make you happiest?",
        "options": [
            {"label": "Creating useful technology", "value": "technology"},
            {"label": "Making something visually attractive", "value": "design"},
            {"label": "Growing a successful business", "value": "business"},
            {"label": "Making a positive difference to people", "value": "people"}
        ]
    },
    {
        "id": 13,
        "question": "Which role sounds most appealing?",
        "options": [
            {"label": "Software Developer", "value": "technology"},
            {"label": "UI/UX Designer", "value": "design"},
            {"label": "Business Analyst", "value": "business"},
            {"label": "Teacher or Trainer", "value": "people"}
        ]
    },
    {
        "id": 14,
        "question": "What motivates you most?",
        "options": [
            {"label": "Learning and innovation", "value": "technology"},
            {"label": "Creating new ideas", "value": "design"},
            {"label": "Achieving business goals", "value": "business"},
            {"label": "Supporting others", "value": "people"}
        ]
    },
    {
        "id": 15,
        "question": "What kind of career would you prefer?",
        "options": [
            {"label": "Technology and engineering", "value": "technology"},
            {"label": "Creative and design", "value": "design"},
            {"label": "Management and business", "value": "business"},
            {"label": "Education and people development", "value": "people"}
        ]
    }

]


# ==========================================
# CAREER ASSESSMENT
# ==========================================

@app.route("/assessment", methods=["GET", "POST"])
@login_required
def assessment():

    if request.method == "POST":

        answers = {}

        for question in CAREER_QUESTIONS:

            answer = request.form.get(f"q{question['id']}")

            valid_options = [
                option["value"]
                for option in question["options"]
            ]

            if answer not in valid_options:
                flash("Please answer all questions correctly.", "error")
                return redirect(url_for("assessment"))

            answers[f"q{question['id']}"] = answer

        categories = [
            "technology", "design", "business", "people"
        ]

        counts = {
            category: 0
            for category in categories
        }

        for answer in answers.values():
            counts[answer] += 1

        total_questions = len(CAREER_QUESTIONS)

        scores = {
            category.title(): round(
                (counts[category] / total_questions) * 100,
                2
            )
            for category in categories
        }

        recommended_career = max(
            counts,
            key=counts.get
        ).title()

        result = AssessmentResult(
            student_id=current_user.id,
            answers=json.dumps(answers),
            scores=json.dumps(scores),
            recommended_career=recommended_career
        )

        try:
            db.session.add(result)
            db.session.commit()

        except Exception:
            db.session.rollback()
            app.logger.exception("Assessment saving failed")
            flash("Unable to save assessment. Please try again.", "error")
            return redirect(url_for("assessment"))

        flash("Assessment submitted successfully!", "success")

        return redirect(url_for("assessment_result"))

    return render_template(
        "assessment.html",
        questions=CAREER_QUESTIONS
    )


# ==========================================
# CAREER ASSESSMENT RESULT
# ==========================================

@app.route("/assessment-result")
@login_required
def assessment_result():

    result = AssessmentResult.query.filter_by(
        student_id=current_user.id
    ).order_by(
        AssessmentResult.id.desc()
    ).first()

    if result is None:
        flash("Please complete your assessment first.", "error")
        return redirect(url_for("assessment"))

    scores = json.loads(result.scores)

    return render_template(
        "result.html",
        scores=scores,
        recommended_career=result.recommended_career
    )


# ==========================================
# SKILLS ASSESSMENT
# ==========================================

@app.route("/skills-assessment", methods=["GET", "POST"])
@login_required
def skills_assessment():

    result = AssessmentResult.query.filter_by(
        student_id=current_user.id
    ).order_by(
        AssessmentResult.id.desc()
    ).first()

    if result is None:
        flash("Please complete career assessment first.", "error")
        return redirect(url_for("assessment"))

    career_skills = {

        "Technology": [
            "Python", "SQL", "Problem Solving",
            "Data Structures", "Web Development"
        ],

        "Design": [
            "Creativity", "UI/UX Design",
            "Graphic Design", "Figma",
            "Visual Communication"
        ],

        "Business": [
            "Business Analysis", "Communication",
            "Excel", "Problem Solving", "Decision Making"
        ],

        "People": [
            "Communication", "Leadership",
            "Teamwork", "Teaching", "Problem Solving"
        ]

    }

    recommended_career = result.recommended_career

    skills = career_skills.get(
        recommended_career,
        career_skills["Technology"]
    )

    if request.method == "POST":

        student_skills = {}

        for skill in skills:

            level = request.form.get(skill)

            if level not in [
                "beginner", "intermediate", "advanced"
            ]:
                flash("Please select a level for every skill.", "error")
                return redirect(url_for("skills_assessment"))

            student_skills[skill] = level

        skill_result = SkillAssessment(
            student_id=current_user.id,
            skills=json.dumps(student_skills)
        )

        try:
            db.session.add(skill_result)
            db.session.commit()

        except Exception:
            db.session.rollback()
            app.logger.exception("Skills assessment saving failed")
            flash("Unable to save skills. Please try again.", "error")
            return redirect(url_for("skills_assessment"))

        flash("Skills assessment submitted successfully!", "success")
        return redirect(url_for("skill_result"))

    return render_template(
        "skills.html",
        skills=skills,
        recommended_career=recommended_career
    )


# ==========================================
# SKILL RESULT + TOP 3 ML RECOMMENDATIONS
# ==========================================

@app.route("/skill-result")
@login_required
def skill_result():

    saved_skills = SkillAssessment.query.filter_by(
        student_id=current_user.id
    ).order_by(
        SkillAssessment.id.desc()
    ).first()

    if saved_skills is None:
        flash("Please complete skills assessment first.", "error")
        return redirect(url_for("skills_assessment"))

    career_result = AssessmentResult.query.filter_by(
        student_id=current_user.id
    ).order_by(
        AssessmentResult.id.desc()
    ).first()

    if career_result is None:
        flash("Please complete career assessment first.", "error")
        return redirect(url_for("assessment"))

    student_skills = json.loads(saved_skills.skills)

    # ML recommendations
    try:
        ml_recommendations = predict_top_careers(
            student_skills,
            top_n=3
        )
    except Exception:
        app.logger.exception("ML recommendation failed")
        ml_recommendations = []

    # Rule-based recommendation
    recommended_career = career_result.recommended_career

    required_skill_levels = {

        "Technology": {
            "Python": "intermediate",
            "SQL": "intermediate",
            "Problem Solving": "advanced",
            "Data Structures": "intermediate",
            "Web Development": "intermediate"
        },

        "Design": {
            "Creativity": "advanced",
            "UI/UX Design": "intermediate",
            "Graphic Design": "intermediate",
            "Figma": "intermediate",
            "Visual Communication": "intermediate"
        },

        "Business": {
            "Business Analysis": "intermediate",
            "Communication": "advanced",
            "Excel": "intermediate",
            "Problem Solving": "advanced",
            "Decision Making": "intermediate"
        },

        "People": {
            "Communication": "advanced",
            "Leadership": "intermediate",
            "Teamwork": "advanced",
            "Teaching": "intermediate",
            "Problem Solving": "intermediate"
        }

    }

    level_scores = {
        "beginner": 1,
        "intermediate": 2,
        "advanced": 3
    }

    required_levels = required_skill_levels.get(
        recommended_career,
        required_skill_levels["Technology"]
    )

    skill_gaps = []
    readiness_scores = []

    for skill, current_level in student_skills.items():

        required_level = required_levels.get(
            skill, "intermediate"
        )

        current_score = level_scores.get(current_level, 1)
        required_score = level_scores[required_level]

        if current_score < required_score:
            status = "Needs Improvement"
        elif current_score == required_score:
            status = "Meets Target"
        else:
            status = "Above Target"

        readiness_scores.append(
            min(current_score / required_score, 1) * 100
        )

        skill_gaps.append({
            "name": skill,
            "current_level": current_level,
            "required_level": required_level,
            "status": status
        })

    readiness = round(
        sum(readiness_scores) / len(readiness_scores)
    ) if readiness_scores else 0

    return render_template(
        "skill_result.html",
        skills=student_skills,
        recommended_career=recommended_career,
        skill_gaps=skill_gaps,
        readiness=readiness,
        ml_recommendations=ml_recommendations
    )


# ==========================================
# LEARNING ROADMAP
# ==========================================

@app.route("/learning-roadmap")
@login_required
def learning_roadmap():

    saved_skills = SkillAssessment.query.filter_by(
        student_id=current_user.id
    ).order_by(
        SkillAssessment.id.desc()
    ).first()

    if saved_skills is None:
        flash("Please complete skills assessment first.", "error")
        return redirect(url_for("skills_assessment"))

    student_skills = json.loads(saved_skills.skills)

    roadmap_data = {

        "Python": {
            "topics": [
                "Python Basics", "Functions", "OOP", "File Handling"
            ],
            "project": "Build a Student Management System",
            "duration": "7 Days"
        },

        "SQL": {
            "topics": [
                "SELECT", "WHERE", "JOINS", "GROUP BY"
            ],
            "project": "Build a Student Database",
            "duration": "5 Days"
        },

        "Problem Solving": {
            "topics": [
                "Logic Building", "Basic Algorithms", "Practice Problems"
            ],
            "project": "Solve 20 Coding Problems",
            "duration": "7 Days"
        },

        "Data Structures": {
            "topics": [
                "Arrays", "Lists", "Stacks", "Queues"
            ],
            "project": "Build a Data Structures Practice Program",
            "duration": "7 Days"
        },

        "Web Development": {
            "topics": [
                "HTML", "CSS", "JavaScript", "Flask"
            ],
            "project": "Build a Personal Portfolio Website",
            "duration": "7 Days"
        }

    }

    roadmap = []

    for skill, level in student_skills.items():

        if level in ["beginner", "intermediate"]:

            if skill in roadmap_data:

                roadmap.append({
                    "skill": skill,
                    "current_level": level.title(),
                    "topics": roadmap_data[skill]["topics"],
                    "project": roadmap_data[skill]["project"],
                    "duration": roadmap_data[skill]["duration"]
                })

    return render_template(
        "learning_roadmap.html",
        roadmap=roadmap
    )


# ==========================================
# RUN APPLICATION
# ==========================================

if __name__ == "__main__":

    with app.app_context():
        db.create_all()

    app.run(debug=True)
