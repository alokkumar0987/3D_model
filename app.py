import streamlit as st
import cv2
import numpy as np
from rembg import remove
import trimesh
import matplotlib.pyplot as plt
from PIL import Image
import os
import tempfile

# Configure environment for broader compatibility
os.environ["PYOPENGL_PLATFORM"] = "osmesa"  # Fallback for systems without GPU support

# Preprocess image: remove background and enhance edges
def preprocess_image(image):
    try:
        image = np.array(image.convert('RGB'))
        image = cv2.cvtColor(image, cv2.COLOR_RGB2BGR)
        
        # Background removal with fallback
        try:
            image_no_bg = remove(image)
        except:
            st.warning("Background removal failed. Using original image.")
            image_no_bg = image
        
        # Edge detection with adaptive thresholds
        gray = cv2.cvtColor(image_no_bg, cv2.COLOR_BGR2GRAY)
        gray = cv2.GaussianBlur(gray, (5, 5), 0)
        edges = cv2.Canny(gray, 50, 150)
        edges = cv2.dilate(edges, np.ones((3, 3), np.uint8))
        
        return edges, image_no_bg
    except Exception as e:
        st.error(f"Image processing error: {str(e)}")
        return None, None

# Convert edges to 3D mesh with multiple fallbacks
def image_to_3d(edges):
    try:
        # Check if edges contain any non-zero values
        if not np.any(edges):  # ← Explicit check
            st.warning("No edges detected. Using fallback shape.")
            return trimesh.creation.box(extents=[2, 2, 1])
        
        # Find contours
        contours, _ = cv2.findContours(
            edges.astype(np.uint8),  # ← Ensure correct dtype
            cv2.RETR_EXTERNAL,
            cv2.CHAIN_APPROX_SIMPLE
        )
        
        if not contours:  # ← This is safe (list check)
            st.warning("No contours found. Using fallback shape.")
            return trimesh.creation.box(extents=[2, 2, 1])
        
        # Rest of your processing...
        
    except Exception as e:
        st.error(f"3D conversion failed: {str(e)}")
        return trimesh.creation.box(extents=[2, 2, 1])  # Final fallback

# Enhanced text-to-3D with primitive shapes
def text_to_3d(prompt):
    prompt = prompt.lower()

    try:
        if any(word in prompt for word in ["car", "vehicle", "automobile"]):
            body = trimesh.creation.box(extents=[2, 1, 0.5])
            roof = trimesh.creation.box(extents=[1.5, 0.8, 0.5])
            roof.apply_translation([0, 0, 0.5])
            wheels = [trimesh.creation.cylinder(radius=0.2, height=0.2) for _ in range(4)]
            for i, wheel in enumerate(wheels):
                wheel.apply_translation([-0.8 if i < 2 else 0.8, -0.6 if i % 2 == 0 else 0.6, -0.2])
            return trimesh.util.concatenate([body, roof] + wheels)

        elif any(word in prompt for word in ["chair", "seat"]):
            seat = trimesh.creation.box(extents=[1, 1, 0.1])
            legs = [trimesh.creation.cylinder(radius=0.05, height=0.8) for _ in range(4)]
            for i, leg in enumerate(legs):
                x = -0.4 if i % 2 == 0 else 0.4
                y = -0.4 if i < 2 else 0.4
                leg.apply_translation([x, y, -0.8])
            back = trimesh.creation.box(extents=[0.1, 1, 1])
            back.apply_translation([0.5, 0, 0])
            return trimesh.util.concatenate([seat] + legs + [back])

        elif any(word in prompt for word in ["ball", "sphere", "round"]):
            return trimesh.creation.icosphere(radius=1)

        elif any(word in prompt for word in ["box", "cube", "block"]):
            return trimesh.creation.box(extents=[1, 1, 1])

        elif "cylinder" in prompt:
            return trimesh.creation.cylinder(radius=0.5, height=1)

        else:
            st.warning("Unknown object in prompt. Defaulting to cube.")
            return trimesh.creation.box(extents=[1, 1, 1])

    except Exception as e:
        st.error(f"Error generating 3D from text: {str(e)}")
        return trimesh.creation.box(extents=[1, 1, 1])

