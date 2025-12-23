import google.generativeai as genai
import PIL.Image
import os
import ast

# --- CONFIGURATION ---
# 1. Get your free API key here: https://aistudio.google.com/app/apikey
# It is recommended to use environment variables for security
os.environ["GOOGLE_API_KEY"] = "YOUR_PASTED_API_KEY_HERE"
genai.configure(api_key=os.environ["GOOGLE_API_KEY"])

# --- MODEL SETUP ---
# Using 'gemini-1.5-flash' is recommended for the free tier due to higher rate limits (15 RPM).
# If the image recognition isn't good enough, switch to 'gemini-1.5-pro'.
model = genai.GenerativeModel('gemini-1.5-flash')

# --- DATA PREPARATION ---
image_path = 'image3.png'  # Ensure this file exists
if not os.path.exists(image_path):
    print(f"Error: File '{image_path}' not found.")
    exit()

img = PIL.Image.open(image_path)

# --- SYSTEM PROMPT (YOUR CUSTOM INSTRUCTION) ---
system_instruction = """
תפקיד ומטרות:
* פעל כמומחה בעיבוד תמונה המתמחה בניתוח טבלאות אילוצי עובדים.
* סרוק תמונות המכילות טבלאות שבועיות עבור מספר עובדים.
* זהה במדויק סימוני עיגול אדום המציינים חוסר זמינות של עובד למשמרת ספציפית.
* המר את הנתונים הוויזואליים לרשימת פייתון מובנית בפורמט: (empID, day : 0-6, shift: 0-2).

התנהגות וכללים:
1) תהליך הניתוח:
א) זהה כל טבלה בנפרד ושייך אותה למזהה עובד (empID) רלוונטי (לפי סדר מלמעלה למטה: 0, 1, 2...).
ב) עבור כל טבלה, סרוק 7 ימים (0=ראשון עד 6=שבת) ו-3 משמרות ליום (0=בוקר, 1=צהריים, 2=ערב).
ג) חלץ רק את המשמרות המסומנות בעיגול אדום כמשמרות 'לא זמינות'.

2) בקרת איכות ודיוק:
א) בצע בדיקה משולשת (Triple-check) של הנתונים לפני הפקת הפלט כדי למנוע טעויות זיהוי.
ב) וודא שההתאמה בין המיקום בטבלה לבין האינדקסים (יום ומשמרת) מדויקת לחלוטין.

3) פורמט הפלט:
א) הצג את התוצאה הסופית כמשתנה בשם unavailable_requests המכיל רשימת טאפלים (tuples).
ב) שמור על מבנה הקוד כפי שהוגדר בדוגמה: (ID, day, shift).
ג) החזר רק את רשימת ה-Python, ללא טקסט נוסף, ללא Markdown וללא הסברים.
"""

# --- EXECUTION ---
print("Sending image to Gemini (Free Tier)...")

try:
    # Sending the prompt and the image
    response = model.generate_content([system_instruction, img])

    # Cleaning the response just in case
    response_text = response.text.strip()
    # Remove markdown code blocks if present
    if response_text.startswith("```"):
        response_text = response_text.split("```")[1]
        if response_text.startswith("python"):
            response_text = response_text[6:]

    # Locate the list part if there's extra text
    start_index = response_text.find('[')
    end_index = response_text.rfind(']') + 1

    if start_index != -1 and end_index != -1:
        list_str = response_text[start_index:end_index]

        # Convert string to actual Python list
        unavailable_requests = ast.literal_eval(list_str)

        print("\n--- Success! Data Extracted ---")
        print(f"Total constraints found: {len(unavailable_requests)}")
        print("Data Structure (List of Tuples):")
        print(unavailable_requests)
    else:
        print("\n--- Parsing Error ---")
        print("Could not find a valid list in the response.")
        print("Raw response:", response_text)

except Exception as e:
    print(f"\n--- API Error ---")
    print(e)