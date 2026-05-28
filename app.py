import streamlit as st
import tensorflow as tf
from PIL import Image, ImageOps
import numpy as np

# Page Configuration for better GUI
st.set_page_config(
    page_title="Athleta Vision AI | Sports Category Detection",
    page_icon="🏆",
    layout="wide",
    initial_sidebar_state="expanded"
)

# Custom Cyberpunk Glassmorphism Theme CSS
st.markdown("""
    <style>
    @import url('https://fonts.googleapis.com/css2?family=Outfit:wght@300;400;600;800&display=swap');
    
    html, body, [data-testid="stAppViewContainer"] {
        background: linear-gradient(135deg, #0b0f19 0%, #151030 50%, #090616 100%);
        font-family: 'Outfit', sans-serif;
        color: #f1f5f9;
    }
    
    [data-testid="stHeader"] {
        background-color: rgba(0, 0, 0, 0);
    }
    
    [data-testid="stSidebar"] {
        background-color: #0d0c22 !important;
        border-right: 1px solid rgba(255, 255, 255, 0.05);
    }
    
    h1, h2, h3, h4, h5, h6 {
        font-family: 'Outfit', sans-serif;
        font-weight: 800;
        letter-spacing: -0.5px;
    }
    
    /* Neon Glowing Cards */
    .glass-card {
        background: rgba(255, 255, 255, 0.02);
        border: 1px solid rgba(255, 255, 255, 0.06);
        border-radius: 16px;
        padding: 24px;
        backdrop-filter: blur(12px);
        box-shadow: 0 8px 32px 0 rgba(0, 0, 0, 0.37);
        transition: all 0.3s ease;
        margin-bottom: 20px;
    }
    
    .glass-card:hover {
        border-color: rgba(0, 242, 254, 0.3);
        box-shadow: 0 8px 32px 0 rgba(0, 242, 254, 0.12);
        transform: translateY(-2px);
    }
    
    .glow-cyan {
        border-left: 5px solid #00f2fe;
    }
    
    .glow-magenta {
        border-left: 5px solid #ff007f;
    }
    
    .glow-green {
        border-left: 5px solid #39ff14;
    }
    
    /* Neon buttons styling override */
    div.stButton > button:first-child {
        background: linear-gradient(90deg, #00f2fe 0%, #4facfe 100%);
        border: none;
        color: white;
        font-weight: 700;
        border-radius: 8px;
        padding: 10px 20px;
        box-shadow: 0 4px 15px rgba(0, 242, 254, 0.3);
        transition: all 0.3s ease;
        text-transform: uppercase;
        letter-spacing: 1px;
        width: 100%;
    }
    
    div.stButton > button:first-child:hover {
        background: linear-gradient(90deg, #4facfe 0%, #00f2fe 100%);
        box-shadow: 0 4px 25px rgba(0, 242, 254, 0.5);
        transform: translateY(-1px);
        color: white;
        border: none;
    }
    
    /* Secondary Action Button (Clear) */
    div.stButton > button[key*="clear"] {
        background: rgba(255, 255, 255, 0.05);
        border: 1px solid rgba(255, 255, 255, 0.1);
        color: #f1f5f9;
        font-weight: 600;
    }
    div.stButton > button[key*="clear"]:hover {
        background: rgba(255, 255, 255, 0.1);
        border-color: rgba(255, 255, 255, 0.2);
        color: white;
    }
    
    /* Drag & Drop Area overrides */
    [data-testid="stFileUploader"] {
        border: 2px dashed rgba(0, 242, 254, 0.25);
        border-radius: 12px;
        background: rgba(255, 255, 255, 0.01);
        padding: 10px;
        transition: all 0.3s ease;
    }
    
    [data-testid="stFileUploader"]:hover {
        border-color: #00f2fe;
        background: rgba(0, 242, 254, 0.02);
    }
    
    /* Progress Bars styling */
    .custom-progress-container {
        width: 100%;
        background-color: rgba(255, 255, 255, 0.05);
        border-radius: 8px;
        margin: 8px 0 12px 0;
        height: 10px;
        overflow: hidden;
        border: 1px solid rgba(255, 255, 255, 0.05);
    }
    
    .custom-progress-bar {
        height: 100%;
        border-radius: 8px;
        background: linear-gradient(90deg, #00f2fe, #4facfe);
        box-shadow: 0 0 10px rgba(0, 242, 254, 0.4);
        transition: width 0.5s ease-in-out;
    }
    
    /* Quick Select Cards */
    .sample-img-card {
        border: 1px solid rgba(255, 255, 255, 0.06);
        border-radius: 12px;
        background: rgba(255, 255, 255, 0.01);
        padding: 8px;
        text-align: center;
        transition: all 0.2s ease;
    }
    
    .sample-img-card:hover {
        border-color: #00f2fe;
        background: rgba(0, 242, 254, 0.03);
    }
    
    /* Sport Grid Cards */
    .sport-grid-card {
        border: 1px solid rgba(255, 255, 255, 0.04);
        border-radius: 12px;
        background: rgba(255, 255, 255, 0.01);
        padding: 16px;
        text-align: center;
        transition: all 0.3s ease;
        height: 100%;
        min-height: 160px;
    }
    
    .sport-grid-card:hover {
        border-color: #ff007f;
        background: rgba(255, 0, 127, 0.03);
        transform: translateY(-4px);
        box-shadow: 0 6px 20px rgba(255, 0, 127, 0.1);
    }
    
    .sport-emoji {
        font-size: 36px;
        margin-bottom: 8px;
    }
    
    .sport-title {
        font-size: 16px;
        font-weight: 700;
        color: #f1f5f9;
        text-transform: uppercase;
        margin-bottom: 4px;
    }
    
    .sport-cat {
        font-size: 10px;
        font-weight: 600;
        color: #cbd5e1;
        background: rgba(255, 255, 255, 0.08);
        padding: 2px 8px;
        border-radius: 12px;
        display: inline-block;
    }
    
    /* Active Tab indicator styles */
    .stTabs [data-baseweb="tab-list"] {
        gap: 8px;
        background-color: rgba(255, 255, 255, 0.01);
        padding: 6px;
        border-radius: 12px;
        border: 1px solid rgba(255, 255, 255, 0.05);
    }

    .stTabs [data-baseweb="tab"] {
        height: 45px;
        border-radius: 8px;
        color: #94a3b8;
        font-weight: 600;
        background-color: transparent;
        transition: all 0.2s ease;
    }

    .stTabs [aria-selected="true"] {
        color: #00f2fe !important;
        background-color: rgba(0, 242, 254, 0.08) !important;
        border: 1px solid rgba(0, 242, 254, 0.2) !important;
    }
    
    /* Image caption customization */
    .stImage > div > p {
        color: #94a3b8 !important;
        font-style: italic;
    }
    </style>
    """, unsafe_allow_html=True)

