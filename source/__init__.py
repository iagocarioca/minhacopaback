from flask import Flask
from flask_cors import CORS
from config import Config
from source.extensions.extensios import db, migrate, jwt

def create_app(config_class=Config):
    app = Flask(__name__)
    app.config.from_object(config_class)

    # Configurar CORS
    # Em desenvolvimento: aceita todas as origens (inclui rede local)
    # Em produção, ajuste para aceitar apenas domínios específicos
    import os
    is_development = os.environ.get('FLASK_ENV') != 'production'
    
    if is_development:
        # Desenvolvimento: aceita qualquer origem (inclui IPs da rede local)
        CORS(app, resources={
            r"/api/*": {
                "origins": "*",  # Aceita qualquer origem em desenvolvimento
                "methods": ["GET", "POST", "PUT", "DELETE", "OPTIONS"],
                "allow_headers": ["Content-Type", "Authorization"],
                "expose_headers": ["Content-Type", "Authorization"],
                "supports_credentials": True,
                "max_age": 3600
            }
        })
    else:
        # Produção: apenas origens específicas
        CORS(app, resources={
            r"/api/*": {
                "origins": ["http://localhost:3000", "http://localhost:3001"],
                "methods": ["GET", "POST", "PUT", "DELETE", "OPTIONS"],
                "allow_headers": ["Content-Type", "Authorization"],
                "expose_headers": ["Content-Type", "Authorization"],
                "supports_credentials": True,
                "max_age": 3600
            }
        }) 

    # Inicialização das extensões
    db.init_app(app)
    migrate.init_app(app, db)
    jwt.init_app(app)

    # Importação dos modelos
    with app.app_context():
        from source.domain.users.models import User
        from source.domain.peladas.models import (
            Pelada, Jogador, Temporada, Rodada, Time, TimeJogador,
            Partida, Gol, Votacao, Voto
        )
        
    # Registrar blueprints
    from source.api.user import user_bp
    from source.api.pelada import pelada_bp

    app.register_blueprint(user_bp, url_prefix='/api/usuarios')
    app.register_blueprint(pelada_bp, url_prefix='/api/peladas')

    # Servir arquivos estáticos de uploads
    import os
    from flask import send_from_directory
    
    @app.route('/static/uploads/<path:filename>')
    def uploaded_file(filename):
        upload_dir = os.path.join(app.root_path, '..', 'static', 'uploads')
        return send_from_directory(upload_dir, filename)

    @app.route('/')
    def index():
        return {'message': 'XClickPayEx API'}, 200

    return app
