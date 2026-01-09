# config.py

# ==========================================
#         System Configuration
# ==========================================
ENABLE_IMAGE_PARSING = False
IMAGE_FILENAME = "images/image3.png"

# ==========================================
#         Shift Rules & Weights
# ==========================================
NUM_DAYS = 7
NUM_SHIFTS = 3
SHIFTS_PER_DAY_DEMAND = 2

# Optimization Weights
WEIGHTS = {
    'TARGET_SHIFTS': 40,
    'REST_GAP': 2,
    'MAX_NIGHTS': 5,
    'MAX_MORNINGS': 4,
    'MAX_EVENINGS': 2,
    'CONSECUTIVE_NIGHTS': 20,
    'MIN_NIGHTS': 5,
    'MIN_MORNINGS': 4,
    'MIN_EVENINGS': 2
}

# ==========================================
#         Data: Employees
# ==========================================
EMPLOYEES = [
    {'name': 'Ira', 'target_shifts': 5, 'max_shifts': 6,
     'max_nights': 1, 'min_nights': 1,
     'max_mornings': 3, 'min_mornings': 1,
     'max_evenings': 3, 'min_evenings': 1,
     'history_streak': 1},

    {'name': 'Alex', 'target_shifts': 4, 'max_shifts': 4,
     'max_nights': 2, 'min_nights': 1,
     'max_mornings': 1, 'min_mornings': 0,
     'max_evenings': 3, 'min_evenings': 1,
     'history_streak': 0},

    {'name': 'Barak', 'target_shifts': 5, 'max_shifts': 6,
     'max_nights': 0, 'min_nights': 0,
     'max_mornings': 6, 'min_mornings': 4,
     'max_evenings': 0, 'min_evenings': 0,
     'history_streak': 0},

    {'name': 'Gilad', 'target_shifts': 3, 'max_shifts': 4,
     'max_nights': 1, 'min_nights': 1,
     'max_mornings': 3, 'min_mornings': 0,
     'max_evenings': 4, 'min_evenings': 0,
     'history_streak': 2},

    {'name': 'Gadi', 'target_shifts': 5, 'max_shifts': 6,
     'max_nights': 2, 'min_nights': 2,
     'max_mornings': 2, 'min_mornings': 0,
     'max_evenings': 3, 'min_evenings': 5,
     'history_streak': 5},

    {'name': 'Dolev', 'target_shifts': 4, 'max_shifts': 4,
     'max_nights': 2, 'min_nights': 2,
     'max_mornings': 1, 'min_mornings': 0,
     'max_evenings': 4, 'min_evenings': 0,
     'history_streak': 1},

    {'name': 'Michael', 'target_shifts': 3, 'max_shifts': 4,
     'max_nights': 2, 'min_nights': 1,
     'max_mornings': 1, 'min_mornings': 0,
     'max_evenings': 2, 'min_evenings': 1,
     'history_streak': 2},

    {'name': 'Saar', 'target_shifts': 5, 'max_shifts': 5,
     'max_nights': 2, 'min_nights': 1,
     'max_mornings': 3, 'min_mornings': 0,
     'max_evenings': 5, 'min_evenings': 0,
     'history_streak': 4},

    {'name': 'Billy', 'target_shifts': 5, 'max_shifts': 5,
     'max_nights': 2, 'min_nights': 1,
     'max_mornings': 3, 'min_mornings': 2,
     'max_evenings': 3, 'min_evenings': 2,
     'history_streak': 0},

    {'name': 'Shon', 'target_shifts': 3, 'max_shifts': 3,
     'max_nights': 2, 'min_nights': 1,
     'max_mornings': 1, 'min_mornings': 0,
     'max_evenings': 4, 'min_evenings': 0,
     'history_streak': 1},
]

EMPLOYEE_COLORS = [
    'FF9999', '99FF99', '9999FF', 'FFFF99', 'FFCC99',
    'FF99FF', '99FFFF', 'CCCCCC', '87CEFA', 'E6B8B7'
]

# ==========================================
#         Constraints & Context
# ==========================================

# Previous Week Context
WORKED_LAST_SAT_NOON = [5, 7]
WORKED_LAST_SAT_NIGHT = [6, 4]

# Manual Assignments (Force Shift)
MANUAL_ASSIGNMENTS = [
    (8, 4, 0), (8, 5, 0), (8, 1, 1),
]

# Manual Unavailability Requests
# Format: (Employee ID, Day 0-6, Shift 0-2)
MANUAL_REQUESTS = [
    # --- Employee ID 0 ---
    (0, 4, 2),  # חמישי
    (0, 5, 0), (0, 5, 1),  # שישי

# --- ID 1: Additional Constraints ---
    (1, 0, 1), # ראשון צהריים
    (1, 1, 0), # שני בוקר
    (1, 2, 2), # שלישי לילה
    (1, 3, 1), # רביעי צהריים
    (1, 4, 2), # חמישי לילה

    # --- Employee ID 2 ---
    (2, 5, 0),  # שישי
    (2, 6, 0),  # שבת

    # --- Employee ID 3 ---
    (3, 0, 0), (3, 0, 1), (3, 0, 2),  # ראשון
    (3, 1, 0), (3, 1, 1), (3, 1, 2),  # שני
    (3, 2, 2),  # שלישי
    (3, 3, 2),  # רביעי
    (3, 4, 2),  # חמישי
    (3, 6, 1), (3, 6, 2),  # שבת

    # --- Employee ID 4 ---
    (4, 3, 2),  # רביעי
    (4, 4, 0), (4, 4, 1), (4, 4, 2),  # חמישי
    (4, 5, 0), (4, 5, 1), (4, 5, 2),  # שישי

    # --- Employee ID 5 ---
    (5, 0, 0), (5, 1, 0), (5, 2, 0), (5, 3, 0), (5, 4, 0), (5, 5, 0),
    (5, 0, 0), (5, 0, 2),  # ראשון
    (5, 4, 2),  # חמישי
    (5, 5, 2),  # שישי
    (5, 6, 0),  # שבת

    # --- Employee ID 6 ---
    (6, 0, 2),  # ראשון
    (6, 1, 0),  # שני
    (6, 2, 2),  # שלישי
    (6, 3, 2),  # רביעי
    (6, 4, 0), (6, 4, 2),  # חמישי
    (6, 5, 0), (6, 5, 1), (6, 5, 2),  # שישי
    (6, 6, 0), (6, 6, 1),  # שבת

    # --- Employee ID 7 ---
    (7, 0, 0),  # ראשון

    # --- Employee ID 8 (Billy) ---
    (8, 0, 0),  # ראשון
    (8, 1, 2),  # שני
    (8, 2, 0), (8, 2, 2),  # שלישי
    (8, 3, 0),  # רביעי
    (8, 4, 1),  # חמישי
    (8, 5, 1), (8, 5, 2),  # שישי
    (8, 6, 0), (8, 6, 1), (8, 6, 2),  # שבת

    # --- Employee ID 9 (Shon) ---
    (9, 0, 0), (9, 1, 0), (9, 2, 0), (9, 3, 0), (9, 4, 0), (9, 5, 0),
    (9, 0, 0), (9, 0, 1), (9, 0, 2),  # ראשון
    (9, 2, 0), (9, 2, 1),  # שלישי
    (9, 5, 1), (9, 5, 2),  # שישי
]