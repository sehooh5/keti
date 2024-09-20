from flask import Flask
from fastapi import FastAPI
from flask_mail import Mail
from routes import user_bp, content_bp, group_bp
from werkzeug.middleware.dispatcher import DispatcherMiddleware
from fastapi.middleware.wsgi import WSGIMiddleware
from werkzeug.serving import run_simple

app_flask = Flask(__name__)
app_fastapi = FastAPI()

app_flask.config.from_object('config.Config')
app_flask.register_error_handler(Exception, custom_exception_handler)

mail = Mail(app_flask)

@app_flask.route('/')
def index():
    return 'index'

@app_flask.route(app_flask.config['MEDIA_URL'] + '<path:filename>')
def media_files(filename):
    return send_from_directory(app_flask.config['MEDIA_ROOT'], filename)

app_flask.register_blueprint(user_bp, url_prefix='/users')
app_flask.register_blueprint(content_bp, url_prefix='/contents')
app_flask.register_blueprint(group_bp, url_prefix='/groups')


# FastAPI
app_fastapi = FastAPI()

@app_fastapi.post("/getToken/")
async def get_token():
    return {"message": "Token generated"}

@app_fastapi.post("/verify-token/")
async def verify_token():
    return {"message": "Token verified"}

@app_fastapi.post("/refresh-token/")
async def refresh_token():
    return {"message": "Token refreshed"}

app = DispatcherMiddleware(app_flask, {
    "/api": WSGIMiddleware(app_fastapi),
    "/media": WSGIMiddleware(app_flask)
})


if __name__ == "__main__":
    run_simple('0.0.0.0', 5000, app)
