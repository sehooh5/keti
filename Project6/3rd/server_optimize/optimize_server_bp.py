from flask import Flask
from flask_cors import CORS
from routes.weather import weather_bp
from routes.edge import edge_bp
from routes.usage import usage_bp

app = Flask(__name__)
CORS(app)

# Blueprint 등록
app.register_blueprint(weather_bp, url_prefix='/weather')
app.register_blueprint(edge_bp, url_prefix='/edge')
app.register_blueprint(usage_bp, url_prefix='/usage')

if __name__ == '__main__':
    app.run(host='0.0.0.0', threaded=True, port=6432)
