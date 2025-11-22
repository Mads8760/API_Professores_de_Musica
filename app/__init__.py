# API PARA PROFESSORES DE MÚSICA #

# ===================================================================
# 1. IMPORTAÇÕES
# Aqui importamos as "ferramentas" que vamos usar.
# ===================================================================

from flask import Flask, request
from flask_sqlalchemy import SQLAlchemy
from flask_cors import CORS
from flask_jwt_extended import JWTManager
# ===================================================================
# 2 . TRADUTOR
# # Criamos nosso Tradutor (db) e Gerente (app) aqui, mas sem "ligar" ainda.
# ===================================================================

db = SQLAlchemy()
app = Flask(__name__)

# Configuração do banco de dados (apontando para o "fichário")
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///professores.db'
# ===================================================================
# CONFIGURAÇÃO DO JWT (A MÁQUINA DE PULSEIRAS)
# ===================================================================
# 1. Definimos a "Tinta Secreta" do carimbo. 
# (Na vida real, isso seria uma senha gigante e aleatória escondida)
app.config["JWT_SECRET_KEY"] = "super-secreta-chave-do-festival-musica"

# 2. Ligamos a máquina
jwt = JWTManager(app)

# ===================================================================
# PASSO 2: INICIALIZE O CORS
# Aqui dizemos ao "Segurança" para permitir acesso de "qualquer origem" (*)
# a "todos os nossos recursos" (rotas) (r"/*").
# ===================================================================
CORS(app, resources={r"/*": {"origins": "*"}})


# Apresentamos o Gerente ao Tradutor
db.init_app(app)

# IMPORTANTE: Importamos nossas rotas e modelos DEPOIS de criar o app e o db
# para evitar problemas de "quem veio primeiro?".
from . import routes, models