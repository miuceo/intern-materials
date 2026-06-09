from flask import Flask, session, redirect, url_for, request


app = Flask(__name__)
app.secret_key = "6J=far*v(^gfg_m65"

@app.route("/")
def index():
    if "username" in session:
        return f"Logged in as {session['username']}"
    return "You are not logged in."


@app.route("/login", methods=["POST", "GET"])
def login():
    if request.method == "POST":
        username = request.form["username"]
        session["username"] = username
        return f"Hello, {username}. Click <a href='{url_for('index')}'>here</a>!"
    
    return f"""
            <form method='post'>
                <p><input type="text" name="username">
                <p><input type="submit" name="Login">
            </form>
        """
        
        
@app.route("/logout")
def logout():
    session.pop("username", None)
    return redirect(url_for('index'))


if __name__ == "__main__":
    app.run(debug=True)