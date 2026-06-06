from app import app
import views
import auth

if __name__ == "__main__":
    app.secret_key = "Au*h8*as&d56_7-8J"
    app.register_blueprint(views.bp)
    app.register_blueprint(auth.bp)
    app.run(debug=True)