# 1. Load Model (Cache it to avoid reloading every time)
@st.cache_resource
def load_my_model():
    model_path = 'my_sports_classifier.h5'
    model = tf.keras.models.load_model(model_path)
    return model

# 2. Define Classes (As per your notebook)
CLASS_NAMES = [
    'badminton', 'baseball', 'basketball', 'boxing', 'chess', 
    'cricket', 'fencing', 'football', 'formula1', 'gymnastics', 
    'hockey', 'ice_hockey', 'kabaddi', 'motogp', 'shooting', 
    'swimming', 'table_tennis', 'tennis', 'volleyball', 
    'weight_lifting', 'wrestling', 'wwe'
]

# Detailed Sports Metadata for premium GUI elements
SPORTS_DETAILS = {
    'badminton': {'emoji': '🏸', 'category': 'Racket Sports', 'description': 'Fast-paced sport played with rackets and a shuttlecock over a net.'},
    'baseball': {'emoji': '⚾', 'category': 'Team Sports', 'description': 'Popular bat-and-ball sport played between two teams of nine players.'},
    'basketball': {'emoji': '🏀', 'category': 'Team Sports', 'description': 'Played by two teams of five players on a rectangular court trying to shoot a basketball.'},
    'boxing': {'emoji': '🥊', 'category': 'Combat Sports', 'description': 'Combat sport in which two people wearing protective gloves throw punches at each other.'},
    'chess': {'emoji': '♟️', 'category': 'Mind Sports', 'description': 'An abstract strategic two-player board game played on a checkered board.'},
    'cricket': {'emoji': '🏏', 'category': 'Team Sports', 'description': 'Bat-and-ball game played between two teams of eleven players on a circular field.'},
    'fencing': {'emoji': '🤺', 'category': 'Combat Sports', 'description': 'Elegant combat sport using bladed weapons (foil, épée, or sabre) for scoring points.'},
    'football': {'emoji': '⚽', 'category': 'Team Sports', 'description': 'The world\'s most popular sport, played between two teams of eleven players with a spherical ball.'},
    'formula1': {'emoji': '🏎️', 'category': 'Motorsports', 'description': 'The highest class of single-seater auto racing sanctioned by the FIA.'},
    'gymnastics': {'emoji': '🤸', 'category': 'Precision Sports', 'description': 'Exercises requiring physical strength, flexibility, power, agility, and balance.'},
    'hockey': {'emoji': '🏑', 'category': 'Team Sports', 'description': 'Field game played on grass or turf with a curved stick and a small hard ball.'},
    'ice_hockey': {'emoji': '🏒', 'category': 'Team Sports', 'description': 'Fast contact team sport played on ice skates on a flat ice rink with a puck.'},
    'kabaddi': {'emoji': '🤼‍♂️', 'category': 'Combat Sports', 'description': 'Traditional contact sport of Indian origin played by teams tagging and escaping defenders.'},
    'motogp': {'emoji': '🏍️', 'category': 'Motorsports', 'description': 'The premier class of motorcycle road racing events held on road circuits.'},
    'shooting': {'emoji': '🎯', 'category': 'Precision Sports', 'description': 'Precise shooting sport involving accuracy, speed, and focus using target firearms.'},
    'swimming': {'emoji': '🏊', 'category': 'Water Sports', 'description': 'Individual or team racing sport utilizing various swimming strokes in a pool.'},
    'table_tennis': {'emoji': '🏓', 'category': 'Racket Sports', 'description': 'Also known as ping-pong, played on a hard table divided by a net using small paddles.'},
    'tennis': {'emoji': '🎾', 'category': 'Racket Sports', 'description': 'Racket sport played individually against a single opponent or between two teams of two.'},
    'volleyball': {'emoji': '🏐', 'category': 'Team Sports', 'description': 'Played by two teams of six players on a court separated by a net, scoring by grounding the ball.'},
    'weight_lifting': {'emoji': '🏋️', 'category': 'Strength Sports', 'description': 'Athletes attempt to lift extreme weights on a barbell loaded with plates.'},
    'wrestling': {'emoji': '🤼', 'category': 'Combat Sports', 'description': 'Grappling physical combat sport involving clinches, throws, and pins.'},
    'wwe': {'emoji': '👑', 'category': 'Combat Sports', 'description': 'Professional theatrical entertainment wrestling featuring athletics and storylines.'}
}

