# update_config_file.py
import re
from bs4 import BeautifulSoup


def modify_config_file_physically(html_path, config_path):
    """
    Parses the Yalam HTML file and physically modifies the config.py file.
    First, it resets specific state attributes for ALL employees.
    Then, it updates the unavailable_shifts lists only for matching Employee IDs.
    """
    # --- 1. Read the existing config.py file ---
    try:
        with open(config_path, 'r', encoding='utf-8') as f:
            config_content = f.read()
    except FileNotFoundError:
        print(f"❌ Error: Could not find '{config_path}'")
        return

    # --- 2. Global Reset for ALL Employees ---
    # Reset history_streak to 0
    config_content = re.sub(r"(history_streak\s*=\s*)\d+", r"\g<1>0", config_content)

    # Reset weekend boolean flags to False
    config_content = re.sub(r"(worked_last_fri_night\s*=\s*)(True|False)", r"\g<1>False", config_content)
    config_content = re.sub(r"(worked_last_sat_noon\s*=\s*)(True|False)", r"\g<1>False", config_content)
    config_content = re.sub(r"(worked_last_sat_night\s*=\s*)(True|False)", r"\g<1>False", config_content)

    # Reset unavailable_shifts to empty lists []
    # (re.DOTALL is required because existing lists might span multiple lines)
    config_content = re.sub(r"(unavailable_shifts\s*=\s*\[).*?(\])", r"\g<1>\g<2>", config_content, flags=re.DOTALL)

    print("✅ Step 1: Successfully reset all employee states to default values.")

    # --- 3. Parse HTML to extract constraints per Employee ID ---
    try:
        with open(html_path, 'r', encoding='utf-8') as f:
            soup = BeautifulSoup(f.read(), 'html.parser')
    except FileNotFoundError:
        print(f"❌ Error: Could not find '{html_path}'")
        return

    rows = soup.find('tbody').find_all('tr', recursive=False)
    employee_constraints = {}

    for row in rows:
        cols = row.find_all('td', recursive=False)
        if len(cols) < 5:
            continue

        raw_id = cols[2].text.strip()
        if not raw_id.isdigit():
            continue

        emp_id = int(raw_id)
        constraints = []

        # Find all red circle icons for constraints (column index 4)
        circles = cols[4].find_all('i', class_='tblCircle')
        for circle in circles:
            match = re.search(r"includes\('(\d{2})'\)", circle.get('ng-if', ''))
            if match:
                code = match.group(1)
                # Convert Yalam format to OR-Tools indices (0-indexed)
                day = int(code[0]) - 1
                shift = int(code[1]) - 1
                constraints.append((day, shift))

        employee_constraints[emp_id] = constraints

    # --- 4. Apply new constraints via Regex ---
    updated_count = 0

    for emp_id, constraints in employee_constraints.items():
        if constraints:
            # Format the list properly: "(0, 1), (2, 2)"
            constraints_str = ", ".join([f"({d}, {s})" for d, s in constraints])

            # Regex targets the specific employee ID and inserts the constraints
            # inside the newly emptied brackets "[]"
            pattern = re.compile(
                r"(id\s*=\s*" + str(emp_id) + r"\b.*?unavailable_shifts\s*=\s*\[)(\])",
                re.DOTALL
            )

            if pattern.search(config_content):
                config_content = pattern.sub(r"\g<1>" + constraints_str + r"\g<2>", config_content)
                updated_count += 1
            else:
                print(f"⚠️ Warning: Employee ID {emp_id} not found in config.py or structure mismatch.")

    # --- 5. Write the modified content back to config.py ---
    with open(config_path, 'w', encoding='utf-8') as f:
        f.write(config_content)

    print(f"✅ Step 2: Physically updated {updated_count} employees with new constraints in '{config_path}'.")


if __name__ == "__main__":
    # Specify the paths to your files
    modify_config_file_physically('yalam_table.html', 'config.py')