import os
from image_parser import ScheduleImageParser


def solve_shift_scheduling():
    # ... (Employee list definition remains the same) ...

    # --------------------------------------------------------
    # NEW: Load constraints from image
    # --------------------------------------------------------
    image_filename = "images/image2.png"  # The file you upload
    image_constraints = []

    if os.path.exists(image_filename):
        print(f"Loading constraints from image: {image_filename}...")
        try:
            # Define which employee corresponds to which table in the image (Top -> Down)
            # Example: Table 1 is Barak (ID 0), Table 2 is Billy (ID 1), etc.
            # You must update this list based on your image order!
            img_employee_order = [7, 3, 8]

            parser = ScheduleImageParser(image_filename)
            image_constraints = parser.extract_constraints(img_employee_order)
            print(f"Successfully extracted {len(image_constraints)} constraints from image.")
        except Exception as e:
            print(f"Error parsing image: {e}")
    else:
        print("No constraints image found, skipping.")

    # --------------------------------------------------------
    # Merge Manual Requests with Image Requests
    # --------------------------------------------------------
    # Old manual list
    manual_requests = [
        (0, 0, 2), (0, 1, 1),  # ... existing list
    ]

    # Combine both
    unavailable_requests = manual_requests + image_constraints

    # ... (Rest of the code remains exactly the same) ...