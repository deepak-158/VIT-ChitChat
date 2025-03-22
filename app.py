import streamlit as st
import firebase_admin
from firebase_admin import credentials, db, storage
import time
import random
import string
import base64
from PIL import Image
import io

# Firebase Configuration
FIREBASE_URL = "https://vit-chitchat-36032-default-rtdb.firebaseio.com/"  # Change to your Firebase URL
FIREBASE_BUCKET = "vit-chitchat-36032.appspot.com"  # Change to your Firebase Storage bucket

# Initialize Firebase
if not firebase_admin._apps:
    import json
    import streamlit as st
    from firebase_admin import credentials
    cred = credentials.Certificate(st.secrets["firebase"])


    firebase_admin.initialize_app(cred, {
        'databaseURL': FIREBASE_URL,
        'storageBucket': FIREBASE_BUCKET
    })

# Reference to Firebase Database
chat_ref = db.reference("messages")

# Generate a Random Username
def generate_username():
    return "User_" + "".join(random.choices(string.ascii_letters + string.digits, k=5))

# Get Previous Messages from Firebase
@st.cache_data(ttl=10)
def get_messages():
    messages = chat_ref.get()
    return messages if messages else {}

# Upload Image to Firebase Storage and Get URL
def upload_image(image):
    bucket = storage.bucket()
    blob = bucket.blob(f"chat_images/{time.time()}.png")
    blob.upload_from_string(image, content_type="image/png")
    return blob.public_url  # Get the image URL

# Convert Image to Base64 for Firebase Storage
def encode_image(image):
    buffered = io.BytesIO()
    image.save(buffered, format="PNG")
    return base64.b64encode(buffered.getvalue()).decode()

# Streamlit UI
st.title("💬 VIT Anonymous Chat Room")

# Sidebar for Username
if "username" not in st.session_state:
    st.session_state["username"] = generate_username()

st.sidebar.write(f"**Your Username:** `{st.session_state['username']}`")
custom_username = st.sidebar.text_input("Set Custom Username", max_chars=15)
if custom_username:
    st.session_state["username"] = custom_username

# Display Chat Messages
st.subheader("📜 Chat History")
messages = get_messages()
for msg_id, msg_data in messages.items():
    username = msg_data.get("username", "Anonymous")
    text = msg_data.get("text", "")
    img_data = msg_data.get("image", None)

    st.write(f"**{username}**: {text}")
    
    # Show image if exists
    if img_data:
        image = Image.open(io.BytesIO(base64.b64decode(img_data)))
        st.image(image, caption="📷 Image", use_column_width=True)

# Chat Input
st.subheader("✍️ Send a Message")
message = st.text_input("Type your message here...")

# Image Upload Option
image_file = st.file_uploader("Upload an image (optional)", type=["png", "jpg", "jpeg"])

if st.button("Send"):
    if message or image_file:
        data = {
            "username": st.session_state["username"],
            "text": message,
            "timestamp": time.time()
        }
        
        # Handle image upload
        if image_file:
            image = Image.open(image_file)
            encoded_img = encode_image(image)
            data["image"] = encoded_img
        
        chat_ref.push(data)  # Store message in Firebase
        st.rerun()
  # Refresh chat

