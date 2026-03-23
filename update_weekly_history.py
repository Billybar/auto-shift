# update_history.py
import re
import openpyxl


def update_history_from_excel(xlsx_path, config_path):
    """
    Reads the previous week's site schedule (Excel export), calculates the
    historical streak and weekend shifts based on exact row/col indices,
    and directly updates config.py safely without breaking tuples.
    """

    # Mapping Hebrew names from the Excel to the Yalam IDs in config.py
    name_to_id = {
        'אירינה גונקו': 111172,
        'אלכס קרסילניקוב': 111386,
        'ברק טרבולסי': 106363,
        'גלעד אלברט': 110606,
        'גרוסברד גדי': 105744,
        'דולב אזולאי': 108119,
        'מיכאל פייגין': 111145,
        'סער אליעזרי': 111046,
        'עמינדב (בילי) בר חיים': 108520,
        'שון בן צבי': 109350
    }

    morning_rows = [6, 8, 18]
    noon_rows = [10, 12]
    night_rows = [14, 16]
    all_shift_rows = morning_rows + noon_rows + night_rows

    fri_col = 6
    sat_col = 7

    # --- 1. Read Excel (.xlsx) and Extract Data ---
    csv_data = []
    try:
        wb = openpyxl.load_workbook(xlsx_path, data_only=True)
        sheet = wb.active

        for row in sheet.iter_rows(values_only=True):
            cleaned_row = [str(cell) if cell is not None else "" for cell in row]
            csv_data.append(cleaned_row)

        print(f"✅ Successfully read Excel file: '{xlsx_path}'.")
    except FileNotFoundError:
        print(f"❌ Error: Could not find '{xlsx_path}'. Check the file name and path.")
        return
    except Exception as e:
        print(f"❌ Error loading Excel file: {e}")
        return

    history_updates = {}

    for emp_name, emp_id in name_to_id.items():
        def is_working(row_idx, col_idx):
            if row_idx < len(csv_data) and col_idx < len(csv_data[row_idx]):
                return csv_data[row_idx][col_idx].strip() == emp_name
            return False

        fri_night = any(is_working(r, fri_col) for r in night_rows)
        sat_noon = any(is_working(r, sat_col) for r in noon_rows)
        sat_night = any(is_working(r, sat_col) for r in night_rows)

        streak = 0
        for day_col in range(7, 0, -1):
            worked_that_day = any(is_working(r, day_col) for r in all_shift_rows)
            if worked_that_day:
                streak += 1
            else:
                break

        history_updates[emp_id] = {
            'history_streak': streak,
            'worked_last_fri_night': fri_night,
            'worked_last_sat_noon': sat_noon,
            'worked_last_sat_night': sat_night
        }

    print(f"📊 Extracted history for {len(history_updates)} employees. Updating config.py...")

    # --- 2. Update config.py with ROBUST Regex ---
    try:
        with open(config_path, 'r', encoding='utf-8') as f:
            config_content = f.read()
    except FileNotFoundError:
        print(f"❌ Error: Could not find '{config_path}'")
        return

    updated_count = 0

    for emp_id, state_updates in history_updates.items():
        # חותך בלוק שלם לעובד ספציפי (עד העובד הבא או עד סוף הרשימה)
        emp_pattern = re.compile(r"(id\s*=\s*" + str(emp_id) + r"\b.*?)(?=Employee\s*\(|\])", re.DOTALL)
        match = emp_pattern.search(config_content)

        if not match:
            print(f"⚠️ Warning: Employee ID {emp_id} not found in config.py. Skipping.")
            continue

        emp_block = match.group(1)

        for field, new_value in state_updates.items():
            # מחפש את השדה באופן ספציפי (ללא קשר לסוגריים)
            field_pattern = re.compile(r"\b" + field + r"\s*=\s*[A-Za-z0-9_]+")

            if field_pattern.search(emp_block):
                # אם השדה קיים, רק מעדכן את הערך שלו
                emp_block = field_pattern.sub(f"{field}={new_value}", emp_block)
            else:
                # אם השדה לא קיים, מזריק אותו בבטחה מיד בשורה שאחרי WeeklyState(
                emp_block = re.sub(
                    r"(WeeklyState\s*\()",
                    r"\g<1>\n            " + field + "=" + str(new_value) + ",",
                    emp_block,
                    count=1
                )

        # מדביק את הבלוק המתוקן בחזרה לקובץ השלם
        config_content = config_content[:match.start()] + emp_block + config_content[match.end():]
        updated_count += 1

    # --- 3. Save the modifications ---
    with open(config_path, 'w', encoding='utf-8') as f:
        f.write(config_content)

    print(f"✅ Success: Updated history states for {updated_count} employees in '{config_path}'.")


if __name__ == "__main__":
    excel_file_name = 'history2102.xlsx'
    update_history_from_excel(excel_file_name, 'config.py')