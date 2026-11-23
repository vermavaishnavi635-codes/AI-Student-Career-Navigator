from flask_login import UserMixin
from database import db


class Student(UserMixin, db.Model):

    # Database table name
    __tablename__ = "students"

    # Unique student ID
    id = db.Column(db.Integer, primary_key=True)

    # Student information
    name = db.Column(db.String(100), nullable=False)

    email = db.Column(
        db.String(120),
        unique=True,
        nullable=False
    )

    # Stores hashed password, not original password
    password = db.Column(db.String(255), nullable=False)

    # Academic information
    age = db.Column(db.Integer, nullable=True)

    education = db.Column(db.String(100), nullable=True)

    course = db.Column(db.String(100), nullable=True)

    # Student interests
    interests = db.Column(db.Text, nullable=True)

    # Account creation time
    created_at = db.Column(
        db.DateTime,
        server_default=db.func.current_timestamp()
    )

    def __repr__(self):
        return f"<Student {self.name}>"


class AssessmentResult(db.Model):
    __tablename__ = "assessment_results"

    id = db.Column(db.Integer, primary_key=True)

    student_id = db.Column(
        db.Integer,
        db.ForeignKey("students.id"),
        nullable=False
    )

    answers = db.Column(db.Text, nullable=False)
    scores = db.Column(db.Text, nullable=True)
    recommended_career = db.Column(db.String(100), nullable=True)

    created_at = db.Column(
        db.DateTime,
        server_default=db.func.current_timestamp()
    )


class SkillAssessment(db.Model):
    __tablename__ = "skill_assessments"

    id = db.Column(db.Integer, primary_key=True)

    student_id = db.Column(
        db.Integer,
        db.ForeignKey("students.id"),
        nullable=False
    )

    skills = db.Column(db.Text, nullable=False)

    created_at = db.Column(
        db.DateTime,
        server_default=db.func.current_timestamp()
    )
