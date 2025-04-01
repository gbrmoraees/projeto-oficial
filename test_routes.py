from flask_restx import Api, Resource, fields

api = Api(
    title="API de Autenticação",
    version="1.0",
    description="Documentação interativa da API",
    doc="/docs",  # URL da documentação
    default="Auth",
    default_label="Endpoints de Autenticação"
)

# Modelo para documentação do payload
user_model = api.model('User', {
    'email': fields.String(required=True, example="user@example.com"),
    'password': fields.String(required=True, example="Senha@123")
})
app/api/auth.py (Exemplo de endpoint documentado):
python
Copy
from .docs import api, user_model

ns = api.namespace('auth', description='Operações de autenticação')

@ns.route('/register')
class UserRegister(Resource):
    @ns.expect(user_model, validate=True)
    @ns.response(201, 'Usuário criado com sucesso')
    @ns.response(400, 'Validação falhou')
    def post(self):
        """Registro de novo usuário"""
        data = api.payload
        # ... sua lógica de registro ...
        return {"message": "Usuário registrado!"}, 201
3. Configuração Avançada (FastAPI - Recomendado)
main.py:
python
Copy
from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware

app = FastAPI(
    title="API de Autenticação",
    description="Documentação Swagger/OpenAPI",
    version="0.1.0",
    openapi_url="/api/v1/openapi.json"
)



app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_methods=["*"],
    allow_headers=["*"],
)

@app.post("/auth/register", response_model=UserResponse, tags=["Autenticação"])
async def register(user: UserCreate):
    """Endpoint para registro de usuários
    
    - **email**: deve ser um email válido
    - **password**: mínimo 8 caracteres
    """
    .
    return user
schemas.py (Modelos Pydantic):
python
Copy
from pydantic import BaseModel, EmailStr

class UserCreate(BaseModel):
    email: EmailStr
    password: str = Field(..., min_length=8, example="Senha@123")

class UserResponse(BaseModel):
    id: int
    email: EmailStr
    class Config:
        schema_extra = {
            "example": {
                "id": 1,
                "email": "user@example.com"
            }
        }
4. Visualização da Documentação
Flask-RESTX: Acesse http://localhost:5000/docs

FastAPI: Acesse http://localhost:8000/docs (Swagger UI) ou http://localhost:8000/redoc (ReDoc)

Swagger UI Example

5. Melhores Práticas
a. Tags e Organização
python
Copy
@api_tags(['Autenticação', 'Usuários'])  # Flask-RESTX
# OU
@app.post(..., tags=["Autenticação"])  # FastAPI
b. Respostas Personalizadas
python
Copy
# Flask-RESTX
@ns.response(404, 'Usuário não encontrado', error_model)

# FastAPI
from fastapi.responses import JSONResponse
@app.post(..., responses={
    404: {"description": "Usuário não encontrado", "model": ErrorResponse}
})
c. Segurança (JWT no Swagger)
python
Copy
# FastAPI
app = FastAPI(swagger_ui_parameters={"defaultModelsExpandDepth": -1})

# Adicionar autenticação
security_scheme = {
    "type": "http",
    "scheme": "bearer",
    "bearerFormat": "JWT"
}

app.openapi_schema = {
    "components": {
        "securitySchemes": {
            "BearerAuth": security_scheme
        }
    }
}
6. Exemplo Completo (FastAPI)
main.py:
python
Copy
from fastapi import FastAPI, Depends, HTTPException
from pydantic import BaseModel

app = FastAPI()

class User(BaseModel):
    email: str
    password: str

users_db = []

@app.post("/register/", tags=["Autenticação"])
async def register(user: User):
    """Registra um novo usuário
    
    - **email**: deve ser único
    - **password**: mínimo 8 caracteres
    """
    if any(u.email == user.email for u in users_db):
        raise HTTPException(status_code=400, detail="Email já registrado")
    
    users_db.append(user)
    return {"message": "Usuário criado com sucesso"}
Testando:
Execute: uvicorn main:app --reload

Acesse: http://localhost:8000/docs

7. Dicas Avançadas
Validação Customizada:

python
Copy
from pydantic import validator

class UserCreate(BaseModel):
    @validator('password')
    def password_complexity(cls, v):
        if len(v) < 8:
            raise ValueError("Senha muito curta")
        return v
Marcar Endpoints como Deprecados:

python
Copy
@app.get("/old-endpoint/", deprecated=True)
Agrupamento por Tags:

python
Copy
app.openapi_tags = [
    {
        "name": "Autenticação",
        "description": "Operações de login e registro"
    }
]
Adicionar Exemplos:

python
Copy
class UserCreate(BaseModel):
    email: str = Field(..., example="user@example.com")
    password: str = Field(..., example="Senha@123", min_length=8)