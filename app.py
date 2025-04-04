import os
import requests
from flask import Flask, redirect, request, session, url_for, render_template
from dotenv import load_dotenv

# Load environment variables from the .env file
load_dotenv()

app = Flask(__name__)
app.secret_key = os.urandom(24)  # Secret key for Flask sessions

# Hardcoded the redirect URI for live testing
REDIRECT_URI = "https://rydewitheli.com/tiktok/callback"  # Use the live redirect URI here

# These should be pulled from your .env file, but for now we'll hardcode for simplicity
TIKTOK_CLIENT_KEY = "your_tiktok_client_key_here"  # Replace with your actual TikTok Client Key
TIKTOK_CLIENT_SECRET = "your_tiktok_client_secret_here"  # Replace with your actual TikTok Client Secret

# Home route to display user data or login link
@app.route("/")
def home():
    user = session.get("user")
    if user:
        return render_template("home.html", user=user)
    else:
        return render_template("home.html", user=None)

# Login route to redirect to TikTok's login page
@app.route("/login")
def login():
    print("Login route hit!")  # Debugging log to check if the route is working
    return redirect(
        f"https://www.tiktok.com/v2/auth/authorize/?"
        f"client_key={TIKTOK_CLIENT_KEY}"
        f"&response_type=code"
        f"&scope=user.info.basic"
        f"&redirect_uri={REDIRECT_URI}"
        f"&state=randomstate"
    )

# Callback route for TikTok to send users back after authentication
@app.route("/tiktok/callback")
def tiktok_callback():
    code = request.args.get("code")
    if not code:
        return "Authorization failed. No code received."

    token_url = "https://open.tiktokapis.com/v2/oauth/token"
    data = {
        "client_key": TIKTOK_CLIENT_KEY,
        "client_secret": TIKTOK_CLIENT_SECRET,
        "code": code,
        "grant_type": "authorization_code",
        "redirect_uri": REDIRECT_URI,
    }

    res = requests.post(token_url, data=data).json()
    access_token = res.get("access_token")

    if not access_token:
        return "Token error. Unable to get access token."

    # Fetch user information using the access token
    user_info = requests.get(
        "https://open.tiktokapis.com/v2/user/info/",
        headers={"Authorization": f"Bearer {access_token}"}
    ).json()

    session["user"] = user_info.get("data", {}).get("user")
    return redirect(url_for("home"))

# Logout route to clear user session
@app.route("/logout")
def logout():
    session.pop("user", None)  # Clear the user session
    return redirect(url_for("home"))

# Run the app on a specified port
if __name__ == "__main__":
    port = int(os.environ.get("PORT", 10000))  # Default port to 10000, or from environment
    app.run(debug=True, host="0.0.0.0", port=port)
