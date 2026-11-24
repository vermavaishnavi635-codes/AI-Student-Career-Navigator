
import os
import joblib
import pandas as pd

from sklearn.ensemble import RandomForestClassifier
from sklearn.preprocessing import LabelEncoder
from sklearn.model_selection import (
    StratifiedKFold,
    cross_val_predict
)
from sklearn.metrics import (
    accuracy_score,
    balanced_accuracy_score,
    precision_score,
    recall_score,
    f1_score,
    classification_report,
    confusion_matrix
)


# =====================================
# FILE PATHS
# =====================================

BASE_DIR = os.path.dirname(os.path.abspath(__file__))

DATASET_PATH = os.path.join(
    BASE_DIR, "data", "career_dataset.csv"
)

MODEL_PATH = os.path.join(
    BASE_DIR, "career_model.pkl"
)

ENCODER_PATH = os.path.join(
    BASE_DIR, "career_encoder.pkl"
)

FEATURE_INFO_PATH = os.path.join(
    BASE_DIR, "career_feature_info.pkl"
)


# =====================================
# MODEL FEATURES
# =====================================

FEATURE_COLUMNS = [
    "python",
    "sql",
    "problem_solving",
    "data_structures",
    "web_development",
    "creativity",
    "communication",
    "analytical_thinking"
]


# =====================================
# SKILL LEVEL MAPPING
# =====================================

LEVEL_MAPPING = {
    "beginner": 1,
    "intermediate": 3,
    "advanced": 5
}


