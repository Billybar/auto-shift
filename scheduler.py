import os
import openpyxl
from openpyxl.styles import PatternFill, Font, Alignment, Border, Side
from ortools.sat.python import cp_model

# ==========================================
#         System Configuration
# ==========================================

# Enable image parsing?
# True = Try to read constraints from the image file
# False = Ignore image, use only the manual list below
ENABLE_IMAGE_PARSING = False

# Image filename (if enabled)
IMAGE_FILENAME = "images/image3.png"


# ==========================================

def solve_shift_scheduling():
    # -------------------------------------------------------------------------
    # 1. Data Definition
    # -------------------------------------------------------------------------
    employees = [
        {'name': 'Barak', 'target_shifts': 6, 'max_shifts': 6,
         'max_nights': 0, 'min_nights': 0,
         'max_mornings': 6, 'min_mornings': 6,
         'max_evenings': 0, 'min_evenings': 0,
         'history_streak': 0},

        {'name': 'Billy', 'target_shifts': 5, 'max_shifts': 5,
         'max_nights': 2, 'min_nights': 1,
         'max_mornings': 3, 'min_mornings': 2,
         'max_evenings': 3, 'min_evenings': 3,
         'history_streak': 6},

        {'name': 'Asaf', 'target_shifts': 5, 'max_shifts': 6,
         'max_nights': 2, 'min_nights': 2,
         'max_mornings': 0, 'min_mornings': 0,
         'max_evenings': 3, 'min_evenings': 3,
         'history_streak': 2},

        {'name': 'Gadi', 'target_shifts': 5, 'max_shifts': 6,
         'max_nights': 2, 'min_nights': 2,
         'max_mornings': 3, 'min_mornings': 0,
         'max_evenings': 3, 'min_evenings': 5,
         'history_streak': 0},

        {'name': 'Saar', 'target_shifts': 5, 'max_shifts': 6,
         'max_nights': 2, 'min_nights': 1,
         'max_mornings': 3, 'min_mornings': 0,
         'max_evenings': 5, 'min_evenings': 0,
         'history_streak': 0},

        {'name': 'Ira', 'target_shifts': 5, 'max_shifts': 6,
         'max_nights': 1, 'min_nights': 1,
         'max_mornings': 3, 'min_mornings': 2,
         'max_evenings': 3, 'min_evenings': 0,
         'history_streak': 0},

        {'name': 'Shon', 'target_shifts': 3, 'max_shifts': 4,
         'max_nights': 2, 'min_nights': 0,
         'max_mornings': 2, 'min_mornings': 0,
         'max_evenings': 4, 'min_evenings': 0,
         'history_streak': 0},

        {'name': 'Gilad', 'target_shifts': 3, 'max_shifts': 4,
         'max_nights': 1, 'min_nights': 1,
         'max_mornings': 3, 'min_mornings': 0,
         'max_evenings': 4, 'min_evenings': 0,
         'history_streak': 0},

        {'name': 'Dolev', 'target_shifts': 3, 'max_shifts': 4,
         'max_nights': 3, 'min_nights': 2,
         'max_mornings': 2, 'min_mornings': 0,
         'max_evenings': 4, 'min_evenings': 0,
         'history_streak': 0},

        {'name': 'Michael', 'target_shifts': 3, 'max_shifts': 4,
         'max_nights': 2, 'min_nights': 0,
         'max_mornings': 2, 'min_mornings': 0,
         'max_evenings': 2, 'min_evenings': 0,
         'history_streak': 0},
    ]

    employee_colors = [
        'FF9999', '99FF99', '9999FF', 'FFFF99', 'FFCC99',
        'FF99FF', '99FFFF', 'CCCCCC', 'D9D9D9', 'E6B8B7'
    ]

    num_employees = len(employees)
    num_days = 7
    num_shifts = 3
    shifts_per_day_demand = 2

    # --------------------------------------------------------
    # Manual Constraints List
    # --------------------------------------------------------
    # Enter manual constraints here
    # Format: (Employee ID, Day 0-6, Shift 0-2)
    manual_requests = [
        # ID 0
        (0, 0, 2), (0, 1, 1), (0, 1, 2), (0, 5, 1), (0, 5, 2),
        # ID 1
        (1, 0, 0), (1, 1, 2), (1, 2, 0), (1, 2, 2), (1, 3, 0), (1, 3, 2),
        (1, 4, 1), (1, 4, 2), (1, 5, 1), (1, 5, 2), (1, 6, 0), (1, 6, 1), (1, 6, 2),
        # ID 2
        (2, 4, 1), (2, 5, 1), (2, 5, 2), (2, 6, 0), (2, 6, 1),
        # ID 3
        (3, 1, 0), (3, 1, 1), (3, 2, 1), (3, 3, 2),
        (3, 4, 0), (3, 4, 1), (3, 4, 2), (3, 5, 0),
        # ID 4
        (4, 6, 1),
        # ID 5
        (5, 0, 1),
        # ID 6
        (6, 0, 0), (6, 1, 0), (6, 2, 0), (6, 2, 2), (6, 3, 0), (6, 3, 2),
        (6, 4, 0), (6, 4, 2), (6, 6, 1), (6, 6, 2),
        # ID 7
        (7, 0, 0), (7, 0, 1), (7, 0, 2), (7, 1, 0), (7, 1, 1), (7, 1, 2),
        (7, 2, 2), (7, 3, 1), (7, 3, 2), (7, 4, 1), (7, 4, 2), (7, 5, 0),
        (7, 6, 1), (7, 6, 2),
        # ID 8
        (8, 0, 0), (8, 4, 2), (8, 5, 0), (8, 5, 1), (8, 5, 2), (8, 6, 0),
        # ID 9
        (9, 0, 0), (9, 1, 0), (9, 1, 1), (9, 1, 2), (9, 2, 0), (9, 2, 1),
        (9, 3, 0), (9, 4, 0), (9, 4, 1), (9, 4, 2), (9, 5, 0),
    ]

    # --------------------------------------------------------
    # Image Parsing Logic (Only if enabled)
    # --------------------------------------------------------
    image_constraints = []

    if ENABLE_IMAGE_PARSING:
        print(f"--- Image Mode Enabled: Parsing {IMAGE_FILENAME} ---")
        if os.path.exists(IMAGE_FILENAME):
            try:
                # Import only if needed to avoid crashes if file is missing/broken
                from image_parser import ScheduleImageParser

                # Define employee order in image (Top -> Down)
                img_employee_order = [0, 1, 2, 3, 4, 5, 6, 7]

                parser = ScheduleImageParser(IMAGE_FILENAME)
                # Call the new parse_tables function
                image_constraints = parser.parse_tables(img_employee_order)
                print(f"V Success: Extracted {len(image_constraints)} constraints from image.")
            except ImportError:
                print("X Error: image_parser.py is missing or invalid.")
            except AttributeError:
                print("X Error: 'parse_tables' function not found in image_parser.py. Check file version.")
            except Exception as e:
                print(f"X General Error parsing image: {e}")
        else:
            print(f"X Error: File {IMAGE_FILENAME} not found.")
    else:
        print("--- Image Mode Disabled: Using manual list only ---")

    # Combine Lists
    unavailable_requests = manual_requests + image_constraints

    # Debug Print
    print(f"\nTotal active constraints: {len(unavailable_requests)}")
    days_map = ["Sunday", "Monday", "Tuesday", "Wednesday", "Thursday", "Friday", "Saturday"]
    shifts_map = ["Morning", "Noon", "Night"]

    if len(unavailable_requests) > 0:
        print("Constraints Details:")
        for req in unavailable_requests:
            e, d, s = req
            if 0 <= e < len(employees):
                print(f"- {employees[e]['name']}: {days_map[d]} {shifts_map[s]}")

    model = cp_model.CpModel()

    # -------------------------------------------------------------------------
    # 2. Variables
    # -------------------------------------------------------------------------
    shift_vars = {}
    for e in range(num_employees):
        for d in range(num_days):
            for s in range(num_shifts):
                shift_vars[(e, d, s)] = model.NewBoolVar(f'shift_{e}_{d}_{s}')

    # -------------------------------------------------------------------------
    # 3. Hard Constraints
    # -------------------------------------------------------------------------

    # A. Exact number of workers per shift
    for d in range(num_days):
        for s in range(num_shifts):
            model.Add(sum(shift_vars[(e, d, s)] for e in range(num_employees)) == shifts_per_day_demand)

    # B. Prevent back-to-back shifts
    for e in range(num_employees):
        for total_s in range(num_days * num_shifts - 1):
            day = total_s // num_shifts
            shift = total_s % num_shifts
            next_total_s = total_s + 1
            next_day = next_total_s // num_shifts
            next_shift = next_total_s % num_shifts
            model.Add(shift_vars[(e, day, shift)] + shift_vars[(e, next_day, next_shift)] <= 1)

    # C. Apply unavailability (Manual + Image)
    for req in unavailable_requests:
        e, d, s = req
        if 0 <= e < num_employees and 0 <= d < num_days and 0 <= s < num_shifts:
            model.Add(shift_vars[(e, d, s)] == 0)

    # D. Prevent working 7 days in a row
    for e in range(num_employees):
        work_days_vars = []
        for d in range(num_days):
            is_working_day = model.NewBoolVar(f'working_day_{e}_{d}')
            model.Add(sum(shift_vars[(e, d, s)] for s in range(num_shifts)) > 0).OnlyEnforceIf(is_working_day)
            model.Add(sum(shift_vars[(e, d, s)] for s in range(num_shifts)) == 0).OnlyEnforceIf(is_working_day.Not())
            work_days_vars.append(is_working_day)

        streak = employees[e]['history_streak']
        if streak > 0:
            limit = 7 - streak
            if limit <= num_days and limit > 0:
                model.Add(sum(work_days_vars[0:limit]) < limit)
        if streak == 0:
            model.Add(sum(work_days_vars) < 7)

    # -------------------------------------------------------------------------
    # 4. Soft Constraints (Optimization)
    # -------------------------------------------------------------------------
    WEIGHT_TARGET_SHIFTS = 4
    WEIGHT_REST_GAP = 2

    WEIGHT_MAX_NIGHTS = 5
    WEIGHT_MAX_MORNINGS = 4
    WEIGHT_MAX_EVENINGS = 4
    WEIGHT_CONSECUTIVE_NIGHTS = 20

    WEIGHT_MIN_NIGHTS = 5
    WEIGHT_MIN_MORNINGS = 4
    WEIGHT_MIN_EVENINGS = 4

    objective_terms = []

    for e in range(num_employees):
        emp_shifts = []
        morning_shifts = []
        evening_shifts = []
        night_shifts = []

        for d in range(num_days):
            morning_shifts.append(shift_vars[(e, d, 0)])
            evening_shifts.append(shift_vars[(e, d, 1)])
            night_shifts.append(shift_vars[(e, d, 2)])

            for s in range(num_shifts):
                emp_shifts.append(shift_vars[(e, d, s)])

        # Maximum Constraints
        excess_nights = model.NewIntVar(0, 7, f'excess_nights_{e}')
        model.Add(sum(night_shifts) <= employees[e]['max_nights'] + excess_nights)
        objective_terms.append(excess_nights * WEIGHT_MAX_NIGHTS)

        excess_mornings = model.NewIntVar(0, 7, f'excess_mornings_{e}')
        model.Add(sum(morning_shifts) <= employees[e]['max_mornings'] + excess_mornings)
        objective_terms.append(excess_mornings * WEIGHT_MAX_MORNINGS)

        excess_evenings = model.NewIntVar(0, 7, f'excess_evenings_{e}')
        model.Add(sum(evening_shifts) <= employees[e]['max_evenings'] + excess_evenings)
        objective_terms.append(excess_evenings * WEIGHT_MAX_EVENINGS)

        # Minimum Constraints
        shortage_nights = model.NewIntVar(0, 7, f'shortage_nights_{e}')
        model.Add(sum(night_shifts) + shortage_nights >= employees[e]['min_nights'])
        objective_terms.append(shortage_nights * WEIGHT_MIN_NIGHTS)

        shortage_mornings = model.NewIntVar(0, 7, f'shortage_mornings_{e}')
        model.Add(sum(morning_shifts) + shortage_mornings >= employees[e]['min_mornings'])
        objective_terms.append(shortage_mornings * WEIGHT_MIN_MORNINGS)

        shortage_evenings = model.NewIntVar(0, 7, f'shortage_evenings_{e}')
        model.Add(sum(evening_shifts) + shortage_evenings >= employees[e]['min_evenings'])
        objective_terms.append(shortage_evenings * WEIGHT_MIN_EVENINGS)

        # Logic and Rest
        # Avoid 3 consecutive nights
        for d in range(num_days - 2):
            is_three_nights = model.NewBoolVar(f'3nights_{e}_{d}')
            model.AddBoolAnd(
                [shift_vars[(e, d, 2)], shift_vars[(e, d + 1, 2)], shift_vars[(e, d + 2, 2)]]).OnlyEnforceIf(
                is_three_nights)
            model.AddBoolOr([shift_vars[(e, d, 2)].Not(), shift_vars[(e, d + 1, 2)].Not(),
                             shift_vars[(e, d + 2, 2)].Not()]).OnlyEnforceIf(is_three_nights.Not())
            objective_terms.append(is_three_nights * WEIGHT_CONSECUTIVE_NIGHTS)

        # Avoid short rest gap
        for total_s in range(num_days * num_shifts - 2):
            day = total_s // num_shifts
            shift = total_s % num_shifts
            t_total_s = total_s + 2
            t_day = t_total_s // num_shifts
            t_shift = t_total_s % num_shifts
            both_working = model.NewBoolVar(f'bad_gap_{e}_{total_s}')
            model.AddBoolAnd([shift_vars[(e, day, shift)], shift_vars[(e, t_day, t_shift)]]).OnlyEnforceIf(both_working)
            model.AddBoolOr([shift_vars[(e, day, shift)].Not(), shift_vars[(e, t_day, t_shift)].Not()]).OnlyEnforceIf(
                both_working.Not())
            objective_terms.append(both_working * WEIGHT_REST_GAP)

        # Target Shifts
        total_worked = sum(emp_shifts)
        delta = model.NewIntVar(0, 21, f'delta_target_{e}')
        model.Add(total_worked - employees[e]['target_shifts'] <= delta)
        model.Add(employees[e]['target_shifts'] - total_worked <= delta)
        objective_terms.append(delta * WEIGHT_TARGET_SHIFTS)

        # Hard limit max shifts
        model.Add(total_worked <= employees[e]['max_shifts'])

    # -------------------------------------------------------------------------
    # 5. Solve and Export
    # -------------------------------------------------------------------------
    model.Minimize(sum(objective_terms))
    solver = cp_model.CpSolver()
    status = solver.Solve(model)

    if status == cp_model.OPTIMAL or status == cp_model.FEASIBLE:
        print(f"\n✅ Solution Found! Cost (Penalty): {solver.ObjectiveValue()}")
        create_excel_schedule(solver, shift_vars, employees, num_days, num_shifts, shifts_per_day_demand,
                              employee_colors)
    else:
        print("\n❌ No feasible solution found. Try relaxing constraints.")


