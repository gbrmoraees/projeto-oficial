from app import create_app, db
from sqlalchemy import text

app = create_app()

with app.app_context():
    try:
        db.session.execute(text('SELECT 1'))
        print("Conexão com o banco bem-sucedida!")
    except Exception as e:
        print(f"Erro ao conectar ao banco: {e}")