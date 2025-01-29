from flask import Flask, request
from flask_cors import CORS

from routes.routes import index_bp

def create_app():
    app = Flask(__name__)
    
    app.secret_key = 'sua_chave_secreta_super_segura'

    app.register_blueprint(index_bp)
    
    CORS(app)
    
    @app.after_request
    def add_hsts_header(resp):
        if request.is_secure:
            resp.headers['Strict-Transport-Security'] = 'max-age31536000; includeSubDomains'
        return resp
    
    @app.route('/health')
    def health():
        return 'OK'
    
    return app

app = create_app()

if  __name__ == '__main__':
    app.run(debug=True)

