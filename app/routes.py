# app/routes.py

# 1. O "Mapa" e "Ferramentas"
from . import app, db
from .models import Professor, Aula
from flask import request
from werkzeug.security import generate_password_hash, check_password_hash 
from flask_jwt_extended import create_access_token, jwt_required, get_jwt_identity
# ===================================================================
# 4. Rotas
# ===================================================================

# ROTA - Listar todos os professores (Método GET) - VERSÃO BANCO DE DADOS
# app/routes.py
# ...

# ROTA 1: Listar todos os professores (Método GET) - VERSÃO COM FILTROS!
# app/routes.py
# ...

# ROTA 1: Listar todos os professores (Método GET) - VERSÃO COM FILTROS!
@app.route("/professores")
def get_professores():
    # 1. Começamos com uma consulta "base" que seleciona TUDO.
    #    Ainda não estamos executando, só "montando o plano" da consulta.
    query = db.select(Professor)
    
    # 2. Pegamos os filtros que o cliente *pode* ter enviado na URL.
    #    Usamos .get() para não dar erro se o filtro não existir.
    instrumento_filtro = request.args.get('instrumento')
    cidade_filtro = request.args.get('cidade')
    
    # 3. Construímos a consulta "em camadas" (como pedais de efeito!)
    
    # Se o cliente mandou o filtro 'instrumento'...?
    if instrumento_filtro:
        # ...adicionamos uma camada .where() à nossa consulta.
        # A linha nova, que "contém"
     query = query.where(Professor.instrumento.ilike(f"%{instrumento_filtro}%"))
    
    # Se o cliente *também* mandou o filtro 'cidade'...?
    if cidade_filtro:
        # ...adicionamos MAIS UMA camada .where() à consulta.
        query = query.where(Professor.cidade == cidade_filtro)

    # 4. Agora sim, executamos a consulta final que foi construída.
    professores_objetos = db.session.execute(query).scalars().all()
    
    # 5. Convertemos e retornamos o resultado (filtrado ou não).
    professores_dicionarios = [prof.to_dict() for prof in professores_objetos]

    return professores_dicionarios
# ===================================================================
# ROTA Buscar um professor por ID (Método GET) - VERSÃO BANCO DE DADOS

@app.route("/professores/<int:prof_id>")
def get_professor_por_id(prof_id):
    # 1. O Tradutor (SQLAlchemy) tem um atalho para buscar pela chave primária: .get()
    # É super eficiente! Ele vai direto na ficha certa.
    professor = db.session.get(Professor, prof_id)

    # 2. Se o .get() não encontrar nada com aquele ID, ele retorna 'None'.
    if professor:
        # Se encontrou, usamos nosso conversor e retornamos o dicionário.
        return professor.to_dict()
    
    # 3. Se o professor for 'None', avisamos o cliente.
    return {"erro": "Professor não encontrado"}, 404

# ===================================================================

# ROTA Cadastrar um novo professor (Método POST) - VERSÃO BANCO DE DADOS
# app/routes.py

# ROTA 3: Cadastrar um novo professor (COM SEGURANÇA)
@app.route("/professores", methods=["POST"])
def criar_professor():
    dados = request.json
    
    # 1. VALIDAÇÃO ATUALIZADA
    # Precisamos garantir que 'nome', 'email' e 'senha' foram enviados
    if 'nome' not in dados or not dados.get('nome'):
        return {"erro": "Nome é obrigatório"}, 400
    
    if 'email' not in dados or not dados.get('email'):
        return {"erro": "E-mail é obrigatório"}, 400
        
    if 'senha' not in dados or not dados.get('senha'):
        return {"erro": "Senha é obrigatória"}, 400

    # 2. VERIFICAÇÃO DE E-MAIL DUPLICADO
    # Antes de cadastrar, perguntamos ao banco: "Já existe alguém com esse e-mail?"
    # Usamos .filter_by(email=...) para buscar.
    professor_existente = db.session.execute(db.select(Professor).filter_by(email=dados.get('email'))).scalar()
    
    if professor_existente:
        return {"erro": "E-mail já cadastrado no sistema."}, 400

    # 3. O PROCESSO DE HASH (A SEGURANÇA)
    senha_pura = dados.get('senha')
    senha_triturada = generate_password_hash(senha_pura) 
    # O resultado será algo como: "scrypt:32768:8:1$lK..."

    # 4. CRIAÇÃO DO OBJETO
    novo_professor = Professor(
        nome=dados.get('nome'),
        email=dados.get('email'),
        senha_hash=senha_triturada, # <-- SALVAMOS O HASH, NÃO A SENHA PURA!
        instrumento=dados.get('instrumento'),
        cidade=dados.get('cidade'),
        descricao=dados.get('descricao')
    )
    
    db.session.add(novo_professor)
    db.session.commit()
    
    return novo_professor.to_dict(), 201
