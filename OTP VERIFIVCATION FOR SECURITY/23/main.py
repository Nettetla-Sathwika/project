import streamlit as st
import sqlite3
import os
import smtplib
import random
import string
from email.mime.text import MIMEText
from email.mime.multipart import MIMEMultipart
from cryptography.fernet import Fernet
from io import BytesIO

def load_or_create_key():
    key_path = "secret.key"
    if os.path.exists(key_path):
        with open(key_path, "rb") as f:
            return f.read()
    else:
        key = Fernet.generate_key()
        with open(key_path, "wb") as f:
            f.write(key)
        return key

key = load_or_create_key()
cipher = Fernet(key)

conn = sqlite3.connect("users.db", check_same_thread=False)
cursor = conn.cursor()
cursor.execute('''CREATE TABLE IF NOT EXISTS users (
    username TEXT, password TEXT, email TEXT, phone TEXT,
    gender TEXT, address TEXT)''')

cursor.execute('''CREATE TABLE IF NOT EXISTS files (
    username TEXT, filename TEXT, encrypted_data BLOB)''')
conn.commit()
session_otp = {}
def send_otp(email,otp):
    # otp = ''.join(random.choices(string.digits, k=6))
    session_otp[email] = otp

  

    sender_email = "sudhatestmail@gmail.com"
    sender_password = "nhbjssyxvxbendzz"
    msg = MIMEMultipart()
    msg['From'] = sender_email
    msg['To'] = email
    msg['Subject'] = "Your OTP Code"

    msg.attach(MIMEText(f"Your OTP is: {otp}", 'plain'))

    try:
        server = smtplib.SMTP('smtp.gmail.com', 587)
        server.starttls()
        server.login(sender_email, sender_password)
        server.send_message(msg)
        server.quit()
        return True
    except Exception as e:
        st.error(f"Email sending failed: {e}")
        return False

# --- Register User ---
def register_user(username, password, email, phone, gender, address):
    cursor.execute("INSERT INTO users VALUES (?, ?, ?, ?, ?, ?)",
                   (username, password, email, phone, gender, address))
    conn.commit()

# --- Verify Login Credentials ---
def verify_login(username, password):
    cursor.execute("SELECT * FROM users WHERE username=? AND password=?", (username, password))
    return cursor.fetchone()

# --- Encrypt and Store File ---
def encrypt_and_store_file(username, file):
    encrypted_data = cipher.encrypt(file.read())
    cursor.execute("INSERT INTO files VALUES (?, ?, ?)", (username, file.name, encrypted_data))
    conn.commit()

# --- Retrieve Files ---
def get_files(username):
    cursor.execute("SELECT filename, encrypted_data FROM files WHERE username=?", (username,))
    return cursor.fetchall()

# --- Streamlit UI ---
st.title("🔐 Secure OTP File Encryption System")

menu = st.sidebar.selectbox("Menu", ["Register", "Login", "Upload & Download"])

# --- Register ---
if menu == "Register":
    st.subheader("📝 User Registration")
    with st.form("register_form"):
        username = st.text_input("Username")
        password = st.text_input("Password", type="password")
        email = st.text_input("Email")
        phone = st.text_input("Phone")
        gender = st.selectbox("Gender", ["Male", "Female", "Other"])
        address = st.text_area("Address")
        submit = st.form_submit_button("Register")
        if submit:
            register_user(username, password, email, phone, gender, address)
            st.success("✅ Registration successful!")

elif menu == "Login":
    st.subheader("User Login with OTP Verification")

    if "otp_sent" not in st.session_state:
        with st.form("login_form"):
            username = st.text_input("Username")
            password = st.text_input("Password", type="password")
            login_btn = st.form_submit_button("Send OTP")

        if login_btn:
            user = verify_login(username, password)
            if user:
                email = user[2]
                otp = ''.join(random.choices(string.digits, k=6))
                if send_otp(email,otp):
                    st.success(f"📩 OTP sent to {email}")
                    st.session_state["otp_sent"] = True
                    st.session_state["login_user"] = username
                    st.session_state["otp_email"] = email
                    st.session_state["otp_code"] = session_otp[email]
            else:
                st.error("❌ Invalid credentials")

    elif st.session_state.get("otp_sent"):
        with st.form("otp_verify_form"):
            otp_input = st.text_input("Enter OTP")
            verify_btn = st.form_submit_button("Verify OTP")

        if verify_btn:
            if otp_input == st.session_state.get("otp_code", ""):
                st.session_state["logged_in_user"] = st.session_state.get("login_user")
                st.success("✅ OTP Verified! You are now logged in.")
                # Cleanup
                for key in ["otp_sent", "otp_email", "otp_code", "login_user"]:
                    st.session_state.pop(key, None)
            else:
                st.error("❌ Invalid OTP")


# --- Upload & Download ---
elif menu == "Upload & Download":
    if "logged_in_user" not in st.session_state:
        st.warning("⚠️ Please log in first.")
    else:
        st.subheader(f"📁 Welcome, {st.session_state['logged_in_user']}")

        with st.form("upload_form"):
            uploaded_file = st.file_uploader("Upload a file")
            upload_btn = st.form_submit_button("Encrypt and Save")
            if upload_btn and uploaded_file:
                encrypt_and_store_file(st.session_state['logged_in_user'], uploaded_file)
                st.success("✅ File encrypted and saved successfully.")

        st.write("### 📂 Your Files:")
        files = get_files(st.session_state['logged_in_user'])
        for filename, encrypted_data in files:
            try:
                decrypted_data = cipher.decrypt(encrypted_data)
                b64 = BytesIO(decrypted_data)
                st.download_button("Download " + filename, b64, file_name=filename)
            except Exception as e:
                st.error(f"❌ Failed to decrypt {filename}: {e}")
