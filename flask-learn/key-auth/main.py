from app import app
import views

if __name__ == "__main__":
    app.register_blueprint(views.bp)
    app.run(host="127.0.0.1", port=5000, debug=True)