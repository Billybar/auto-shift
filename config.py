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
    'TARGET_SHIFTS': 4,
    'REST_GAP': 2,
    'MAX_NIGHTS': 5,
    'MAX_MORNINGS': 4,
    'MAX_EVENINGS': 4,
    'CONSECUTIVE_NIGHTS': 20,
    'MIN_NIGHTS': 5,
    'MIN_MORNINGS': 4,
    'MIN_EVENINGS': 4
}

# ==========================================
#         Data: Employees
# ==========================================
EMPLOYEES = [
    {'name': 'Ira', 'target_shifts': 5, 'max_shifts': 6,
     'max_nights': 1, 'min_nights': 1,
     'max_mornings': 3, 'min_mornings': 1,
     'max_evenings': 3, 'min_evenings': 1,
     'history_streak': 2},

    {'name': 'Asaf', 'target_shifts': 5, 'max_shifts': 6,
     'max_nights': 2, 'min_nights': 2,
     'max_mornings': 0, 'min_mornings': 0,
     'max_evenings': 3, 'min_evenings': 3,
     'history_streak': 1},

    {'name': 'Barak', 'target_shifts': 5, 'max_shifts': 6,
     'max_nights': 0, 'min_nights': 0,
     'max_mornings': 6, 'min_mornings': 6,
     'max_evenings': 0, 'min_evenings': 0,
     'history_streak': 0},

    {'name': 'Gilad', 'target_shifts': 3, 'max_shifts': 4,
     'max_nights': 1, 'min_nights': 1,
     'max_mornings': 3, 'min_mornings': 0,
     'max_evenings': 4, 'min_evenings': 0,
     'history_streak': 0},

    {'name': 'Gadi', 'target_shifts': 4, 'max_shifts': 4,
     'max_nights': 2, 'min_nights': 2,
     'max_mornings': 3, 'min_mornings': 0,
     'max_evenings': 3, 'min_evenings': 5,
     'history_streak': 3},

    {'name': 'Dolev', 'target_shifts': 4, 'max_shifts': 4,
     'max_nights': 2, 'min_nights': 2,
     'max_mornings': 0, 'min_mornings': 0,
     'max_evenings': 4, 'min_evenings': 0,
     'history_streak': 1},

    {'name': 'Michael', 'target_shifts': 3, 'max_shifts': 4,
     'max_nights': 2, 'min_nights': 1,
     'max_mornings': 2, 'min_mornings': 0,
     'max_evenings': 2, 'min_evenings': 1,
     'history_streak': 0},

    {'name': 'Saar', 'target_shifts': 5, 'max_shifts': 5,
     'max_nights': 2, 'min_nights': 1,
     'max_mornings': 3, 'min_mornings': 0,
     'max_evenings': 5, 'min_evenings': 0,
     'history_streak': 5},

    {'name': 'Billy', 'target_shifts': 5, 'max_shifts': 5,
     'max_nights': 2, 'min_nights': 1,
     'max_mornings': 3, 'min_mornings': 2,
     'max_evenings': 3, 'min_evenings': 2,
     'history_streak': 0},

    {'name': 'Shon', 'target_shifts': 3, 'max_shifts': 4,
     'max_nights': 2, 'min_nights': 1,
     'max_mornings': 0, 'min_mornings': 0,
     'max_evenings': 4, 'min_evenings': 0,
     'history_streak': 0},
]

EMPLOYEE_COLORS = [
    'FF9999', '99FF99', '9999FF', 'FFFF99', 'FFCC99',
    'FF99FF', '99FFFF', 'CCCCCC', '87CEFA', 'E6B8B7'
]

# ==========================================
#         Constraints & Context
# ==========================================

# Previous Week Context
WORKED_LAST_SAT_NOON = [0, 4]  # Example: Ira and Gadi
WORKED_LAST_SAT_NIGHT = [1, 5]  # Example: Asaf, Dolev

# Manual Assignments (Force Shift)
MANUAL_ASSIGNMENTS = [
    (8, 4, 0), (8, 5, 0), (8, 1, 1),
]

# Manual Unavailability Requests
# Format: (Employee ID, Day 0-6, Shift 0-2)
MANUAL_REQUESTS = [
    # --- ID 0: Ira ---
    (0, 3, 0), (0, 3, 1), (0, 3, 2),
    (0, 4, 0), (0, 4, 1), (0, 4, 2),

    # --- ID 1: Asaf ---
    (1, 5, 1), (1, 5, 2),
    (1, 6, 0), (1, 6, 1),

    # --- ID 2: Barak ---
    (2, 5, 0),
    (2, 6, 0),

    # --- ID 3: Gilad ---
    (3, 0, 0), (3, 0, 1), (3, 0, 2),
    (3, 1, 0), (3, 1, 1), (3, 1, 2),
    (3, 2, 2),
    (3, 3, 1), (3, 3, 2),
    (3, 4, 2),
    (3, 6, 1), (3, 6, 2),

    # --- ID 4: Gadi ---
    (4, 0, 0), (4, 0, 1), (4, 0, 2),
    (4, 3, 1), (4, 3, 2),

    # --- ID 5: Dolev ---
    (5, 4, 0), (5, 4, 1), (5, 4, 2),
    (5, 5, 0), (5, 5, 1), (5, 5, 2),

    # --- ID 6: Michael ---
    (6, 0, 0), (6, 0, 1), (6, 0, 2),
    (6, 1, 2),
    (6, 2, 2),
    (6, 3, 2),
    (6, 4, 2),

    # --- ID 8: Billy ---
    (8, 0, 0), (8, 0, 1),
    (8, 1, 2),
    (8, 2, 0), (8, 2, 2),
    (8, 3, 0),
    (8, 4, 1), (8, 4, 2),
    (8, 5, 1), (8, 5, 2),
    (8, 6, 0), (8, 6, 1), (8, 6, 2),

    # --- ID 9: Shon ---
    (9, 3, 1), (9, 3, 2),
    (9, 4, 0), (9, 4, 1),
    (9, 5, 1), (9, 5, 2),
]