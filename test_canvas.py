"""
MINIMAL TEST APP - Save as test_canvas.py

Run this simple app to test if your canvas can display backgrounds at all.
This will help isolate whether the issue is with your image or the canvas setup.

To run:
1. Save this file as test_canvas.py
2. Run: streamlit run test_canvas.py
3. Check if you see colored backgrounds in the canvases
"""

import streamlit as st
from streamlit_drawable_canvas import st_canvas
from PIL import Image
import numpy as np

st.set_page_config(page_title="Canvas Background Test")
st.title("🧪 Canvas Background Test")

st.markdown("### Test 1: Simple Colored Background")
st.write("You should see a RED background:")

# Test 1: Simple colored image
test_img_1 = Image.new('RGB', (800, 400), color='red')
canvas1 = st_canvas(
    fill_color="rgba(0, 255, 0, 0.3)",
    stroke_width=2,
    background_image=test_img_1,
    height=400,
    width=800,
    drawing_mode="circle",
    key="test1"
)

if canvas1.image_data is not None:
    st.success("✅ Test 1 PASSED - Canvas accepts simple background")
else:
    st.error("❌ Test 1 FAILED - Canvas not accepting backgrounds")

st.markdown("---")
st.markdown("### Test 2: Gradient Background")
st.write("You should see a GRADIENT background (blue to green):")

# Test 2: Gradient image
gradient = np.zeros((400, 800, 3), dtype=np.uint8)
for i in range(800):
    gradient[:, i, 0] = 0  # Red channel
    gradient[:, i, 1] = int((i / 800) * 255)  # Green channel (gradient)
    gradient[:, i, 2] = int(255 - (i / 800) * 255)  # Blue channel (gradient)

test_img_2 = Image.fromarray(gradient, 'RGB')
canvas2 = st_canvas(
    fill_color="rgba(255, 0, 0, 0.3)",
    stroke_width=2,
    background_image=test_img_2,
    height=400,
    width=800,
    drawing_mode="rect",
    key="test2"
)

if canvas2.image_data is not None:
    st.success("✅ Test 2 PASSED - Canvas handles generated images")
else:
    st.error("❌ Test 2 FAILED")

st.markdown("---")
st.markdown("### Test 3: Your Actual Image")

uploaded_file = st.file_uploader("Upload your Training_base_map.png", type=['png', 'jpg', 'jpeg'])

if uploaded_file is not None:
    try:
        # Load the user's image
        user_img = Image.open(uploaded_file)
        
        # Show info
        st.write(f"Original image - Size: {user_img.size}, Mode: {user_img.mode}")
        
        # Resize to 800 wide
        target_width = 800
        scale = target_width / user_img.width
        scaled_height = int(user_img.height * scale)
        resized_img = user_img.resize((target_width, scaled_height))
        
        # Force RGB
        if resized_img.mode != 'RGB':
            st.warning(f"Converting from {resized_img.mode} to RGB")
            resized_img = resized_img.convert('RGB')
        
        st.write(f"Resized image - Size: {resized_img.size}, Mode: {resized_img.mode}")
        
        # Show preview
        st.image(resized_img, caption="Your image (preview)", use_container_width=True)
        
        # Try in canvas
        st.write("Your image in canvas (should show as background):")
        
        canvas3 = st_canvas(
            fill_color="rgba(255, 255, 0, 0.3)",
            stroke_width=2,
            background_image=resized_img,
            height=scaled_height,
            width=target_width,
            drawing_mode="polygon",
            key="test3"
        )
        
        if canvas3.image_data is not None:
            st.success("✅ Test 3 PASSED - Your image works in canvas!")
            st.info("✓ Problem is likely in your main app.py configuration")
        else:
            st.error("❌ Test 3 FAILED - Your image has issues")
            st.warning("Try a different image or check the format")
            
    except Exception as e:
        st.error(f"Error loading your image: {e}")

st.markdown("---")
st.markdown("### Test 4: Alternative Method")
st.write("Testing with numpy array conversion:")

if uploaded_file is not None:
    try:
        user_img = Image.open(uploaded_file)
        target_width = 800
        scale = target_width / user_img.width
        scaled_height = int(user_img.height * scale)
        resized_img = user_img.resize((target_width, scaled_height))
        
        if resized_img.mode != 'RGB':
            resized_img = resized_img.convert('RGB')
        
        # Convert to numpy array and back
        img_array = np.array(resized_img)
        img_from_array = Image.fromarray(img_array.astype('uint8'), 'RGB')
        
        st.write("Image from numpy array:")
        canvas4 = st_canvas(
            fill_color="rgba(0, 255, 255, 0.3)",
            stroke_width=2,
            background_image=img_from_array,
            height=scaled_height,
            width=target_width,
            drawing_mode="circle",
            key="test4"
        )
        
        if canvas4.image_data is not None:
            st.success("✅ Test 4 PASSED - Numpy conversion works")
        else:
            st.error("❌ Test 4 FAILED")
    except Exception as e:
        st.error(f"Error: {e}")

st.markdown("---")
st.markdown("### Diagnosis")

if canvas1.image_data is None:
    st.error("""
    ❌ **MAJOR ISSUE**: Canvas cannot display ANY backgrounds
    
    This suggests:
    - streamlit-drawable-canvas installation issue
    - Version incompatibility
    - Browser issue
    
    Try:
    1. Update streamlit-drawable-canvas: `pip install streamlit-drawable-canvas --upgrade`
    2. Clear browser cache
    3. Try different browser
    4. Check version compatibility
    """)
elif uploaded_file is None:
    st.info("📤 Upload your Training_base_map.png above to test it")
elif canvas3.image_data is None:
    st.error("""
    ❌ **IMAGE ISSUE**: Simple backgrounds work, but your image doesn't
    
    Your image might have:
    - Incompatible format
    - Corruption
    - Wrong color mode
    - Size issues
    
    Try:
    1. Convert to standard RGB PNG
    2. Reduce file size
    3. Use image editing software to re-save
    """)
else:
    st.success("""
    ✅ **ALL TESTS PASSED**
    
    Your image works fine! The issue is in your main app.py configuration.
    
    Check:
    1. How you're loading the image
    2. Variable names and passing to canvas
    3. Canvas key uniqueness
    4. State management
    """)

st.markdown("---")
st.markdown("### System Info")
st.write(f"Streamlit version: {st.__version__}")
try:
    import streamlit_drawable_canvas
    st.write(f"Canvas version: {streamlit_drawable_canvas.__version__}")
except:
    st.write("Canvas version: Unable to determine")
