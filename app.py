import os
from flask import Flask, redirect, request, session, url_for, render_template
from dotenv import load_dotenv

# Load environment variables from .env
load_dotenv()

app = Flask(__name__)
app.secret_key = os.urandom(24)  # Secret key for Flask sessions

# Hardcoded values for the redirect URI and TikTok API credentials
REDIRECT_URI = "https://rydewitheli.com/tiktok/callback"  # Adjust as necessary

TIKTOK_CLIENT_KEY = "your_tiktok_client_key_here"  # Replace with your actual TikTok Client Key
TIKTOK_CLIENT_SECRET = "your_tiktok_client_secret_here"  # Replace with your actual TikTok Client Secret

# Home route to display user data or login link
@app.route("/")
def home():
    user = session.get("user")
    return render_template("home.html", user=user)

# Login route to simulate successful login
@app.route("/login")
def login():
    # Simulate a successful login by creating mock user data
    mock_user_data = {
        "id": "123456",
        "name": "Test User",
        "username": "testuser",
        "avatar": "https://via.placeholder.com/150"  # Placeholder avatar
    }
    session["user"] = mock_user_data  # Store mock user in the session
    return redirect(url_for("home"))  # Redirect to home page after login

# Callback route for TikTok to send users back after authentication
@app.route("/tiktok/callback")
def tiktok_callback():
    # Simulate the user info after successful login
    mock_user_data = {
        "id": "123456",
        "name": "Test User",
        "username": "testuser",
        "avatar": "https://via.placeholder.com/150"  # Placeholder avatar
    }
    session["user"] = mock_user_data  # Store mock user in the session
    return redirect(url_for("home"))  # Redirect to home page after callback

# Logout route to clear user session
@app.route("/logout")
def logout():
    session.pop("user", None)  # Clear the user session
    return redirect(url_for("home"))

# Run the app on a specified port
if __name__ == "__main__":
    port = int(os.environ.get("PORT", 10000))  # Default port to 10000, or from environment
    app.run(debug=True, host="0.0.0.0", port=port)