# Load the model
try:
    model = load_my_model()
    model_loaded = True
except Exception as e:
    model_loaded = False
    st.sidebar.error(f"Error loading model: {e}")

# ================= SIDEBAR SETUP =================
st.sidebar.markdown("""
<div style='text-align: center; padding: 10px 0;'>
    <h1 style='color: #00f2fe; margin-bottom: 0; font-size: 28px; font-weight: 800; letter-spacing: 1px;'>🔮 ATHLETA AI</h1>
    <p style='color: #94a3b8; font-size: 13px; margin-top: 5px; font-weight: 600; text-transform: uppercase; letter-spacing: 2px;'>Sports Detector</p>
</div>
<hr style='border-color: rgba(255,255,255,0.05); margin-top: 5px; margin-bottom: 15px;' />
""", unsafe_allow_html=True)

# Model Specs card in sidebar
st.sidebar.markdown("""
<div class='glass-card glow-magenta' style='padding: 16px; margin-bottom: 20px;'>
    <h4 style='color: #ff007f; margin: 0 0 12px 0; font-size: 15px; font-weight: 700; text-transform: uppercase;'>⚙️ Model Diagnostics</h4>
    <div style='font-size: 13px; line-height: 1.8;'>
        <p style='margin: 4px 0;'><b>Model File:</b> <code style='color: #ff007f;'>classifier.h5</code></p>
        <p style='margin: 4px 0;'><b>Input Shape:</b> 224 × 224 × 3 (RGB)</p>
        <p style='margin: 4px 0;'><b>Total Categories:</b> 22 Sports</p>
        <p style='margin: 4px 0;'><b>Framework:</b> TensorFlow 2.x</p>
    </div>
</div>
""", unsafe_allow_html=True)