SKILL_MAPPING = {
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


# =====================================
# CREATE MODEL
# =====================================

def create_model():

    return RandomForestClassifier(
        n_estimators=300,
        max_depth=4,
        min_samples_split=4,
        min_samples_leaf=2,
        max_features="sqrt",
        class_weight="balanced",
        random_state=42,
        n_jobs=-1
    )


# =====================================
# VALIDATE DATASET
# =====================================

def load_and_validate_dataset():

    if not os.path.exists(DATASET_PATH):
        raise FileNotFoundError(
            "Career dataset not found: " + DATASET_PATH
        )

    data = pd.read_csv(DATASET_PATH)

    required_columns = FEATURE_COLUMNS + ["career"]

    missing_columns = [
        column for column in required_columns
        if column not in data.columns
    ]

    if missing_columns:
        raise ValueError(
            f"Missing dataset columns: {missing_columns}"
        )

    data = data[required_columns].copy()

    if data.empty:
        raise ValueError("Dataset is empty!")

    if data.isnull().any().any():
        raise ValueError(
            "Dataset contains missing values. "
            "Please correct the CSV before training."
        )

    for column in FEATURE_COLUMNS:

        data[column] = pd.to_numeric(
            data[column],
            errors="coerce"
        )

        if data[column].isnull().any():
            raise ValueError(
                f"Invalid numeric values in column: {column}"
            )

        if not data[column].between(1, 5).all():
            raise ValueError(
                f"Skill scores in {column} must be between 1 and 5."
            )

        if not (data[column] % 1 == 0).all():
            raise ValueError(
                f"Skill scores in {column} must be whole numbers."
            )

    data["career"] = data["career"].astype(str).str.strip()

    if (data["career"] == "").any():
        raise ValueError("Dataset contains empty career labels!")

    if data["career"].nunique() < 3:
        raise ValueError(
            "Dataset must contain at least 3 career categories."
        )

    class_counts = data["career"].value_counts()

    if class_counts.min() < 5:
        raise ValueError(
            "Each career category needs at least 5 records "
            "for 5-fold stratified cross-validation."
        )

    return data


# =====================================
# TRAIN AND EVALUATE MODEL
# =====================================

def train_model():

    print("\n========== DATASET VALIDATION ==========")

    data = load_and_validate_dataset()

    X = data[FEATURE_COLUMNS]
    y = data["career"]

    print("Total Records:", len(data))
    print("Total Features:", len(FEATURE_COLUMNS))
    print("Career Categories:", y.nunique())

    print("\nCareer Distribution:")
    print(y.value_counts().sort_index())

    duplicate_count = int(data.duplicated().sum())

    print("\nExact Duplicate Records:", duplicate_count)

    if duplicate_count > 0:
        print(
            "Warning: Duplicate records detected. "
            "They have not been automatically removed."
        )

    # Encode career labels
    encoder = LabelEncoder()
    y_encoded = encoder.fit_transform(y)

    # 5-Fold Stratified Cross-Validation
    cv = StratifiedKFold(
        n_splits=5,
        shuffle=True,
        random_state=42
    )

    model = create_model()

    print("\n========== CROSS-VALIDATION ==========")

    predictions = cross_val_predict(
        model,
        X,
        y_encoded,
        cv=cv,
        method="predict",
        n_jobs=1
    )

    accuracy = accuracy_score(
        y_encoded,
        predictions
    )

    balanced_accuracy = balanced_accuracy_score(
        y_encoded,
        predictions
    )

    precision = precision_score(
        y_encoded,
        predictions,
        average="macro",
        zero_division=0
    )

    recall = recall_score(
        y_encoded,
        predictions,
        average="macro",
        zero_division=0
    )

    f1 = f1_score(
        y_encoded,
        predictions,
        average="macro",
        zero_division=0
    )

    print("Accuracy:", round(accuracy * 100, 2), "%")

    print(
        "Balanced Accuracy:",
        round(balanced_accuracy * 100, 2), "%"
    )

    print("Macro Precision:", round(precision, 4))
    print("Macro Recall:", round(recall, 4))
    print("Macro F1-Score:", round(f1, 4))

    print("\n========== CLASSIFICATION REPORT ==========")

    print(
        classification_report(
            y_encoded,
            predictions,
            labels=list(range(len(encoder.classes_))),
            target_names=encoder.classes_,
            zero_division=0
        )
    )

    print("\n========== CONFUSION MATRIX ==========")

    matrix = confusion_matrix(
        y_encoded,
        predictions,
        labels=list(range(len(encoder.classes_)))
    )

    confusion_df = pd.DataFrame(
        matrix,
        index=encoder.classes_,
        columns=encoder.classes_
    )

    print(confusion_df)

    # =====================================
    # TRAIN FINAL MODEL ON ALL RECORDS
    # =====================================

    print("\n========== FINAL MODEL TRAINING ==========")

    final_model = create_model()

    final_model.fit(X, y_encoded)

    feature_info = {
        "default_values": X.median().to_dict(),
        "feature_columns": FEATURE_COLUMNS,
        "dataset_records": len(data),
        "career_categories": list(encoder.classes_)
    }

    joblib.dump(final_model, MODEL_PATH)
    joblib.dump(encoder, ENCODER_PATH)
    joblib.dump(feature_info, FEATURE_INFO_PATH)

    print("\nModel trained successfully!")
    print("Model saved:", MODEL_PATH)
    print("Encoder saved:", ENCODER_PATH)
    print("Feature information saved:", FEATURE_INFO_PATH)

    print("\n========== FEATURE IMPORTANCE ==========")

    importance = pd.Series(
        final_model.feature_importances_,
        index=FEATURE_COLUMNS
    ).sort_values(ascending=False)

    print(importance.round(4))

    print("\nTraining completed successfully!")


# =====================================
# PREPARE STUDENT FEATURES
# =====================================

def prepare_student_features(student_skills):

    if not isinstance(student_skills, dict):
        raise ValueError(
            "Student skills must be provided as a dictionary."
        )

    if not os.path.exists(FEATURE_INFO_PATH):
        raise FileNotFoundError(
            "Feature information not found. "
            "Run python career_engine.py first."
        )

    feature_info = joblib.load(FEATURE_INFO_PATH)

    default_values = feature_info["default_values"]

    features = {
        feature: float(default_values[feature])
        for feature in FEATURE_COLUMNS
    }

    for skill, level in student_skills.items():

        feature_name = SKILL_MAPPING.get(skill)

        if feature_name is None:
            continue

        if isinstance(level, (int, float)):
            numeric_level = float(level)

        else:
            level_name = str(level).strip().lower()

            numeric_level = LEVEL_MAPPING.get(level_name)

            if numeric_level is None:
                continue

        if not 1 <= numeric_level <= 5:
            raise ValueError(
                f"Invalid level for {skill}. "
                "Skill level must be between 1 and 5."
            )

        features[feature_name] = numeric_level

    return pd.DataFrame(
        [features],
        columns=FEATURE_COLUMNS
    )


# =====================================
# TOP CAREER RECOMMENDATIONS
# =====================================

def predict_top_careers(student_skills, top_n=3):

    required_files = [
        MODEL_PATH,
        ENCODER_PATH,
        FEATURE_INFO_PATH
    ]

    for file_path in required_files:

        if not os.path.exists(file_path):
            raise FileNotFoundError(
                "Required ML file not found: "
                + file_path
                + ". Run python career_engine.py first."
            )

    if not isinstance(top_n, int) or top_n < 1:
        raise ValueError("top_n must be a positive integer.")

    model = joblib.load(MODEL_PATH)
    encoder = joblib.load(ENCODER_PATH)

    input_data = prepare_student_features(student_skills)

    scores = model.predict_proba(input_data)[0]

    ranked_indices = scores.argsort()[::-1]

    results = []

    for index in ranked_indices[:top_n]:

        career_name = encoder.inverse_transform(
            [model.classes_[index]]
        )[0]

        score = round(
            float(scores[index]) * 100,
            2
        )

        results.append({
            "career": career_name,
            "probability": score
        })

    return results


# =====================================
# SINGLE CAREER PREDICTION
# =====================================

def predict_career(student_skills):

    recommendations = predict_top_careers(
        student_skills,
        top_n=1
    )

    return recommendations[0]["career"]


# =====================================
# RUN TRAINING
# =====================================

if __name__ == "__main__":
    train_model()
