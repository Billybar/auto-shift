# optimizer.py
from ortools.sat.python import cp_model
import config


def build_and_solve_model(employees, unavailable_requests, manual_assignments,
                          worked_last_sat_noon, worked_last_sat_night):
    num_employees = len(employees)
    num_days = config.NUM_DAYS
    num_shifts = config.NUM_SHIFTS

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
            model.Add(sum(shift_vars[(e, d, s)] for e in range(num_employees)) == config.SHIFTS_PER_DAY_DEMAND)

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

    # D. Apply Previous Week Constraints (Rest Rules)
    for emp_id in worked_last_sat_night:
        if 0 <= emp_id < num_employees:
            model.Add(shift_vars[(emp_id, 0, 0)] == 0)

    # E. Apply Manual Assignments (Force Specific Shifts)
    for assign in manual_assignments:
        e, d, s = assign
        if 0 <= e < num_employees and 0 <= d < num_days and 0 <= s < num_shifts:
            # Validate against unavailability constraints
            if (e, d, s) in unavailable_requests:
                emp_name = employees[e]['name']
                raise ValueError(f"CRITICAL ERROR: Conflict detected for {emp_name}! "
                                 f"You are forcing a shift (Day {d}, Shift {s}) but it is marked as UNAVAILABLE.")
            print(f"Forcing assignment: Employee {e} -> Day {d} Shift {s}")
            model.Add(shift_vars[(e, d, s)] == 1)

    # F. Prevent working 7 days in a row
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

    # G. Max one shift per day per employee
    # One shift a day only - cannot do morning and night at the same day
    for e in range(num_employees):
        for d in range(num_days):
            model.Add(sum(shift_vars[(e, d, s)] for s in range(num_shifts)) <= 1)

    # -------------------------------------------------------------------------
    # 4. Soft Constraints (Optimization)
    # -------------------------------------------------------------------------
    w = config.WEIGHTS  # Alias for shorter code
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
        objective_terms.append(excess_nights * w['MAX_NIGHTS'])

        excess_mornings = model.NewIntVar(0, 7, f'excess_mornings_{e}')
        model.Add(sum(morning_shifts) <= employees[e]['max_mornings'] + excess_mornings)
        objective_terms.append(excess_mornings * w['MAX_MORNINGS'])

        excess_evenings = model.NewIntVar(0, 7, f'excess_evenings_{e}')
        model.Add(sum(evening_shifts) <= employees[e]['max_evenings'] + excess_evenings)
        objective_terms.append(excess_evenings * w['MAX_EVENINGS'])

        # Minimum Constraints
        shortage_nights = model.NewIntVar(0, 7, f'shortage_nights_{e}')
        model.Add(sum(night_shifts) + shortage_nights >= employees[e]['min_nights'])
        objective_terms.append(shortage_nights * w['MIN_NIGHTS'])

        shortage_mornings = model.NewIntVar(0, 7, f'shortage_mornings_{e}')
        model.Add(sum(morning_shifts) + shortage_mornings >= employees[e]['min_mornings'])
        objective_terms.append(shortage_mornings * w['MIN_MORNINGS'])

        shortage_evenings = model.NewIntVar(0, 7, f'shortage_evenings_{e}')
        model.Add(sum(evening_shifts) + shortage_evenings >= employees[e]['min_evenings'])
        objective_terms.append(shortage_evenings * w['MIN_EVENINGS'])

        # Logic and Rest
        # Avoid 3 consecutive nights
        for d in range(num_days - 2):
            is_three_nights = model.NewBoolVar(f'3nights_{e}_{d}')
            model.AddBoolAnd(
                [shift_vars[(e, d, 2)], shift_vars[(e, d + 1, 2)], shift_vars[(e, d + 2, 2)]]).OnlyEnforceIf(
                is_three_nights)
            model.AddBoolOr([shift_vars[(e, d, 2)].Not(), shift_vars[(e, d + 1, 2)].Not(),
                             shift_vars[(e, d + 2, 2)].Not()]).OnlyEnforceIf(is_three_nights.Not())
            objective_terms.append(is_three_nights * w['CONSECUTIVE_NIGHTS'])

        # If employee worked last Sat night + works Sun night + works Mon night -> Penalty
        if e in worked_last_sat_night:
            is_continuation_3_nights = model.NewBoolVar(f'3nights_from_prev_week_{e}')
            # בדיקה: האם עובד לילה ביום 0 (ראשון) וגם לילה ביום 1 (שני)
            model.AddBoolAnd([shift_vars[(e, 0, 2)], shift_vars[(e, 1, 2)]]).OnlyEnforceIf(is_continuation_3_nights)
            model.AddBoolOr([shift_vars[(e, 0, 2)].Not(), shift_vars[(e, 1, 2)].Not()]).OnlyEnforceIf(
                is_continuation_3_nights.Not())

            objective_terms.append(is_continuation_3_nights * w['CONSECUTIVE_NIGHTS'])

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
            objective_terms.append(both_working * w['REST_GAP'])

        # include Previous Week Gap (saturday noon and night)
        if e in worked_last_sat_noon:
            objective_terms.append(shift_vars[(e, 0, 0)] * w['REST_GAP'])

        # Optimization: If worked Last Sat Night, avoid Sun Noon.
        if e in worked_last_sat_night:
            objective_terms.append(shift_vars[(e, 0, 1)] * w['REST_GAP'])

        # Target Shifts
        total_worked = sum(emp_shifts)
        delta = model.NewIntVar(0, 21, f'delta_target_{e}')
        model.Add(total_worked - employees[e]['target_shifts'] <= delta)
        model.Add(employees[e]['target_shifts'] - total_worked <= delta)
        objective_terms.append(delta * w['TARGET_SHIFTS'])

        # Hard limit max shifts
        model.Add(total_worked <= employees[e]['max_shifts'])

    # -------------------------------------------------------------------------
    # 5. Solve
    # -------------------------------------------------------------------------
    model.Minimize(sum(objective_terms))
    solver = cp_model.CpSolver()
    status = solver.Solve(model)

    return solver, status, shift_vars