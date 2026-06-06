from authlib.integrations.flask_client import OAuth
from flask import Flask, url_for, session
from flask import redirect

import os

from dotenv import load_dotenv

load_dotenv()

app = Flask(__name__)
app.secret_key = "czFiDcWbqA"  # Some random string
# First, create your project https://console.cloud.google.com/projectcreate
# Then, create OAuth Client ID https://console.cloud.google.com/apis/credentials
# Copy and paste Client ID/Secret
app.config["GOOGLE_CLIENT_ID"]=os.getenv("GOOGLE_CLIENT_ID")
app.config["GOOGLE_CLIENT_SECRET"]=os.getenv("GOOGLE_CLIENT_SECRET")

CONF_URL = "https://accounts.google.com/.well-known/openid-configuration"
oauth = OAuth(app)
oauth.register(
    name="google",
    server_metadata_url=CONF_URL,
    client_kwargs={
        "scope": "openid email profile"
    }
)


@app.route("/")
def homepage():
    username = session.get("username")
    if username:
        return f"""<pre>Hello, { username }!</pre><a href="/logout">logout</a>"""

    return """<a href="/login">login</a>"""


@app.route("/login")
def login():
    redirect_uri = url_for("auth", _external=True)
    return oauth.google.authorize_redirect(redirect_uri)


@app.route("/auth")
def auth():
    token = oauth.google.authorize_access_token()
    session["username"] = token["userinfo"]["name"]
    return redirect("/")


@app.route("/logout")
def logout():
    session.pop("username", None)
    return redirect("/")


if __name__ == "__main__":
    app.run(debug=True)

