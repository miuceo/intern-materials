from app import app
import views


if __name__ == "__main__":
    app.register_blueprint(views.bp)
    app.run(debug=True)