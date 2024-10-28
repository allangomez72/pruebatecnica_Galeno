from typing import Annotated
from fastapi import APIRouter, Depends, HTTPException, status
from schema.user_schema import UserSchema
from config.db import conn
from model.user import user
from fastapi.security import OAuth2PasswordBearer, OAuth2PasswordRequestForm
from passlib.context import CryptContext
from datetime import datetime, timedelta
import jwt
import httpx

# Configuración
SECRET_KEY = "9d25e094faa6ca2556c818166b7a9563b93f70"
ALGORITHM = "HS256"
ACCESS_TOKEN_EXPIRE_MINUTES = 30

# Datos para la API externa
EXTERNAL_API_LOGIN_URL = "https://apiexamen.compuflashgt.com/api/Login"
EXTERNAL_API_USERNAME = "1000"
EXTERNAL_API_PASSWORD = "!G4l3n0!"
EXTERNAL_API_KEY = "62245354621022924456"

pwd_context = CryptContext(schemes=["bcrypt"], deprecated="auto")
oauth2_scheme = OAuth2PasswordBearer(tokenUrl="token")

user_router = APIRouter()

# Funciones de ayuda
def verify_password(plain_password, hashed_password):
    return pwd_context.verify(plain_password, hashed_password)

def get_password_hash(password):
    return pwd_context.hash(password)

def create_access_token(data: dict, expires_delta: timedelta | None = None):
    to_encode = data.copy()
    expire = datetime.utcnow() + (expires_delta or timedelta(minutes=15))
    to_encode.update({"exp": expire})
    return jwt.encode(to_encode, SECRET_KEY, algorithm=ALGORITHM)


async def authenticate_external_user():
    async with httpx.AsyncClient() as client:
        response = await client.post(EXTERNAL_API_LOGIN_URL, json={
            "Usuario": EXTERNAL_API_USERNAME,
            "Contraseña": EXTERNAL_API_PASSWORD,
            "API_KEY": EXTERNAL_API_KEY
        })
        if response.status_code == 200:
            return response.json()
        else:
            raise HTTPException(status_code=response.status_code, detail="Fallo la autentificacion de la API")


# Rutas de usuario y autenticación
@user_router.get('/')
def root():
    return {"message": "Hello World"}


@user_router.post('/api/user')
def create_user(data_user: UserSchema):
    hashed_password = get_password_hash(data_user.password)
    new_user = {"username": data_user.username, "name": data_user.name, "password": hashed_password}
    conn.execute(user.insert().values(new_user))
    return {"msg": "User created successfully"}


@user_router.post('/token')
def login(form_data: Annotated[OAuth2PasswordRequestForm, Depends()]):
    query = user.select().where(user.c.username == form_data.username)
    db_user = conn.execute(query).first()

    if not db_user or not verify_password(form_data.password, db_user.password):
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Usuario incorrecto o password",
            headers={"WWW-Authenticate": "Bearer"},
        )

    access_token_expires = timedelta(minutes=ACCESS_TOKEN_EXPIRE_MINUTES)
    access_token = create_access_token(data={"sub": db_user.username}, expires_delta=access_token_expires)
    return {"access_token": access_token, "token_type": "bearer"}


# Rutas de productos, carrito y reportes
@user_router.get('/api/products')
async def get_products():
    # Autenticarse en la API externa y obtener el token
    external_auth = await authenticate_external_user()
    external_token = external_auth.get("Token")

    # Ahora usa el token externo para obtener productos
    async with httpx.AsyncClient() as client:
        response = await client.get('https://apiexamen.compuflashgt.com/api/getProductos',
                                    headers={"Authorization": f"Bearer {external_token}"})
        if response.status_code != 200:
            raise HTTPException(status_code=response.status_code, detail="Error fetching products from external API")
        return response.json()


@user_router.post('/api/cart')
def anadir_carrito(product_id: int, quantity: int, token: Annotated[str, Depends(oauth2_scheme)]):
    return {"msg": "Producto añadido al carrito"}


@user_router.get('/api/reports')
def generar_reporte(token: Annotated[str, Depends(oauth2_scheme)]):
    return {"report": "Reporte de compras"}