# Supported Sports Directory in sidebar
with st.sidebar.expander("📂 Supported Sports Grid (22 Classes)", expanded=False):
    st.markdown("""
    <div style='font-size: 12px; line-height: 1.6; color: #cbd5e1;'>
        <b style='color: #00f2fe;'>🏟️ Team:</b> Baseball, Basketball, Cricket, Football, Hockey, Ice Hockey, Volleyball<br>
        <b style='color: #ff007f;'>🥊 Combat:</b> Boxing, Fencing, Kabaddi, Wrestling, WWE<br>
        <b style='color: #39ff14;'>🏸 Racket:</b> Badminton, Table Tennis, Tennis<br>
        <b style='color: #ffaa00;'>🎯 Precision:</b> Gymnastics, Shooting, Weight Lifting<br>
        <b style='color: #00aaff;'>🏊 Water/Mind:</b> Chess, Swimming<br>
        <b style='color: #b975ff;'>🏎️ Motor:</b> Formula 1, MotoGP
    </div>
    """, unsafe_allow_html=True)

st.sidebar.markdown("""
<div style='position: fixed; bottom: 15px; width: 220px; font-size: 11px; color: #64748b;'>
    <hr style='border-color: rgba(255,255,255,0.03); margin-bottom: 10px;' />
    Athleta Vision AI Dashboard v2.0<br/>
    Built using Streamlit & TensorFlow
</div>
""", unsafe_allow_html=True)


# ================= MAIN PAGE SETUP =================
st.markdown("<h1 style='color: #00f2fe; margin-bottom: 5px; font-size: 40px;'>🏟️ Athleta Vision AI Dashboard</h1>", unsafe_allow_html=True)
st.markdown("<p style='color: #94a3b8; font-size: 16px; margin-bottom: 25px;'>Analyze sports photography in real-time. Upload an image or select a sample image to classify the sport instantly!</p>", unsafe_allow_html=True)

# Tabs
tab_predictor, tab_explorer, tab_diagnostics = st.tabs([
    "🔮 AI Sports Predictor", 
    "📊 Category Explorer", 
    "⚙️ Pipeline Diagnostics"
])

# Initialize session state variables
if 'selected_image' not in st.session_state:
    st.session_state.selected_image = None
if 'image_source' not in st.session_state:
    st.session_state.image_source = None
if 'last_prediction' not in st.session_state:
    st.session_state.last_prediction = None
if 'last_image_name' not in st.session_state:
    st.session_state.last_image_name = None
if 'run_analysis' not in st.session_state:
    st.session_state.run_analysis = False
if 'balloon_shown_for' not in st.session_state:
    st.session_state.balloon_shown_for = None

# Reset function
def reset_app():
    st.session_state.selected_image = None
    st.session_state.image_source = None
    st.session_state.last_prediction = None
    st.session_state.last_image_name = None
    st.session_state.run_analysis = False


