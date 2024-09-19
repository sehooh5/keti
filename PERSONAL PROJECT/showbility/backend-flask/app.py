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
def home():
    return 'Flask Home'

@app_flask.route(app_flask.config['MEDIA_URL'] + '<path:filename>')
def media_files(filename):
    return send_from_directory(app_flask.config['MEDIA_ROOT'], filename)

# Blueprint 등록
app_flask.register_blueprint(user_bp, url_prefix='/users')
app_flask.register_blueprint(content_bp, url_prefix='/contents')
app_flask.register_blueprint(group_bp, url_prefix='/groups')


# FastAPI 애플리케이션 생성
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

# DispatcherMiddleware를 사용하여 Flask와 FastAPI 통합
app = DispatcherMiddleware(app_flask, {
    "/api": WSGIMiddleware(app_fastapi),
    "/media": WSGIMiddleware(app_flask)
})


if __name__ == "__main__":
    # DispatcherMiddleware가 포함된 앱을 실행
    run_simple('0.0.0.0', 5000, app)
