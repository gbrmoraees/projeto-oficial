from app import create_app

# Inicializa a aplicação Flask
app = create_app()

# Ponto de entrada principal
if __name__ == '__main__':
    app.run(debug=True)