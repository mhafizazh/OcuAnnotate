import cv2
import tkinter as tk
from tkinter import filedialog, messagebox
import os
import numpy as np

# Global vars
centers = []
radii = []
drawing = False
temp_img = None
original_img = None

def select_image_file():
    root = tk.Tk()
    root.withdraw()
    return filedialog.askopenfilename(title="Select Eye Image",
                                      filetypes=[("Image files", "*.jpg *.png *.jpeg")])

def mouse_callback(event, x, y, flags, param):
    global centers, radii, drawing, temp_img
    img = param.copy()

    if event == cv2.EVENT_LBUTTONDOWN:
        centers.append((x, y))
        radii.append(0)
        drawing = True

    elif event == cv2.EVENT_MOUSEMOVE and drawing:
        if len(centers) > 0:
            r = int(((x - centers[-1][0])**2 + (y - centers[-1][1])**2) ** 0.5)
            temp_img = img.copy()
            cv2.circle(temp_img, centers[-1], r, (0, 255, 0), 2)
            cv2.imshow("Mark Pupils", temp_img)

    elif event == cv2.EVENT_LBUTTONUP:
        drawing = False
        r = int(((x - centers[-1][0])**2 + (y - centers[-1][1])**2) ** 0.5)
        radii[-1] = r
        img_with_circle = img.copy()
        for i in range(len(centers)):
            cv2.circle(img_with_circle, centers[i], radii[i], (0, 255, 0), 2)
        temp_img = img_with_circle
        cv2.imshow("Mark Pupils", temp_img)

def save_segmentation_mask(original_image, filename, centers, radii):
    height, width = original_image.shape[:2]
    mask = np.zeros((height, width), dtype=np.uint8)

    for center, radius in zip(centers, radii):
        cv2.circle(mask, center, radius, 255, -1)  # white filled circle

    base_name = os.path.splitext(os.path.basename(filename))[0]
    os.makedirs("./datasets/masked/", exist_ok=True)
    mask_filename = f"./datasets/masked/{base_name}_mask.png"
    cv2.imwrite(mask_filename, mask)
    print(f"Saved mask: {mask_filename}")

def save_blank_mask(original_image, filename):
    height, width = original_image.shape[:2]
    mask = np.zeros((height, width), dtype=np.uint8)

    base_name = os.path.splitext(os.path.basename(filename))[0]
    os.makedirs("./datasets/masked/", exist_ok=True)
    mask_filename = f"./datasets/masked/{base_name}_mask.png"
    cv2.imwrite(mask_filename, mask)
    print(f"No iris in frame. Saved blank mask: {mask_filename}")

def main():
    global centers, radii, drawing, temp_img, original_img

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

    cv2.namedWindow("Mark Pupils")
    cv2.setMouseCallback("Mark Pupils", mouse_callback, param=img)

    print("Instructions:")
    print("1. Click and drag to mark center + radius of pupil/iris (1 or 2 circles).")
    print("2. Press ENTER to save.")
    print("3. Press N to save a blank mask (no iris).")
    print("4. Press R to restart.")
    print("5. Press ESC to cancel.")

    while True:
        cv2.imshow("Mark Pupils", temp_img)
        key = cv2.waitKey(1) & 0xFF

        if key == 13:  # ENTER
            if 1 <= len(centers) <= 2 and len(centers) == len(radii):
                save_segmentation_mask(original_img, img_path, centers, radii)
                break
            else:
                messagebox.showerror("Error", "Please draw 1 or 2 circles before saving.")

        elif key == 27:  # ESC
            print("Canceled.")
            break

        elif key == ord('r'):  # Restart
            print("Restarting annotation...")
            centers = []
            radii = []
            temp_img = original_img.copy()
            cv2.imshow("Mark Pupils", temp_img)

        elif key == ord('n'):  # No iris
            print("Marked as 'No Iris in Frame'")
            save_blank_mask(original_img, img_path)
            break

    cv2.destroyAllWindows()

if __name__ == "__main__":
    main()
