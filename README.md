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

### 1. Clone o repositório
```bash
git clone [https://github.com/SEU_USUARIO_AQUI/Api_professores_musica.git](https://github.com/SEU_USUARIO_AQUI/Api_professores_musica.git)
cd Api_professores_musica