# ===================================================================

# ROTA Atualizar o perfil de um professor (Método PUT) - VERSÃO BANCO DE DADOS
# app/routes.py

# ROTA 4: Atualizar o perfil de um professor (Método PUT) - COM VALIDAÇÃO!
@app.route("/professores/<int:prof_id>", methods=["PUT"])
def atualizar_professor(prof_id):
    professor = db.session.get(Professor, prof_id)

    if not professor:
        return {"erro": "Professor não encontrado"}, 404

    dados = request.json

    # ===================================================================
    # NOVA VALIDAÇÃO PARA A "REFORMA"
    # ===================================================================
    # A lógica é: SE a chave 'nome' foi enviada no pedido (in dados),
    # ENTÃO verificamos se ela está vazia (not dados['nome']).
    if 'nome' in dados and not dados.get('nome'):
        return {"erro": "O campo 'nome' não pode ser vazio na atualização."}, 400
        
    if 'instrumento' in dados and not dados.get('instrumento'):
        return {"erro": "O campo 'instrumento' não pode ser vazio na atualização."}, 400
    # ===================================================================

    # Se passou na validação, atualizamos normalmente
    professor.nome = dados.get('nome', professor.nome)
    professor.instrumento = dados.get('instrumento', professor.instrumento)
    professor.cidade = dados.get('cidade', professor.cidade)
    professor.descricao = dados.get('descricao', professor.descricao)
    
    db.session.commit()

    return professor.to_dict()

# ===================================================================

# ROTA Apagar o perfil de um professor (Método DELETE) - VERSÃO BANCO DE DADOS
@app.route("/professores/<int:prof_id>", methods=["DELETE"])
def apagar_professor(prof_id):
    """
    Esta função encontra um professor pelo 'id' no banco de dados
    e o remove permanentemente.
    """
    # 1. Encontra o professor no banco de dados que queremos apagar.
    professor = db.session.get(Professor, prof_id)

    # 2. Se não encontrar, retorna o erro 404.
    if not professor:
        return {"erro": "Professor não encontrado"}, 404

    # 3. Damos a ordem para o Tradutor: "Marque este objeto para exclusão".
    #    Isso o coloca na "bandeja de saída".
    db.session.delete(professor)
    
    # 4. A ordem final e irrevogável: "Pode executar as exclusões pendentes!".
    db.session.commit()

    # 5. Retornamos uma mensagem de sucesso.
    return {"mensagem": f"Professor com ID {prof_id} apagado com sucesso!"}

# ===================================================================
# 5. ROTAS PARA AS AULAS (O "REPERTÓRIO")
# ===================================================================

# Metodo POST

@app.route('/professores/<int:prof_id>/aulas', methods = ["POST"] )

def criar_aulas_para_professor(prof_id):
    professor =db.session.get(Professor, prof_id)
    if not professor:
        return{'ERRO: Professor não encontrado'}, 404
    dados = request.json
# ===================================================================
#  NOSSA NOVA VALIDAÇÃO (O "Recepcionista Atento" da Aula)
# ===================================================================
# O "molde" da Aula diz que 'titulo' é obrigatório. Vamos checar.
    
    if 'titulo' not in dados or not dados.get('titulo'):
        # Se faltar, devolvemos um erro 400 (Bad Request)
        return {"erro": "O campo 'titulo' é obrigatório e não pode estar vazio."}, 400
# ===================================================================

    nova_aula = Aula (
        titulo = dados.get('titulo'),
        descricao = dados.get('descricao')
)
    nova_aula.professor = professor
    db.session.add(nova_aula)
    db.session.commit()


    return nova_aula.to_dict(), 201

# app/routes.py
# ... (depois do fim da ROTA 6: criar_aula_para_professor) ...

