# Eye Annotation Tool & Frame Extractor

This project provides two key tools for preparing datasets for eye segmentation tasks:

1. **Flexible Polygon-Based Eye Mask Annotator**
2. **Random Frame Extractor from Video**

## 🔧 Requirements

Make sure you have the following installed:
- Python 3.7+
- OpenCV
- NumPy
- tkinter (usually included with Python)

Install dependencies via pip:
```bash
pip install opencv-python numpy
```

## 🖼️ 1. Flexible Eye Annotation Tool

This tool allows you to draw polygon masks over eye images using OpenCV GUI.

### ✅ Features
- Draw multiple flexible polygons
- Undo last point
- Restart drawing
- Save mask or save blank if no object
- Shows instructions on screen

### 🪜 How to Use

1. Run the tool:
```bash
python annotate_eye.py
```

2. A file picker will open — select an eye image (.jpg, .png, etc.)
3. Use your mouse to click points for a polygon

**Keyboard Controls:**
- `C` - Complete polygon
- `U` - Undo last point
- `R` - Reset drawing
- `ENTER` - Save mask
- `N` - No object present (saves black mask)
- `ESC` - Cancel

Masks are saved in: `./datasets/masked/`

## 🎞️ 2. Random Frame Extractor

This tool extracts random frames from a video file and saves them as PNG images.

### 🪜 How to Use

1. Run the extractor:
```bash
python extract_frames.py
```

2. Select a video file (e.g., .mp4) from the file picker
3. 15 random frames will be extracted and saved as images

To modify the number of frames extracted, edit in `extract_frames.py`:
```python
extract_random_frames(video_path, num_frames=15)
```

## 📁 Output Structure

All output files are saved to: `./datasets/masked/`

### ✅ Example Directory Structure
```
./datasets/masked/
├── 9f23a1c1_1.png       # Extracted frame
├── 9f23a1c1_2.png       # Extracted frame
├── eye1_mask.png        # Mask created from annotate tool
```

## 🙋 Need Help?

For issues or enhancement requests (e.g., specific formats or automation), please:
- Open an issue
- Reach out to the maintainers