# Visualize with matplotlib (more reliable than pyrender)
def visualize_mesh(mesh):
    fig = plt.figure(figsize=(8, 6))
    ax = fig.add_subplot(111, projection='3d')
    
    try:
        if isinstance(mesh, trimesh.Trimesh):
            ax.plot_trisurf(
                mesh.vertices[:, 0],
                mesh.vertices[:, 1],
                mesh.vertices[:, 2],
                triangles=mesh.faces,
                shade=True,
                edgecolor='none'
            )
        else:
            # Fallback for path-based meshes
            for entity in mesh.entities:
                vertices = mesh.vertices[entity.points]
                ax.plot(vertices[:, 0], vertices[:, 1], vertices[:, 2])
    
    except Exception as e:
        st.error(f"Visualization error: {str(e)}")
        ax.text(0, 0, 0, "Could not render mesh", color='red')
    
    ax.set_xlabel('X')
    ax.set_ylabel('Y')
    ax.set_zlabel('Z')
    ax.view_init(elev=20, azim=45)
    return fig

# Streamlit UI
st.title("3D Model Generator")
st.write("Convert images or text into 3D printable models")

input_type = st.radio("Input type:", ["Image", "Text"])

if input_type == "Image":
    uploaded = st.file_uploader("Upload image (PNG/JPG)", type=["png", "jpg", "jpeg"])
    if uploaded:
        image = Image.open(uploaded)
        st.image(image, caption="Input Image", use_container_width=True)  # ← Updated
        
        if st.button("Generate 3D Model"):
            with st.spinner("Processing image..."):
                edges, processed_img = preprocess_image(image)
                
                if edges is not None:
                    st.image(edges, caption="Detected Edges", use_container_width=True)  # ← Updated
                    
                    mesh = image_to_3d(edges)
                    if mesh:
                        fig = visualize_mesh(mesh)
                        st.pyplot(fig)
                        
                        with tempfile.NamedTemporaryFile(suffix=".stl", delete=False) as tmp:
                            mesh.export(tmp.name)
                            with open(tmp.name, "rb") as f:
                                st.download_button(
                                    "Download STL",
                                    f,
                                    "model.stl",
                                    mime="application/octet-stream"
                                )
                        os.unlink(tmp.name)

elif input_type == "Text":
    prompt = st.text_input("Describe your 3D model (e.g., 'a small toy car')")
    if prompt and st.button("Generate 3D Model"):
        with st.spinner("Creating 3D model..."):
            mesh = text_to_3d(prompt)
            if mesh:
                fig = visualize_mesh(mesh)
                st.pyplot(fig)
                
                with tempfile.NamedTemporaryFile(suffix=".stl", delete=False) as tmp:
                    mesh.export(tmp.name)
                    with open(tmp.name, "rb") as f:
                        st.download_button(
                            "Download STL",
                            f,
                            "model.stl",
                            mime="application/octet-stream"
                        )
                os.unlink(tmp.name)

elif input_type == "Text":
    prompt = st.text_input("Describe your 3D model (e.g., 'a small toy car')")
    if prompt and st.button("Generate 3D Model"):
        with st.spinner("Creating 3D model..."):
            mesh = text_to_3d(prompt)
            if mesh:
                fig = visualize_mesh(mesh)
                st.pyplot(fig)
                
                with tempfile.NamedTemporaryFile(suffix=".stl", delete=False) as tmp:
                    mesh.export(tmp.name)
                    with open(tmp.name, "rb") as f:
                        st.download_button(
                            "Download STL",
                            f,
                            "model.stl",
                            mime="application/octet-stream"
                        )
                os.unlink(tmp.name)

st.markdown("---")
st.info("Tip: For best results with images, use clear photos with distinct objects against plain backgrounds.")
