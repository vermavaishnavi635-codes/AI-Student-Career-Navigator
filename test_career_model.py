
from career_engine import predict_top_careers

# Sample student skills
student_skills = {
    "Python": "Advanced",
    "SQL": "Advanced",
    "Problem Solving": "Advanced",
    "Data Structures": "Advanced",
    "Web Development": "Intermediate",
    "Creativity": "Beginner",
    "Communication": "Intermediate",
    "Analytical Thinking": "Advanced"
}

print("\n========== STUDENT CAREER PREDICTION ==========")

recommendations = predict_top_careers(
    student_skills,
    top_n=3
)

for index, item in enumerate(recommendations, start=1):

    print(f"\nRank {index}")
    print("Career:", item["career"])
    print("Model Score:", item["probability"], "%")