# ROTA 7: Listar todas as aulas DE UM PROFESSOR (Método GET)
@app.route("/professores/<int:prof_id>/aulas")
def get_aulas_do_professor(prof_id):
    """
    Lista todo o "repertório" (aulas) de um professor específico.
    """
    # 1. Encontramos o professor "dono" das aulas.
    professor = db.session.get(Professor, prof_id)

    # 2. Se o professor não existir, não há aulas para mostrar.
    if not professor:
        return {"erro": "Professor não encontrado"}, 404

    # ===================================================================
    # 3. A MÁGICA DO db.relationship!
    # ===================================================================
    #    Lembra de todo o trabalho com 'back_populates' e 'aulas'? É para isto.
    #    Ao acessar o atributo .aulas do objeto professor, o SQLAlchemy
    #    vai ao banco e busca TODAS as aulas que têm o 'professor_id' deste professor.
    aulas_do_professor = professor.aulas 

    # 4. Convertemos a lista de objetos <Aula> em uma lista de dicionários.
    aulas_dict = [aula.to_dict() for aula in aulas_do_professor]
    
    # 5. Retornamos a lista.
    return aulas_dict

# ===================================================================
# 4. Atualizando aulas
# ===================================================================

# app/routes.py

# ROTA 8: Atualizar uma aula específica (Método PUT) - COM VALIDAÇÃO!
@app.route("/aulas/<int:aula_id>", methods=["PUT"])
def atualizar_aula(aula_id):
    aula = db.session.get(Aula, aula_id)

    if not aula:
        return {"erro": "Aula não encontrada"}, 404
    
    dados = request.json
    
    # ===================================================================
    # VALIDAÇÃO DA AULA
    # ===================================================================
    if 'titulo' in dados and not dados.get('titulo'):
        return {"erro": "O campo 'titulo' não pode ser vazio na atualização."}, 400
    # ===================================================================

    # Atualiza os dados
    aula.titulo = dados.get('titulo', aula.titulo)
    aula.descricao = dados.get('descricao', aula.descricao)

    db.session.commit()
    
    return aula.to_dict()
# app/routes.py
# ... (Lembre-se de verificar se check_password_hash já está importado lá no topo!)

# app/routes.py

# ROTA 9: Apagar uma aula específica (Método DELETE) - AGORA PROTEGIDA!
# app/routes.py

# ROTA 9: Apagar uma aula específica (Método DELETE) - COM VERIFICAÇÃO DE DONO!
@app.route("/aulas/<int:aula_id>", methods=["DELETE"])
@jwt_required()
def apagar_aula(aula_id):
    
    # 1. Descobrimos QUEM está tentando apagar (lemos a pulseira)
    usuario_atual_id = get_jwt_identity() 
    # Nota: O ID vem como texto (string) da pulseira, vamos precisar converter para número.

    # 2. Encontramos a aula no banco
    aula = db.session.get(Aula, aula_id)
    
    if not aula:
        return {"erro": "Aula não encontrada"}, 404

    # ===================================================================
    # 3. A VERIFICAÇÃO DE PROPRIEDADE (O GUARDIÃO)
    # ===================================================================
    # Comparamos o ID do dono da aula com o ID de quem está logado.
    # Usamos int() para garantir que estamos comparando número com número.
    if aula.professor_id != int(usuario_atual_id):
        # Se forem diferentes, barramos com erro 403 (Forbidden/Proibido)
        return {"erro": "Você não tem permissão para apagar esta aula. Ela não é sua!"}, 403
    # ===================================================================

    # 4. Se passou pelo guarda, pode apagar.
    db.session.delete(aula)
    db.session.commit()
    
    return {"mensagem": "Aula apagada com sucesso!"}
@app.route("/login", methods=["POST"])
def login():
    dados = request.json
    email = dados.get('email')
    senha = dados.get('senha')

    professor = db.session.execute(db.select(Professor).filter_by(email=email)).scalar()

    if not professor or not check_password_hash(professor.senha_hash, senha):
        return {"erro": "Email ou senha incorretos"}, 401

    # ===================================================================
    # AQUI ACONTECE A MÁGICA DA PULSEIRA
    # ===================================================================
    # Criamos o token e "escondemos" o ID do professor dentro dele (identity).
    # Assim, quando ele mostrar a pulseira, saberemos quem ele é (ID 1, 2, etc).
    access_token = create_access_token(identity=str(professor.id))

    # Retornamos o token para o cliente guardar
    return {
        "mensagem": "Login realizado com sucesso!",
        "access_token": access_token,
        "usuario": professor.to_dict()
    }