# ================= TAB 1: PREDICTOR =================
with tab_predictor:
    col_left, col_right = st.columns([1.2, 1.0])
    
    with col_left:
        st.markdown("<h3 style='color: #00f2fe; margin-bottom: 15px;'>📤 Step 1: Upload or Choose Image</h3>", unsafe_allow_html=True)
        
        # File uploader inside glass card
        st.markdown("<div class='glass-card glow-cyan' style='padding: 20px;'>", unsafe_allow_html=True)
        uploaded_file = st.file_uploader(
            "Drag & drop a sports image (JPG, PNG, JFIF)", 
            type=["jpg", "jpeg", "png", "jfif"], 
            key="uploader"
        )
        st.markdown("</div>", unsafe_allow_html=True)
        
        # Quick Select Section
        st.markdown("<div style='text-align: center; margin: 20px 0; color: #64748b; font-weight: 600; font-size: 13px; letter-spacing: 1px;'>— OR TEST WITH SAMPLES —</div>", unsafe_allow_html=True)
        
        col_s1, col_s2 = st.columns(2)
        with col_s1:
            st.markdown("<div class='sample-img-card'>", unsafe_allow_html=True)
            st.image("1.jfif", caption="Sample 1 (Badminton)", use_container_width=True)
            if st.button("Load Sample 1", key="btn_s1", use_container_width=True):
                st.session_state.selected_image = "1.jfif"
                st.session_state.image_source = "sample"
                st.session_state.last_prediction = None
                st.session_state.run_analysis = True
            st.markdown("</div>", unsafe_allow_html=True)
            
        with col_s2:
            st.markdown("<div class='sample-img-card'>", unsafe_allow_html=True)
            st.image("2.jfif", caption="Sample 2 (Tennis)", use_container_width=True)
            if st.button("Load Sample 2", key="btn_s2", use_container_width=True):
                st.session_state.selected_image = "2.jfif"
                st.session_state.image_source = "sample"
                st.session_state.last_prediction = None
                st.session_state.run_analysis = True
            st.markdown("</div>", unsafe_allow_html=True)

    # Listen to new file upload
    if uploaded_file is not None:
        if st.session_state.image_source != "uploaded" or st.session_state.last_image_name != uploaded_file.name:
            st.session_state.selected_image = uploaded_file
            st.session_state.image_source = "uploaded"
            st.session_state.last_prediction = None
            st.session_state.run_analysis = False

    # Extract info of loaded image
    current_image = None
    image_name = ""
    
    if st.session_state.selected_image is not None:
        try:
            if st.session_state.image_source == "sample":
                current_image = Image.open(st.session_state.selected_image).convert('RGB')
                image_name = st.session_state.selected_image
            else:
                current_image = Image.open(st.session_state.selected_image).convert('RGB')
                image_name = st.session_state.selected_image.name
        except Exception as e:
            st.error(f"Error loading image: {e}")

    with col_right:
        st.markdown("<h3 style='color: #ff007f; margin-bottom: 15px;'>👁️ Preview & Pipeline Control</h3>", unsafe_allow_html=True)
        if current_image is not None:
            st.markdown("<div class='glass-card glow-magenta' style='text-align: center;'>", unsafe_allow_html=True)
            st.image(current_image, caption=f"Selected File: {image_name}", use_container_width=True)
            
            st.markdown("<div style='margin-top: 15px;'></div>", unsafe_allow_html=True)
            
            # Action controls
            col_act1, col_act2 = st.columns(2)
            with col_act1:
                # If prediction is already cached, show it was run, otherwise highlight predict button
                predict_label = "🔮 Re-Analyze Sport" if st.session_state.last_prediction is not None else "🔮 Predict Sport"
                if st.button(predict_label, key="btn_predict", use_container_width=True):
                    st.session_state.run_analysis = True
            with col_act2:
                if st.button("❌ Clear Workspace", key="btn_clear", use_container_width=True):
                    reset_app()
                    st.rerun()
            st.markdown("</div>", unsafe_allow_html=True)
        else:
            st.markdown("""
            <div class='glass-card glow-magenta' style='text-align: center; padding: 60px 20px; color: #94a3b8;'>
                <div style='font-size: 54px; margin-bottom: 20px;'>📸</div>
                <h4 style='color: #ff007f; font-weight: 700; margin-bottom: 8px;'>No Image Loaded</h4>
                <p style='font-size: 14px;'>Upload an image on the left panel or click one of the quick test sample images to begin real-time AI classification.</p>
            </div>
            """, unsafe_allow_html=True)

    # ================= RUN PREDICTION AND DISPLAY =================
    if current_image is not None and model_loaded:
        # Check if we should execute model prediction
        if st.session_state.run_analysis or (st.session_state.last_prediction is None and st.session_state.image_source == "uploaded"):
            with st.spinner("Analyzing image features & running inference..."):
                try:
                    # 1. Preprocessing matching original notebook pipeline
                    size = (224, 224)
                    image_resized = ImageOps.fit(current_image, size, Image.LANCZOS)
                    img_array = np.asarray(image_resized)
                    
                    # 2. Rescale pixel values
                    img_array_scaled = img_array.astype('float32') / 255.0
                    
                    # 3. Expand batch dimension
                    img_reshape = img_array_scaled[np.newaxis, ...]
                    
                    # 4. Predict
                    prediction = model.predict(img_reshape)
                    
                    # 5. Cache results
                    st.session_state.last_prediction = prediction
                    st.session_state.last_image_name = image_name
                    st.session_state.run_analysis = False
                    st.rerun()
                except Exception as e:
                    st.error(f"Inference process error: {e}")
                    st.session_state.run_analysis = False

        # Display cached prediction results
        if st.session_state.last_prediction is not None:
            prediction = st.session_state.last_prediction
            
            # Sort prediction results
            idx = np.argmax(prediction[0])
            predicted_class = CLASS_NAMES[idx]
            confidence = 100 * prediction[0][idx]
            
            # Get Top 3 categories
            top_3_idx = np.argsort(prediction[0])[-3:][::-1]
            top_3_classes = [CLASS_NAMES[i] for i in top_3_idx]
            top_3_confidences = [100 * prediction[0][i] for i in top_3_idx]
            
            # Sport details matching the predicted class
            sport_info = SPORTS_DETAILS.get(predicted_class, {'emoji': '🏆', 'category': 'Sports', 'description': 'Sports category detected'})
            emoji = sport_info['emoji']
            category = sport_info['category']
            description = sport_info['description']
            
            st.markdown("<hr style='border-color: rgba(255,255,255,0.05); margin: 30px 0 20px 0;' />", unsafe_allow_html=True)
            st.markdown("<h2 style='color: #39ff14; text-align: center; margin-bottom: 25px; font-weight: 800; letter-spacing: 0.5px;'>🎯 AI Classifier Results</h2>", unsafe_allow_html=True)
            
            col_res1, col_res2 = st.columns(2)
            
            with col_res1:
                st.markdown(f"""
                <div class='glass-card glow-green' style='text-align: center; padding: 30px; height: 100%; display: flex; flex-direction: column; justify-content: center; align-items: center;'>
                    <div style='font-size: 72px; margin-bottom: 12px;'>{emoji}</div>
                    <span class='sport-cat' style='font-size: 12px; font-weight: bold; letter-spacing: 1px; padding: 4px 16px; margin-bottom: 12px;'>{category.upper()}</span>
                    <h1 style='color: #39ff14; font-size: 42px; font-weight: 800; margin: 5px 0 10px 0; text-transform: uppercase;'>{predicted_class.replace('_', ' ')}</h1>
                    <p style='color: #cbd5e1; font-size: 15px; max-width: 90%; margin: 10px auto 20px auto; line-height: 1.6;'>{description}</p>
                    <div style='background: rgba(57, 255, 20, 0.04); border: 1px dashed rgba(57, 255, 20, 0.25); border-radius: 12px; padding: 14px 28px; width: 80%; margin: 0 auto;'>
                        <span style='color: #39ff14; font-size: 16px; font-weight: 800;'>🌟 CONFIDENCE SCORE: {confidence:.2f}%</span>
                    </div>
                </div>
                """, unsafe_allow_html=True)
                
            with col_res2:
                st.markdown("<div class='glass-card glow-cyan' style='padding: 30px; height: 100%;'>", unsafe_allow_html=True)
                st.markdown("<h3 style='color: #00f2fe; margin-top: 0; font-size: 20px; font-weight: 700; text-transform: uppercase;'>📊 Class Probability Distribution</h3>", unsafe_allow_html=True)
                st.markdown("<p style='font-size: 13px; color: #94a3b8; margin-bottom: 20px;'>Below is the distribution of the top 3 categories competing for this image:</p>", unsafe_allow_html=True)
                
                for i, (cls, conf) in enumerate(zip(top_3_classes, top_3_confidences)):
                    cls_info = SPORTS_DETAILS.get(cls, {'emoji': '🏆', 'category': 'General'})
                    cls_emoji = cls_info['emoji']
                    cls_cat = cls_info['category']
                    
                    # Gradient colors for top match vs runner ups
                    bar_color = "linear-gradient(90deg, #39ff14 0%, #00f2fe 100%)" if i == 0 else "linear-gradient(90deg, #00f2fe 0%, #4facfe 100%)"
                    text_color = "#39ff14" if i == 0 else "#00f2fe"
                    
                    st.markdown(f"""
                        <div style='margin-bottom: 20px;'>
                            <div style='display: flex; justify-content: space-between; align-items: center; font-weight: 600; font-size: 15px;'>
                                <span>{cls_emoji} <b style='text-transform: uppercase;'>{cls.replace('_', ' ')}</b> <span style='font-size: 11px; font-weight: normal; color: #64748b; margin-left: 5px;'>({cls_cat})</span></span>
                                <span style='color: {text_color}; font-weight: 700;'>{conf:.2f}%</span>
                            </div>
                            <div class='custom-progress-container' style='height: 12px; margin-top: 6px;'>
                                <div class='custom-progress-bar' style='width: {conf}%; background: {bar_color};'></div>
                            </div>
                        </div>
                    """, unsafe_allow_html=True)
                st.markdown("</div>", unsafe_allow_html=True)
                
            # Trigger party balloons on high accuracy predictions once!
            if confidence > 90.0 and st.session_state.balloon_shown_for != image_name:
                st.balloons()
                st.session_state.balloon_shown_for = image_name
            elif confidence < 50.0:
                st.markdown("""
                <div style='margin-top: 20px;'>
                    <div style='background: rgba(255, 170, 0, 0.06); border: 1px solid rgba(255, 170, 0, 0.2); border-radius: 12px; padding: 16px; color: #ffaa00; font-size: 13.5px; line-height: 1.6;'>
                        ⚠️ <b>Prediction Advisory Note:</b> The model returned a low confidence score (< 50%) for this classification. This often happens if the photo contains complex action backgrounds, multiple athletes, or low resolution. For peak results, we recommend uploading high-contrast, focused pictures of a single sport category.
                    </div>
                </div>
                """, unsafe_allow_html=True)


