# 🎵 API de Professores de Música

Bem-vindo ao repositório da **API de Professores de Música**. Este projeto foi desenvolvido como parte da minha jornada de transição de carreira da Música para o Desenvolvimento Back-end.

O objetivo é criar uma plataforma centralizada onde professores de música possam se cadastrar e divulgar suas aulas, e alunos possam encontrar serviços específicos (como "Aulas de Violão" ou "Teoria Musical").

## 🚀 Funcionalidades

O sistema conta com uma arquitetura RESTful completa, incluindo:

- **CRUD de Professores:** Cadastro, Listagem (com filtros), Atualização e Remoção.
- **CRUD Relacional de Aulas:** Criação de aulas vinculadas a um professor específico.
- **Autenticação e Segurança:**
  - Login com e-mail e senha.
  - Criptografia de senhas (Hash).
  - Proteção de rotas com **Token JWT** (JSON Web Token).
- **Filtros Inteligentes:** Busca de professores por instrumento ou cidade.
- **Autorização:** Regras de negócio que impedem um professor de apagar a aula de outro.

## 🛠️ Tecnologias Utilizadas

- **Linguagem:** [Python](https://www.python.org/)
- **Framework:** [Flask](https://flask.palletsprojects.com/)
- **Banco de Dados:** SQLite
- **ORM:** SQLAlchemy (Flask-SQLAlchemy)
- **Autenticação:** Flask-JWT-Extended
- **Segurança:** Werkzeug Security
- **CORS:** Flask-CORS

## ⚙️ Como Rodar o Projeto

Se você quiser rodar esta API no seu computador, siga os passos abaixo:

## 1. Clone o repositório

git clone [https://github.com/SEU_USUARIO_AQUI/Api_professores_musica.git](https://github.com/SEU_USUARIO_AQUI/Api_professores_musica.git)
cd Api_professores_musica.

## 2. Crie e ative o ambiente virtual
### No Windows
python -m venv venv
venv\Scripts\activate

### No Linux/Mac
python3 -m venv venv
source venv/bin/activate

## 3. Instale as dependências
pip install -r requirements.txt

## 4. Rode o servidor
python run.py <br>
O servidor iniciará em http://127.0.0.1:5000.

## 📡 Endpoints Principais (Rotas)

| Método | Rota | Descrição | Autenticação? |
| :--- | :--- | :--- | :--- |
| `POST` | `/professores` | Cadastra novo professor | Não |
| `GET` | `/professores` | Lista professores (filtros: `?instrumento=` e `?cidade=`) | Não |
| `POST` | `/login` | Realiza login e recebe Token JWT | Não |
| `POST` | `/professores/{id}/aulas` | Cadastra aula para um professor | Não (Simulado) |
| `GET` | `/professores/{id}/aulas` | Lista aulas de um professor | Não |
| `DELETE`| `/aulas/{id}` | Remove uma aula | **Sim (Token)** |

## Autora
Madelu Lopes Estudante de Análise e Desenvolvimento de Sistemas | Professora de Música | Desenvolvedora Back-end em formação. <br>

Projeto desenvolvido com fins educacionais.

## Passo 2: Atualizando o GitHub (Salvando as Novidades)

Você criou dois arquivos novos (`requirements.txt` e `README.md`). Precisamos enviar essas mudanças para a nuvem.

Você já sabe a coreografia:

1.  **Palco:** Coloque os arquivos novos no palco.
    ```bash
    git add .
    ```
2.  **Foto:** Tire a foto (Commit).
    ```bash
    git commit -m "Adiciona documentação (README) e lista de dependências"
    ```
3.  **Upload:** Envie para o GitHub.
    ```bash
    git push
    ```

### O Grand Finale

Agora, vá até a página do seu repositório no GitHub e atualize a página (F5).

Você verá que, abaixo da lista de arquivos, apareceu o seu texto formatado, bonito, com título grande e tabelas. Isso dá uma cara extremamente profissional ao seu trabalho.

Isso é o que recrutadores e outros desenvolvedores veem. Você não tem apenas "código", você tem um "produto documentado".

Me diga como ficou a "capa do seu álbum"! E com isso, encerramos oficialmente todos os preparativos locais. Estamos prontos para o **Deploy** (colocar o site no ar de verdade) na próxima etapa, se você quiser!


