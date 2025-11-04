import cv2
import os
import json
from ultralytics import YOLO
from datetime import datetime

# Load item prices
with open("item_database.json", "r") as f:
    item_prices = json.load(f)

# Create folder for cropped images
os.makedirs("detected_items", exist_ok=True)

# Load YOLO model
model = YOLO("yolov8n.pt")

# Initialize cart
cart = {}

# Initialize webcam
cap = cv2.VideoCapture(0)

print("📷 Press 'b' to add detected items to cart.")
print("🛑 Press 'q' to quit and show bill.\n")

while True:
    ret, frame = cap.read()
    if not ret:
        print("❌ Failed to grab frame.")
        break

    results = model(frame, verbose=False)[0]
    annotated_frame = frame.copy()

    for box in results.boxes:
        cls_id = int(box.cls[0])
        conf = float(box.conf[0])
        name = model.names[cls_id].lower()

        if conf < 0.4:
            continue

        x1, y1, x2, y2 = map(int, box.xyxy[0])
        cv2.rectangle(annotated_frame, (x1, y1), (x2, y2), (0, 255, 0), 2)
        label = f"{name} ({conf:.2f})"
        cv2.putText(annotated_frame, label, (x1, y1 - 10), cv2.FONT_HERSHEY_SIMPLEX, 0.6, (0, 255, 0), 2)

    cv2.imshow("Checkout Camera", annotated_frame)
    key = cv2.waitKey(1) & 0xFF

    if key == ord('b'):
        print("\n🛒 Adding items to cart:")
        for box in results.boxes:
            cls_id = int(box.cls[0])
            name = model.names[cls_id].lower()

            if name == "person":
                print(f" - Ignored: {name}")
                continue

            if name not in item_prices:
                print(f" - Unknown item: {name} (not in database)")
                continue

            cart[name] = cart.get(name, 0) + 1
            print(f" - {name} x{cart[name]}")

            # Save cropped item image
            x1, y1, x2, y2 = map(int, box.xyxy[0])
            crop = frame[y1:y2, x1:x2]
            timestamp = datetime.now().strftime("%Y%m%d_%H%M%S_%f")
            filename = f"detected_items/{name}_{timestamp}.jpg"
            cv2.imwrite(filename, crop)

    elif key == ord('q'):
        break

cap.release()
cv2.destroyAllWindows()

# 🧾 Final Commercial Bill
print("\n🧾 Final Bill:")
print("{:<5} {:<15} {:<10} {:<10} {:<10}".format("S.No", "Item", "Qty", "Unit ₹", "Subtotal ₹"))

subtotal = 0
for i, (item, qty) in enumerate(cart.items(), start=1):
    unit_price = item_prices.get(item, 0)
    item_total = unit_price * qty
    subtotal += item_total
    print("{:<5} {:<15} {:<10} {:<10} {:<10}".format(i, item, qty, unit_price, item_total))

# Add taxes and charges
sgst = round(subtotal * 0.09, 2)
cgst = round(subtotal * 0.09, 2)
bag_cost = 5.0
total = round(subtotal + sgst + cgst + bag_cost, 2)

# Final Summary
print("\n{:>45} ₹{:>10.2f}".format("Subtotal", subtotal))
print("{:>45} ₹{:>10.2f}".format("SGST (9%)", sgst))
print("{:>45} ₹{:>10.2f}".format("CGST (9%)", cgst))
print("{:>45} ₹{:>10.2f}".format("Bag Cost", bag_cost))
print("{:>45} ₹{:>10.2f}".format("Total", total))
print("\n🧡 Thank you for shopping with us!\n")

# Save cart to cart_data.json for GUI use
with open("cart_data.json", "w") as f:
    json.dump(cart, f)