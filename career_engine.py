import pandas as pd
from sklearn.model_selection import train_test_split
from sklearn.ensemble import RandomForestClassifier
from sklearn.preprocessing import LabelEncoder
from sklearn.metrics import accuracy_score
import joblib
import os

# Dataset path
BASE_DIR = os.path.dirname(os.path.abspath(__file__))
DATASET_PATH = os.path.join(BASE_DIR, "data", "career_dataset.csv")
MODEL_PATH = os.path.join(BASE_DIR, "career_model.pkl")
ENCODER_PATH = os.path.join(BASE_DIR, "career_encoder.pkl")

# Load dataset
data = pd.read_csv(DATASET_PATH)

# Separate features and target
X = data.drop("career", axis=1)
y = data["career"]

# Encode career labels
encoder = LabelEncoder()
y_encoded = encoder.fit_transform(y)

# Split dataset
X_train, X_test, y_train, y_test = train_test_split(
    X,
    y_encoded,
    test_size=0.2,
    random_state=42,
    stratify=y_encoded
)

# Train ML model
model = RandomForestClassifier(
    n_estimators=100,
    random_state=42
)

model.fit(X_train, y_train)

# Evaluate model
predictions = model.predict(X_test)
accuracy = accuracy_score(y_test, predictions)

# Save model
joblib.dump(model, MODEL_PATH)
joblib.dump(encoder, ENCODER_PATH)

print("ML Model trained successfully!")
print("Model Accuracy:", round(accuracy * 100, 2), "%")
print("Model saved successfully!")


# =========================
# CAREER PREDICTION FUNCTION
# =========================

def predict_career(student_skills):

    model = joblib.load(MODEL_PATH)
    encoder = joblib.load(ENCODER_PATH)

    level_mapping = {
        "beginner": 1,
        "intermediate": 3,
        "advanced": 5
    }

    features = {
        "python": 1,
        "sql": 1,
        "problem_solving": 1,
        "data_structures": 1,
        "web_development": 1,
        "creativity": 1,
        "communication": 1,
        "analytical_thinking": 1
    }

    skill_mapping = {
        "Python": "python",
        "SQL": "sql",
        "Problem Solving": "problem_solving",
        "Data Structures": "data_structures",
        "Web Development": "web_development",
        "Creativity": "creativity",
        "Communication": "communication",
        "Analytical Thinking": "analytical_thinking",
        "UI/UX Design": "creativity",
        "Graphic Design": "creativity",
        "Figma": "creativity",
        "Visual Communication": "creativity",
        "Business Analysis": "analytical_thinking",
        "Excel": "analytical_thinking",
        "Decision Making": "analytical_thinking",
        "Leadership": "communication",
        "Teamwork": "communication",
        "Teaching": "communication"
    }

    for skill, level in student_skills.items():

        feature_name = skill_mapping.get(skill)

        if feature_name:
            features[feature_name] = level_mapping.get(level, 1)

    input_data = pd.DataFrame([features])

    prediction = model.predict(input_data)

    career = encoder.inverse_transform(prediction)[0]

    return career