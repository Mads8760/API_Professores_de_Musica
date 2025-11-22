# app/models.py
from . import db  # O "." significa "do pacote atual, importe o db"

# ===================================================================
# 1. CLASSES E OBJETOS
# Aqui configuramos os moldes dos professores e das aulas
# ===================================================================

# ===================================================================
# 1.2 MODELAGEM DA "FICHA DE PROFESSORES"
# ===================================================================
# Criação do banco de dados com colunas e seus valores
# app/models.py
from . import db

class Professor(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    nome = db.Column(db.String(100), nullable=False)
    
    # === NOVOS CAMPOS DE SEGURANÇA ===
    # unique=True garante que o banco não aceite e-mails repetidos
    email = db.Column(db.String(120), unique=True, nullable=False)
    # Note que chamamos de 'senha_hash', não de 'senha', para lembrar que está criptografado
    senha_hash = db.Column(db.String(128), nullable=False)
    # =================================
    
    instrumento = db.Column(db.String(100), nullable=False)
    cidade = db.Column(db.String(50))
    descricao = db.Column(db.Text)

    # Relacionamento
    aulas = db.relationship('Aula', back_populates='professor', cascade='all, delete-orphan')

    def to_dict(self):
        return {
            "id": self.id,
            "nome": self.nome,
            "email": self.email, # Podemos mostrar o e-mail
            # NUNCA retornamos a senha_hash no to_dict! É segredo!
            "instrumento": self.instrumento,
            "cidade": self.cidade,
            "descricao": self.descricao
        }




# ===================================================================
# 1.3 MODELAGEM DA "FICHA DE AULA"
# ===================================================================

class Aula(db.Model):
    id =db.Column(db.Integer, primary_key = True)
    titulo = db.Column(db.String(100), nullable = False)
    descricao = db.Column(db.Text)
    professor_id = db.Column(db.Integer, db.ForeignKey('professor.id'), nullable=False)

    # CORREÇÃO 4: 'back_populates' agora aponta para 'aulas' (minúsculo)
    professor = db.relationship('Professor', back_populates = 'aulas')

    # CORREÇÃO 5: Esta função foi movida para DENTRO da classe Aula
    # (E corrigi o nome de 'to_dic' para 'to_dict' (de dictionary))
    def to_dict(self):
        return{
            "id":self.id,
            "titulo":self.titulo,
            "descricao":self.descricao,
            "professor_id":self.professor_id
        }