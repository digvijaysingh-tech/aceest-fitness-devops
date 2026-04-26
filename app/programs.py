PROGRAMS = {
    "fat-loss": {
        "code": "FL",
        "name": "Fat Loss",
        "workout": [
            "Mon: 5x5 Back Squat + AMRAP",
            "Tue: EMOM 20min Assault Bike",
            "Wed: Bench Press + 21-15-9",
            "Thu: 10RFT Deadlifts/Box Jumps",
            "Fri: 30min Active Recovery",
        ],
        "diet": [
            "B: 3 Egg Whites + Oats Idli",
            "L: Grilled Chicken + Brown Rice",
            "D: Fish Curry + Millet Roti",
        ],
        "calories": 2000,
        "calorie_factor": 22,
    },
    "muscle-gain": {
        "code": "MG",
        "name": "Muscle Gain",
        "workout": [
            "Mon: Squat 5x5",
            "Tue: Bench 5x5",
            "Wed: Deadlift 4x6",
            "Thu: Front Squat 4x8",
            "Fri: Incline Press 4x10",
            "Sat: Barbell Rows 4x10",
        ],
        "diet": [
            "B: 4 Eggs + PB Oats",
            "L: Chicken Biryani (250g Chicken)",
            "D: Mutton Curry + Jeera Rice",
        ],
        "calories": 3200,
        "calorie_factor": 35,
    },
    "beginner": {
        "code": "BG",
        "name": "Beginner",
        "workout": [
            "Circuit Training: Air Squats, Ring Rows, Push-ups",
            "Focus: Technique Mastery & Form (90% Threshold)",
        ],
        "diet": [
            "Balanced Tamil Meals: Idli-Sambar, Rice-Dal, Chapati",
            "Protein: 120g/day",
        ],
        "calories": 2400,
        "calorie_factor": 26,
    },
}

SITE_METRICS = {"capacity_users": 150, "area_sqft": 10000, "break_even_members": 250}

AI_TEMPLATES = {
    "fat-loss": [
        "Full Body HIIT 3x/week + 2 Zone-2 Cardio sessions",
        "Circuit Training 4x/week + daily 10k steps",
        "Upper/Lower split with 20min conditioning finisher",
    ],
    "muscle-gain": [
        "Push/Pull/Legs (6 days) + 2x/week core work",
        "Upper/Lower split (4 days) with progressive overload",
        "Full Body Strength 3x/week + 1 hypertrophy accessory day",
    ],
    "beginner": [
        "Full Body 3x/week, technique-first (50-70% 1RM)",
        "Light Strength + Mobility, alternating days",
        "Bodyweight Circuit 3x/week for 4 weeks, then add loading",
    ],
}


def estimate_calories(program_key: str, weight_kg: float) -> int:
    program = PROGRAMS.get(program_key)
    if program is None:
        raise KeyError(program_key)
    if weight_kg <= 0:
        raise ValueError("weight must be positive")
    return int(weight_kg * program["calorie_factor"])


def generate_ai_program(program_key: str, seed: int = None) -> dict:
    """Deterministic when a seed is provided — makes the endpoint testable."""
    import random as _random

    if program_key not in AI_TEMPLATES:
        raise KeyError(program_key)
    rng = _random.Random(seed) if seed is not None else _random
    template = rng.choice(AI_TEMPLATES[program_key])
    return {
        "program": program_key,
        "generated_plan": template,
        "calorie_factor": PROGRAMS[program_key]["calorie_factor"],
    }
