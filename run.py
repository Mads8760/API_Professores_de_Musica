# run.py

# 1. Importamos nosso "Gerente" (app) e "Tradutor" (db) de dentro da pasta "app"
from app import app, db

# 2. Importamos nossos "Moldes"
from app.models import Professor, Aula

# 3. O "Interruptor de Energia"
if __name__ == "__main__":
    # Esta linha mágica garante que o app sabe onde está
    with app.app_context():
        # Esta linha verifica se as tabelas já existem, e se não, as cria.
        # É o nosso antigo comando do "flask shell" de forma automática!
        db.create_all()

    # Liga o servidor
    app.run(debug=True)