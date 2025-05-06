# 3D Model Generator



Convert images or text into 3D printable models using this interactive web application. Simply upload an image or describe the object you want, and the app will generate a 3D visualization and allow you to download it as an STL file for 3D printing.

## Features

-   *Image to 3D:* Upload PNG or JPG images, and the app will attempt to remove the background, detect edges, and generate a 3D mesh.
-   *Text to 3D:* Describe a simple object (like "car", "chair", "ball", "box", or "cylinder"), and the app will create a basic 3D model based on your description.
-   *Visualization:* The generated 3D model is displayed directly in the app using Matplotlib for easy viewing.
-   *STL Download:* Download the generated 3D model as an STL file, the standard format for 3D printing.
-   *Robust Error Handling:* The app includes fallbacks and error handling to provide a smoother experience even if certain processing steps fail.

## How to Use

1.  *Choose Input Type:* Select whether you want to upload an "Image" or provide "Text" as input.

    -   *Image:* Click on the "Upload image (PNG/JPG)" button to upload your image file. Once uploaded, you'll see a preview of the image. Click the "Generate 3D Model" button to start processing.
    -   *Text:* Enter a description of the 3D model you want in the text input field (e.g., "a small toy car"). Then, click the "Generate 3D Model" button.

2.  *View 3D Model:* After processing, a 3D visualization of the generated model will be displayed in the app. You can observe the shape and form of the model.

3.  *Download STL:* If you are satisfied with the generated model, click the "Download STL" button to save the model as a .stl file to your local machine. This file can then be used with 3D printing software.

## Installation

To run this application locally, you need to have Python installed on your system. Follow these steps:


    

2.  *Install the required Python libraries:*
    bash
    pip install streamlit opencv-python numpy rembg trimesh matplotlib Pillow
    

3.  *Run the Streamlit application:*
    bash
    streamlit run app.py

5.  The application will open automatically in your web browser (usually at http://localhost:8501).


![Screenshot of 3D Model Generator](![Screenshot 2025-05-03 233819](https://github.com/user-attachments/assets/55456ee0-395a-449d-964f-22c576b38ed2)
)

## Dependencies

-   *streamlit:* For creating the interactive web application.
-   *opencv-python:* For image processing tasks like edge detection.
-   *numpy:* For numerical operations on images and mesh data.
-   *rembg:* For removing the background from images.
-   *trimesh:* For creating and manipulating 3D meshes.
-   *matplotlib:* For visualizing the 3D mesh.
-   *Pillow (PIL):* For handling image loading.

## Notes and Tips

-   For image input, clear photos with distinct objects against plain backgrounds tend to yield better results for background removal and edge detection.
-   The text-to-3D functionality is based on simple keyword matching and generates basic shapes. More complex descriptions may not produce the desired results.
-   The 3D visualization uses Matplotlib, which provides a static view. You might not be able to interactively rotate the model within the Streamlit app using this method.
-   Error handling is included to manage potential issues during image processing or 3D conversion, providing informative messages within the app.

## Contributing

Contributions to this project are welcome. If you have suggestions for improvements, bug fixes, or new features, feel free to open an issue or submit a pull request.

## License

[Your License Information Here (e.g., MIT License)]





