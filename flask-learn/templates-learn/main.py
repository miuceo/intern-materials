from app import app
import views, auth


if __name__ == "__main__":
    app.secret_key="0892b3408b078234b&9801345&&)(*!^@#%*())"
    app.register_blueprint(views.bp)
    app.register_blueprint(auth.bp)
    app.run(debug=True)