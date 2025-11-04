PROJECT: Queue-Free Smart Checkout System | Sparkathon 2025
THEME: Reimagining Customer Experience
AUTHOR: Sai Sri Pujita Peddi

1. OVERVIEW
This project, developed for Walmart Sparkathon 2025, is a Queue-Free Smart Checkout System designed to eliminate checkout queues in retail stores. 
It simulates a smart trolley that automatically detects items using YOLOv8 object detection and generates a real-time bill with a Tkinter-based checkout interface.

2. KEY FEATURES
- Real-time product detection using Ultralytics YOLOv8n model.
- Automatic cart management: detected items are added to a JSON-based database.
- Itemised billing with SGST (9%), CGST (9%), and a fixed bag cost.
- Graphical checkout interface using Tkinter for billing and payment simulation.
- Image logging for detected items, saved in the 'detected_items' folder.
- Seamless two-phase flow: Detection → Billing & Payment.

3. SYSTEM ARCHITECTURE
Phase A: Detection  → checkout_demo.py  
   • Captures video input through webcam.
   • Uses YOLOv8n model for object detection.
   • Adds detected items (confidence > 0.4) into 'cart_data.json'.
   • Saves cropped detected images in 'detected_items/' folder.

Phase B: Billing  → checkout_gui.py  
   • Loads data from 'cart_data.json'.
   • Displays items in a GUI with quantity, unit price, and total cost.
   • Computes total cost with taxes and bag fee.
   • Supports adding/removing items and simulating payment.

4. TECHNOLOGY STACK
Programming Language : Python 3.8+
Object Detection      : YOLOv8n (Ultralytics)
Computer Vision       : OpenCV (cv2)
GUI Framework         : Tkinter
Data Storage          : JSON files

5. INSTALLATION & SETUP

REQUIREMENTS:
- Python 3.8 or higher
- Functional webcam

INSTALLATION STEPS:
1. Clone this repository:
      git clone https://github.com/Pujita-544/Sparkathon2025.git
      cd Sparkathon2025

2. Create and activate a virtual environment:
      python -m venv venv
      .\venv\Scripts\Activate.ps1    (Windows)
      source venv/bin/activate       (Linux/Mac)

3. Install dependencies:
      pip install -r requirements.txt

4. Ensure the following files exist:
      • yolov8n.pt           (YOLOv8 model weights)
      • item_database.json   (Item-price mapping)
      • cart_data.json       (Auto-generated cart data)
      • detected_items/      (Folder for detected images)

6. EXECUTION

PHASE A: DETECTION
Command:
      python checkout_demo.py

Controls:
      b  → Add detected items to cart (confidence > 0.4)
      q  → Quit detection and save 'cart_data.json'

After quitting, a bill summary prints in the terminal and all cropped item images are saved.

PHASE B: BILLING
Command:
      python checkout_gui.py

This opens the GUI window for billing:
      • Loads cart data automatically.
      • Displays items, quantities, and totals.
      • Calculates taxes and bag fee.
      • User can select payment mode (Cash / Card / UPI).
      • On confirmation, final payment simulated and cart reset.

7. FILE STRUCTURE
Sparkathon2025/
│
├── checkout_demo.py        → Phase A: Object Detection
├── checkout_gui.py         → Phase B: Billing Interface
├── item_database.json      → Stores item name and price
├── cart_data.json          → Generated cart data
├── yolov8n.pt              → YOLO model weights
├── detected_items/         → Cropped images of detected items
├── requirements.txt        → Python dependencies
└── README.txt              → Documentation file

8. SAMPLE OUTPUT
Terminal Bill Summary:
------------------------------------------------------------
S.No  Item        Qty   Unit ₹   Subtotal ₹
1     apple       2     50       100
2     milk        1     35       35
--------------------------------------------
Subtotal : ₹135.00
SGST (9%): ₹12.15
CGST (9%): ₹12.15
Bag Cost : ₹5.00
Total    : ₹164.30
------------------------------------------------------------

GUI Summary:
• Itemized list with editable quantities.
• Dropdown to select payment mode.
• Confirm Payment button with thank-you message.

9. NOTES
- 'cart_data.json' is auto-generated during detection.
- Ensure webcam permissions are enabled.
- Detected images are saved automatically for audit/reference.
- The YOLOv8 model should be placed in the project root directory.

10. AUTHOR & CREDITS
Developed by: Sai Sri Pujita Peddi & Eega Akshasreee
GitHub: https://github.com/Pujita-544

Developed as part of Walmart Sparkathon 2025 using open-source frameworks under their respective licenses.
