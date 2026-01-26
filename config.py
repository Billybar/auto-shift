# config.py
from dataclasses import dataclass, field
from typing import List, Tuple, Optional

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
#         Data Models (Nested Structure)
# ==========================================

@dataclass
class ContactDetails:
    """Static details that do not affect the algorithm."""
    phone: str = ""
    email: str = ""


@dataclass
class ShiftPreferences:
    """Numerical rules and constraints (Configuration)."""
    max_shifts: int
    target_shifts: int
    max_nights: int
    min_nights: int
    max_mornings: int
    min_mornings: int
    max_evenings: int
    min_evenings: int


@dataclass
class WeeklyState:
    """Dynamic State - resets or updates every week."""
    history_streak: int
    worked_last_sat_noon: bool
    worked_last_sat_night: bool
    # Specific constraints for the current week
    unavailable_shifts: List[Tuple[int, int]] = field(default_factory=list)
    forced_shifts: List[Tuple[int, int]] = field(default_factory=list)


@dataclass
class Employee:
    """Main Object - connects all components."""
    id: int
    name: str
    color: str
    is_active: bool = True

    # Composition
    contact: ContactDetails
    prefs: ShiftPreferences
    state: WeeklyState


# ==========================================
#         Employees List
# ==========================================
EMPLOYEES: List[Employee] = [
    Employee(
        id=0, name='Ira', color='FF9999',
        contact=ContactDetails(),
        prefs=ShiftPreferences(
            target_shifts=5, max_shifts=5,
            max_nights=1, min_nights=1,
            max_mornings=3, min_mornings=1,
            max_evenings=3, min_evenings=1
        ),
        state=WeeklyState(
            history_streak=0,
            worked_last_sat_noon=True,
            worked_last_sat_night=False,
            unavailable_shifts=[(6, 1), (6, 2)]
        )
    ),

    Employee(
        id=1, name='Alex', color='99FF99',
        contact=ContactDetails(),
        prefs=ShiftPreferences(
            target_shifts=4, max_shifts=6,
            max_nights=2, min_nights=1,
            max_mornings=1, min_mornings=0,
            max_evenings=3, min_evenings=1
        ),
        state=WeeklyState(
            history_streak=0,
            worked_last_sat_noon=False,
            worked_last_sat_night=False,
            unavailable_shifts=[
                (0, 0), (0, 1), (0, 2), (1, 0), (1, 1), (1, 2),
                (2, 0), (2, 1), (2, 2), (3, 0), (3, 1), (3, 2),
                (4, 0), (4, 1), (4, 2), (5, 0), (5, 1), (5, 2),
                (6, 0), (6, 1), (6, 2)
            ]
        )
    ),

    Employee(
        id=2, name='Barak', color='9999FF',
        contact=ContactDetails(),
        prefs=ShiftPreferences(
            target_shifts=5, max_shifts=6,
            max_nights=0, min_nights=0,
            max_mornings=6, min_mornings=4,
            max_evenings=0, min_evenings=0
        ),
        state=WeeklyState(
            history_streak=0,
            worked_last_sat_noon=False,
            worked_last_sat_night=False,
            unavailable_shifts=[
                (0, 0), (0, 1), (0, 2), (1, 0), (1, 1), (1, 2),
                (2, 0), (2, 1), (2, 2), (3, 0), (3, 1), (3, 2),
                (4, 0), (4, 1), (4, 2), (5, 0), (5, 1), (5, 2),
                (6, 0), (6, 1), (6, 2)
            ]
        )
    ),

    Employee(
        id=3, name='Gilad', color='FFFF99',
        contact=ContactDetails(),
        prefs=ShiftPreferences(
            target_shifts=3, max_shifts=4,
            max_nights=1, min_nights=1,
            max_mornings=3, min_mornings=0,
            max_evenings=4, min_evenings=0
        ),
        state=WeeklyState(
            history_streak=3,
            worked_last_sat_noon=False,
            worked_last_sat_night=False,
            unavailable_shifts=[
                (0, 0), (0, 1), (0, 2), (1, 2), (1, 1), (2, 2),
                (3, 0), (3, 1), (3, 2), (4, 0), (5, 2), (6, 1), (6, 2)
            ]
        )
    ),

    Employee(
        id=4, name='Gadi', color='FFCC99',
        contact=ContactDetails(),
        prefs=ShiftPreferences(
            target_shifts=5, max_shifts=6,
            max_nights=2, min_nights=2,
            max_mornings=2, min_mornings=0,
            max_evenings=3, min_evenings=5
        ),
        state=WeeklyState(
            history_streak=3,
            worked_last_sat_noon=False,
            worked_last_sat_night=True,
            unavailable_shifts=[(0, 0), (0, 1), (4, 2), (5, 0), (6, 2)]
        )
    ),

    Employee(
        id=5, name='Dolev', color='FF99FF',
        contact=ContactDetails(),
        prefs=ShiftPreferences(
            target_shifts=4, max_shifts=6,
            max_nights=2, min_nights=2,
            max_mornings=1, min_mornings=0,
            max_evenings=4, min_evenings=0
        ),
        state=WeeklyState(
            history_streak=1,
            worked_last_sat_noon=False,
            worked_last_sat_night=False,
            unavailable_shifts=[(5, 0), (5, 1), (5, 2)]
        )
    ),

    Employee(
        id=6, name='Michael', color='99FFFF',
        contact=ContactDetails(),
        prefs=ShiftPreferences(
            target_shifts=3, max_shifts=5,
            max_nights=2, min_nights=1,
            max_mornings=1, min_mornings=0,
            max_evenings=2, min_evenings=1
        ),
        state=WeeklyState(
            history_streak=3,
            worked_last_sat_noon=False,
            worked_last_sat_night=True,
            unavailable_shifts=[
                (0, 0), (0, 2), (1, 0), (1, 2), (2, 0), (2, 2),
                (3, 0), (3, 2), (4, 0), (4, 2)
            ]
        )
    ),

    Employee(
        id=7, name='Saar', color='CCCCCC',
        contact=ContactDetails(),
        prefs=ShiftPreferences(
            target_shifts=5, max_shifts=6,
            max_nights=2, min_nights=1,
            max_mornings=3, min_mornings=0,
            max_evenings=5, min_evenings=0
        ),
        state=WeeklyState(
            history_streak=4,
            worked_last_sat_noon=True,
            worked_last_sat_night=False,
            unavailable_shifts=[]
        )
    ),

    Employee(
        id=8, name='Billy', color='87CEFA',
        contact=ContactDetails(),
        prefs=ShiftPreferences(
            target_shifts=5, max_shifts=5,
            max_nights=2, min_nights=1,
            max_mornings=3, min_mornings=2,
            max_evenings=3, min_evenings=2
        ),
        state=WeeklyState(
            history_streak=0,
            worked_last_sat_noon=False,
            worked_last_sat_night=False,
            forced_shifts=[(1, 0), (2, 1), (3, 1), (4, 0), (5, 0)],
            unavailable_shifts=[
                (0, 0), (0, 1), (1, 2), (2, 0), (2, 2), (3, 0),
                (4, 1), (5, 1), (5, 2), (6, 0), (6, 1), (6, 2)
            ]
        )
    ),

    Employee(
        id=9, name='Shon', color='E6B8B7',
        contact=ContactDetails(),
        prefs=ShiftPreferences(
            target_shifts=5, max_shifts=6,
            max_nights=3, min_nights=1,
            max_mornings=1, min_mornings=0,
            max_evenings=4, min_evenings=0
        ),
        state=WeeklyState(
            history_streak=0,
            worked_last_sat_noon=False,
            worked_last_sat_night=False,
            unavailable_shifts=[(0, 0), (0, 1), (0, 2), (1, 0), (5, 1)]
        )
    ),

    Employee(
        id=10, name='ENFORCE', color='FFFFFF',
        contact=ContactDetails(),
        prefs=ShiftPreferences(
            target_shifts=1, max_shifts=1,
            max_nights=2, min_nights=0,
            max_mornings=1, min_mornings=0,
            max_evenings=4, min_evenings=0
        ),
        state=WeeklyState(
            history_streak=0,
            worked_last_sat_noon=False,
            worked_last_sat_night=False,
            unavailable_shifts=[]
        )
    )
]