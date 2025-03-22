import streamlit as st
import firebase_admin
from firebase_admin import credentials, db, storage
import time
import random
import string
import base64
from PIL import Image
import io

# Initialize Firebase with Streamlit Secrets
firebase_secrets = st.secrets["firebase"]

if not firebase_admin._apps:
    cred = credentials.Certificate(dict(firebase_secrets))
    firebase_admin.initialize_app(cred, {
        'databaseURL': firebase_secrets["databaseURL"],
        'storageBucket': firebase_secrets["storageBucket"]
    })

# Firebase References
chat_ref = db.reference("messages")
rooms_ref = db.reference("chatrooms")

# Generate a Random Username
def generate_username():
    return "User_" + "".join(random.choices(string.ascii_letters + string.digits, k=5))

# Get Messages from Firebase
@st.cache_data(ttl=10)
def get_messages(room):
    messages = db.reference(f"messages/{room}").get()
    return messages if messages else {}

# Get Available Chat Rooms
@st.cache_data(ttl=10)
def get_chatrooms():
    rooms = rooms_ref.get()
    return rooms if rooms else {}

# Upload Image to Firebase Storage
def upload_image(image):
    bucket = storage.bucket()
    blob = bucket.blob(f"chat_images/{time.time()}.png")
    blob.upload_from_string(image, content_type="image/png")
    return blob.public_url

# Convert Image to Base64 for Firebase Storage
def encode_image(image):
    buffered = io.BytesIO()
    image.save(buffered, format="PNG")
    return base64.b64encode(buffered.getvalue()).decode()

# Streamlit UI
st.title("💬 VIT Anonymous Chat Room")

# Sidebar for Username and Room Selection
if "username" not in st.session_state:
    st.session_state["username"] = generate_username()

st.sidebar.write(f"**Your Username:** `{st.session_state['username']}`")
custom_username = st.sidebar.text_input("Set Custom Username", max_chars=15)
if custom_username:
    st.session_state["username"] = custom_username

# Select or Create Chat Room
st.sidebar.subheader("🔹 Select a Chat Room")
chatrooms = get_chatrooms()
room_list = list(chatrooms.keys()) if chatrooms else ["General"]
selected_room = st.sidebar.selectbox("Choose a room", room_list)

new_room = st.sidebar.text_input("Create New Room")
if st.sidebar.button("Create Room") and new_room:
    rooms_ref.child(new_room).set({"created_at": time.time()})
    st.rerun()

st.subheader(f"📜 Chat History - {selected_room}")
messages = get_messages(selected_room)

# Display Chat Messages
for msg_id, msg_data in messages.items():
    username = msg_data.get("username", "Anonymous")
    text = msg_data.get("text", "")
    img_data = msg_data.get("image", None)

    st.write(f"**{username}**: {text}")
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
        
        if image_file:
            image = Image.open(image_file)
            encoded_img = encode_image(image)
            data["image"] = encoded_img

        db.reference(f"messages/{selected_room}").push(data)
        st.rerun()
