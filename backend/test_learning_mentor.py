import logging
from modules.learning_mentor.engine import LearningMentorEngine
from modules.learning_mentor.models import PersonalLearningProfile
from modules.adaptive_learning.engine import AdaptiveLearningEngine
from modules.recommendations.recommender import RecommendationEngine

logging.basicConfig(level=logging.DEBUG)

def test_learning_mentor():
    print("--- Testing AI Learning Mentor & Adaptive Engine ---")
    
    # 1. Initialize Mock User
    profile = PersonalLearningProfile(
        user_id="user-xyz-999",
        role="EAF Operator",
        department="Melting Shop",
        completed_lessons=["Basic Metallurgy"],
        strengths=["Furnace Basics"],
        weak_areas=["Safety Protocols"]
    )
    
    # 2. Mock Role Requirements (Operator needs 3 courses, but has only completed 1)
    role_reqs = {
        "EAF Operator": ["Basic Metallurgy", "EAF Operation", "LOTO Safety Standards"]
    }
    
    # 3. Test Mentor Engine (Dashboard Data)
    mentor = LearningMentorEngine()
    dashboard_data = mentor.get_mentor_dashboard_data(profile, role_reqs)
    
    print("\n--- Mentor Dashboard Data ---")
    print(f"Detected Skill Gaps: {dashboard_data['skill_gaps']}")
    print(f"Top Strength: {dashboard_data['insights']['top_strength']}")
    print(f"Today's Goal: {dashboard_data['daily_goal']['title']}")
    
    # 4. Test Adaptive Engine (Routing)
    adaptive = AdaptiveLearningEngine()
    adaptive_steps = adaptive.generate_next_steps(dashboard_data['skill_gaps'])
    
    print("\n--- Adaptive Learning Steps ---")
    for step in adaptive_steps:
        print(f"Module: {step['module']} | Priority: {step['priority']}")
        
    # 5. Test Recommender Engine (Formatting)
    recommender = RecommendationEngine()
    final_recommendations = recommender.get_recommendations(adaptive_steps)
    
    print("\n--- Final Output Recommendations ---")
    print(final_recommendations)
    
    print("\nTest Complete!")

if __name__ == "__main__":
    test_learning_mentor()