def create_excel_schedule(solver, shift_vars, employees, num_days, num_shifts, shifts_per_day_demand, colors):
    wb = openpyxl.Workbook()
    ws = wb.active
    ws.title = "Schedule"
    ws.sheet_view.rightToLeft = True

    days_names = ["ראשון", "שני", "שלישי", "רביעי", "חמישי", "שישי", "שבת"]
    shifts_names = ["בוקר", "צהריים", "לילה"]

    header_font = Font(bold=True, color="FFFFFF")
    header_fill = PatternFill(start_color="4472C4", end_color="4472C4", fill_type="solid")
    center_align = Alignment(horizontal='center', vertical='center')
    thin_border = Border(left=Side(style='thin'), right=Side(style='thin'), top=Side(style='thin'),
                         bottom=Side(style='thin'))

    # Header Row
    ws.cell(row=1, column=1).value = "משמרת"
    for i, day in enumerate(days_names):
        cell = ws.cell(row=1, column=i + 2)
        cell.value = day
        cell.font = header_font
        cell.fill = header_fill
        cell.alignment = center_align

    current_row = 2
    for s_idx, s_name in enumerate(shifts_names):
        for slot in range(shifts_per_day_demand):
            shift_cell = ws.cell(row=current_row, column=1)
            shift_cell.value = f"{s_name} ({slot + 1})"
            shift_cell.font = Font(bold=True)
            shift_cell.alignment = center_align
            shift_cell.border = thin_border

            for d in range(num_days):
                assigned_workers = []
                for e_idx, emp in enumerate(employees):
                    if solver.Value(shift_vars[(e_idx, d, s_idx)]):
                        assigned_workers.append(e_idx)

                cell = ws.cell(row=current_row, column=d + 2)
                cell.border = thin_border
                cell.alignment = center_align

                if len(assigned_workers) > slot:
                    worker_idx = assigned_workers[slot]
                    worker_name = employees[worker_idx]['name']
                    worker_color = colors[worker_idx]

                    cell.value = worker_name
                    cell.fill = PatternFill(start_color=worker_color, end_color=worker_color, fill_type="solid")
            current_row += 1
        current_row += 1

    # Summary Table
    summary_row = current_row + 2
    ws.cell(row=summary_row, column=1).value = "סיכום עובדים"
    ws.cell(row=summary_row, column=1).font = Font(bold=True, size=14)

    headers = ["שם", "סהכ משמרות", "לילות", "בקרים", "ערבים"]
    for col_idx, h in enumerate(headers):
        ws.cell(row=summary_row + 1, column=col_idx + 1).value = h
        ws.cell(row=summary_row + 1, column=col_idx + 1).font = Font(bold=True)

    for i, emp in enumerate(employees):
        r = summary_row + 2 + i
        name_cell = ws.cell(row=r, column=1)
        name_cell.value = emp['name']
        name_cell.fill = PatternFill(start_color=colors[i], end_color=colors[i], fill_type="solid")

        total = 0
        nights = 0
        mornings = 0
        evenings = 0

        for d in range(num_days):
            if solver.Value(shift_vars[(i, d, 0)]): mornings += 1
            if solver.Value(shift_vars[(i, d, 1)]): evenings += 1
            if solver.Value(shift_vars[(i, d, 2)]): nights += 1

        total = mornings + evenings + nights

        ws.cell(row=r, column=2).value = total
        ws.cell(row=r, column=3).value = nights
        ws.cell(row=r, column=4).value = mornings
        ws.cell(row=r, column=5).value = evenings

    wb.save("shift_schedule_colored.xlsx")
    print("Excel file created successfully: shift_schedule_colored.xlsx")


if __name__ == "__main__":
    solve_shift_scheduling()