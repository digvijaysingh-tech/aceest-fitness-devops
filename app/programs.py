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


def estimate_calories(program_key: str, weight_kg: float) -> int:
    program = PROGRAMS.get(program_key)
    if program is None:
        raise KeyError(program_key)
    if weight_kg <= 0:
        raise ValueError("weight must be positive")
    return int(weight_kg * program["calorie_factor"])
