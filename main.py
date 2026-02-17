# main.py
import os
from ortools.sat.python import cp_model

# Import modules
import config
import optimizer
import excel_writer
import yalam_html_parser


def main():
    # --------------------------------------------------------
    # 1. HTML Parsing  (Optional)
    # --------------------------------------------------------
    # Note: Since we moved to an Object-Oriented structure,
    # if image parsing is enabled, we need to inject the results
    # directly into the specific Employee objects.

    # yalam_html_parser.update_constraints_from_html("yalam_table.html")

    # --------------------------------------------------------
    # 2. Run Optimization
    # --------------------------------------------------------
    # The new optimizer signature only requires the employees list.
    # All constraints (manual assignments, history, unavailability) are already inside the objects.

    print("--- Building and Solving Model ---")
    solver, status, shift_vars = optimizer.build_and_solve_model(
        employees=config.EMPLOYEES
    )

    # --------------------------------------------------------
    # 3. Output Results
    # --------------------------------------------------------
    if status == cp_model.OPTIMAL or status == cp_model.FEASIBLE:
        print(f"\n✅ Solution Found! Cost (Penalty): {solver.ObjectiveValue()}")

        # Pass the updated objects to the excel writer
        excel_writer.create_excel_schedule(
            solver=solver,
            shift_vars=shift_vars,
            employees=config.EMPLOYEES,
            num_days=config.NUM_DAYS,
            num_shifts=config.NUM_SHIFTS,
            shifts_per_day_demand=config.SHIFTS_PER_DAY_DEMAND
        )
    else:
        print("\n❌ No feasible solution found. Try relaxing constraints.")


if __name__ == "__main__":
    main()