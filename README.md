# ✨ VIT Anonymous Chat Room

A real-time, anonymous chat application built using **Streamlit** and **Firebase**. Users can chat without login, see previous messages, and share images.

## ✨ Features
- ✅ **Anonymous Chat** - No login required.
- ✅ **Custom Username** - Users can set their own unique names.
- ✅ **Chat History** - Messages load before joining.
- ✅ **Image Sharing** - Users can send images.
- ✅ **Base64 Image Storage** - Images are stored in Firebase.
- ✅ **Auto Refresh** - Chat updates automatically.
- ✅ **Multiple Chat Rooms (Upcoming)** - Users can join different chat rooms.

---

## 🛠 Tech Stack
- **Frontend**: Streamlit
- **Backend**: Firebase Realtime Database
- **Storage**: Firebase Storage
- **Authentication**: Anonymous (Custom Username)

---

## 🛠 Setup & Installation

### 1. Clone the Repository
```bash
git clone https://github.com/deepak-158/Vit-ChitChat.git
cd vit-anonymous-chat
```

### 2. Install Dependencies
```bash
pip install streamlit firebase-admin pillow
```

### 3. Firebase Setup
- **Create a Firebase Project** at [Firebase Console](https://console.firebase.google.com/)
- Enable **Realtime Database** and set rules to public or authenticated users.
- Enable **Firebase Storage** and allow public read/write (or secure access).
- Download **service account JSON file** from Firebase and save as `firebase_credentials.json`.

### 4. Run the Application
```bash
streamlit run app.py
```

---

## 🌟 How It Works
1. **Opens a chat room** where users can send text and images.
2. **Messages are stored** in Firebase in real-time.
3. **Images are converted to Base64** before being stored in Firebase.
4. **Auto-refreshes the chat** when a new message is sent.
5. **Supports custom usernames** without login.

---

## 🔧 Roadmap / Future Improvements
- 🔄 **Real-time Firebase Listeners** (Auto-refresh without reloading page)
- 📞 **Multiple Chat Rooms** (Users can join different chatrooms)
- 🌟 **Enhanced UI** (Add custom themes and chat bubbles)

---

## 👤 Contribution
Pull requests are welcome! Feel free to open an issue or submit a feature request.

---

## 👌 License
This project is open-source under the **MIT License**.

---

Made with ❤️ by Deepak

