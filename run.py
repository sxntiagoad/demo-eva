from app import create_app
from app.routes.auth import bp
app = create_app()

app.register_blueprint(bp)


if __name__ == "__main__":
    app.run()
