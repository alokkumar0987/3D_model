# 3D_model


markdown
# 3D Model Generator Assignment

## 📌 Overview
A Python tool that converts:
- **Images** → 3D models via edge detection
- **Text prompts** → 3D shapes using primitive combinations

## 📂 Files Included

/3D_Model_Generator
│── app.py               # Main Streamlit application
│── requirements.txt     # Dependency list
│── /samples            # Example files
│   ├── chair.jpg       # Sample input image
│   └── car.stl        # Sample output



## 🚀 How to Run
1. **Install dependencies**:
   bash
   pip install -r requirements.txt
   

2. **Launch the app**:
   bash
   streamlit run app.py
   

## 🛠 Features
| Input Type | Processing | Output |
|------------|------------|--------|
| Image (JPG/PNG) | Background removal + edge extrusion | `.stl` file |
| Text prompt | Primitive shape generation | `.stl` file |

## 💡 Examples
**1. Image to 3D**
python
Input: samples/chair.jpg → Output: chair.stl


**2. Text to 3D**
python
Input: "a small toy car" → Output: car.stl


## 📝 Assignment Requirements Checklist
Accepts both image and text input
Generates downloadable STL files
Includes visualization (Matplotlib)
  Python code with alok
Clear documentation


## ❓ Support
For issues, contact: [alok33778@gmail.com]


### Key Features:
1. *Clear Structure* - Separates overview, setup, examples
2. *Visual Indicators* - Uses emojis for better scanning
3. *Checklist* - Shows all requirements are met



