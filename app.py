import os
import requests
from flask import Flask, redirect, request, session, url_for, render_template
from dotenv import load_dotenv

# Load .env variables
load_dotenv()

app = Flask(__name__)
app.secret_key = os.urandom(24)

# Read from environment
TIKTOK_CLIENT_KEY = os.getenv("TIKTOK_CLIENT_KEY")
TIKTOK_CLIENT_SECRET = os.getenv("TIKTOK_CLIENT_SECRET")
REDIRECT_URI = os.getenv("REDIRECT_URI")

@app.route("/")
def home():
    user = session.get("user")
    return render_template("home.html", user=user)

@app.route("/login")
def login():
    return redirect(
        f"https://www.tiktok.com/v2/auth/authorize/"
        f"?client_key={TIKTOK_CLIENT_KEY}"
        f"&response_type=code"
        f"&scope=user.info.basic"
        f"&redirect_uri={REDIRECT_URI}"
        f"&state=randomstate"
    )

@app.route("/tiktok/callback")
def tiktok_callback():
    code = request.args.get("code")
    if not code:
        return "Authorization failed."

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
        return "Token error"

    user_info = requests.get(
        "https://open.tiktokapis.com/v2/user/info/",
        headers={"Authorization": f"Bearer {access_token}"}
    ).json()

    session["user"] = user_info.get("data", {}).get("user")
    return redirect(url_for("home"))

@app.route("/logout")
def logout():
    session.pop("user", None)
    return redirect(url_for("home"))

if __name__ == "__main__":
    port = int(os.environ.get("PORT", 10000))  
    app.run(debug=True, host="0.0.0.0", port=port)