# ================= TAB 2: EXPLORER =================
with tab_explorer:
    st.markdown("<h2 style='color: #ff007f; text-align: center; margin-bottom: 10px; font-size: 32px;'>📊 AI Sports Categories Catalog</h2>", unsafe_allow_html=True)
    st.markdown("<p style='text-align: center; color: #94a3b8; font-size: 15px; margin-bottom: 35px;'>Browse all 22 classes recognized by Athleta AI. These categories are trained to evaluate specific body postures, equipment types, and field structures.</p>", unsafe_allow_html=True)
    
    # Sort classes alphabetically
    sorted_sports = sorted(list(SPORTS_DETAILS.keys()))
    
    # Grid of 4 columns
    cols = st.columns(4)
    for index, sport in enumerate(sorted_sports):
        col_index = index % 4
        details = SPORTS_DETAILS[sport]
        
        with cols[col_index]:
            st.markdown(f"""
            <div class='sport-grid-card'>
                <div class='sport-emoji'>{details['emoji']}</div>
                <div class='sport-title'>{sport.replace('_', ' ')}</div>
                <div class='sport-cat'>{details['category'].upper()}</div>
                <p style='color: #94a3b8; font-size: 12px; margin-top: 10px; line-height: 1.5;'>{details['description']}</p>
            </div>
            <div style='margin-bottom: 20px;'></div>
            """, unsafe_allow_html=True)


