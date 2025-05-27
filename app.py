import cv2
import tkinter as tk
from tkinter import filedialog, messagebox
import os
import numpy as np

# Globals
contours = []       # All polygons
current_contour = []  # Points of current polygon
temp_img = None
original_img = None

def select_image_file():
    root = tk.Tk()
    root.withdraw()
    return filedialog.askopenfilename(title="Select Eye Image",
                                      filetypes=[("Image files", "*.jpg *.png *.jpeg")])

def mouse_callback(event, x, y, flags, param):
    global current_contour, temp_img

    if event == cv2.EVENT_LBUTTONDOWN:
        current_contour.append((x, y))
        redraw(param)

def redraw(img):
    global temp_img
    temp_img = img.copy()

    # Draw current in-progress polygon
    for i in range(len(current_contour)):
        cv2.circle(temp_img, current_contour[i], 3, (0, 255, 0), -1)
        if i > 0:
            cv2.line(temp_img, current_contour[i - 1], current_contour[i], (0, 255, 0), 1)

    # Draw finalized contours
    for poly in contours:
        pts = np.array(poly, np.int32)
        cv2.polylines(temp_img, [pts], isClosed=True, color=(255, 0, 0), thickness=2)

    # Add on-screen instructions
    instructions = [
        "Left-click: Draw point",
        "'C': Complete polygon",
        "'U': Undo point",
        "'R': Restart",
        "'N': No object (blank mask)",
        "ENTER: Save mask",
        "ESC: Cancel"
    ]

    y0 = 20
    for i, text in enumerate(instructions):
        cv2.putText(temp_img, text, (10, y0 + i * 20),
                    cv2.FONT_HERSHEY_SIMPLEX, 0.5, (255, 255, 255), 1, cv2.LINE_AA)

    cv2.imshow("Draw Mask", temp_img)

def save_segmentation_mask(original_image, filename, polygons):
    height, width = original_image.shape[:2]
    mask = np.zeros((height, width), dtype=np.uint8)

    for poly in polygons:
        pts = np.array(poly, np.int32)
        cv2.fillPoly(mask, [pts], 255)

    base_name = os.path.splitext(os.path.basename(filename))[0]
    output_dir = "./datasets/masked/"
    os.makedirs(output_dir, exist_ok=True)
    mask_filename = os.path.join(output_dir, f"{base_name}_mask.png")
    cv2.imwrite(mask_filename, mask)
    print(f"Saved flexible mask: {mask_filename}")


def save_blank_mask(original_image, filename):
    height, width = original_image.shape[:2]
    mask = np.zeros((height, width), dtype=np.uint8)

    base_name = os.path.splitext(os.path.basename(filename))[0]
    os.makedirs("./datasets/masked/", exist_ok=True)
    mask_filename = f"./datasets/masked/{base_name}_mask.png"
    cv2.imwrite(mask_filename, mask)
    print(f"No object in frame. Saved blank mask: {mask_filename}")

def main():
    global current_contour, contours, temp_img, original_img

    img_path = select_image_file()
    if not img_path:
        print("No image selected.")
        return

    img = cv2.imread(img_path)
    if img is None:
        print("Failed to load image.")
        return

    original_img = img.copy()
    temp_img = img.copy()

    cv2.namedWindow("Draw Mask")
    cv2.setMouseCallback("Draw Mask", mouse_callback, param=img)
    redraw(img)

    print("Instructions:")
    print("- Click to draw points of a polygon.")
    print("- Press 'C' to complete a polygon.")
    print("- Press 'U' to undo last point.")
    print("- Press ENTER to save the mask.")
    print("- Press 'N' if no object (saves blank mask).")
    print("- Press 'R' to restart drawing.")
    print("- Press ESC to cancel.")

    while True:
        cv2.imshow("Draw Mask", temp_img)
        key = cv2.waitKey(1) & 0xFF

        if key == 13:  # ENTER
            if contours:
                save_segmentation_mask(original_img, img_path, contours)
                break
            else:
                messagebox.showerror("Error", "No mask drawn. Press 'N' to save blank mask.")

        elif key == ord('c'):
            if len(current_contour) >= 3:
                contours.append(current_contour.copy())
                current_contour.clear()
                redraw(original_img)
            else:
                print("Need at least 3 points to form a polygon.")

        elif key == ord('u'):
            if current_contour:
                current_contour.pop()
                redraw(original_img)

        elif key == ord('n'):
            print("Marked as 'No object in frame'")
            save_blank_mask(original_img, img_path)
            break

        elif key == ord('r'):
            print("Restarting drawing...")
            current_contour = []
            contours = []
            redraw(original_img)

        elif key == 27:  # ESC
            print("Canceled.")
            break

    cv2.destroyAllWindows()

if __name__ == "__main__":
    main()