# ================= TAB 3: DIAGNOSTICS =================
with tab_diagnostics:
    st.markdown("<h2 style='color: #39ff14; text-align: center; margin-bottom: 10px; font-size: 32px;'>⚙️ Model Pipeline Diagnostics</h2>", unsafe_allow_html=True)
    st.markdown("<p style='text-align: center; color: #94a3b8; font-size: 15px; margin-bottom: 35px;'>Understand how the TensorFlow model analyzes raw imagery using standard pre-processing transformations.</p>", unsafe_allow_html=True)
    
    col_diag1, col_diag2 = st.columns([1.1, 0.9])
    
    with col_diag1:
        st.markdown("""
        <div class='glass-card glow-green' style='height: 100%;'>
            <h3 style='color: #39ff14; font-size: 20px; font-weight: 700; margin-top: 0;'>🔄 Pre-Processing Pipeline Details</h3>
            <p style='font-size: 14px; line-height: 1.6; color: #cbd5e1;'>
                A convolutional neural network expects highly structured data that replicates the format of its training set. To ensure predictions are highly accurate, this app transforms any uploaded image on the fly:
            </p>
            <div style='font-size: 14px; line-height: 1.8; color: #cbd5e1;'>
                <b style='color: #39ff14;'>1. Channel Alignment (RGB Mode)</b><br/>
                Modern pictures can sometimes contain an alpha (transparency) channel (PNG) or uses alternate CMYK arrays. The image is parsed and converted to raw three-channel <code>RGB</code> mode immediately to avoid shape errors.<br/><br/>
                <b style='color: #39ff14;'>2. Spatial Normalization (LANCZOS Resizing)</b><br/>
                The model is trained strictly on <code>224 x 224 pixel</code> arrays. We crop and resize the image using Streamlit's <code>ImageOps.fit</code> and high-grade <code>LANCZOS</code> interpolation to minimize pixel aliasing and retain structural features.<br/><br/>
                <b style='color: #39ff14;'>3. Numerical Rescaling (1./255.0)</b><br/>
                Neural network weights operate best on normalized values. Color integers ranging from 0-255 are mapped to floating-point ratios between <code>0.0</code> and <code>1.0</code>.<br/><br/>
                <b style='color: #39ff14;'>4. Tensor Batch Extension</b><br/>
                The Keras model expects a batches tensor input (usually <code>(batch_size, width, height, channels)</code>). We expand the array shape from <code>(224, 224, 3)</code> to <code>(1, 224, 224, 3)</code> using numpy expansion prior to running model inference.
            </div>
        </div>
        """, unsafe_allow_html=True)
        
    with col_diag2:
        st.markdown("<div class='glass-card glow-cyan' style='height: 100%;'>", unsafe_allow_html=True)
        st.markdown("<h3 style='color: #00f2fe; font-size: 20px; font-weight: 700; margin-top: 0;'>🐍 Python Pipeline Implementation</h3>", unsafe_allow_html=True)
        st.markdown("<p style='font-size: 13.5px; color: #94a3b8;'>This is the exact sequence of processing functions implemented in the backend logic of Athleta AI:</p>", unsafe_allow_html=True)
        
        st.code("""
# 1. Align color channels to standard RGB
image_rgb = Image.open(uploaded_file).convert('RGB')

# 2. Resize spatial bounds to 224 x 224
target_size = (224, 224)
image_resized = ImageOps.fit(
    image_rgb, 
    target_size, 
    Image.Resampling.LANCZOS
)

# 3. Scale uint8 array to float32 ratio
img_array = np.asarray(image_resized)
img_scaled = img_array.astype('float32') / 255.0

# 4. Form 4D batch tensor (1, 224, 224, 3)
img_tensor = img_scaled[np.newaxis, ...]

# 5. Model Inference
predictions = model.predict(img_tensor)
        """, language="python")
        st.markdown("</div>", unsafe_allow_html=True)