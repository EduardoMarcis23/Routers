#######################################
########## AUTENTICACION JWT  #########
#######################################

from fastapi import APIRouter, Depends, HTTPException
from pydantic import BaseModel
from fastapi.security import OAuth2PasswordBearer, OAuth2PasswordRequestForm
from jose import jwt, JWTError
from passlib.context import CryptContext
from datetime import datetime, timedelta

#   ALGORITMO PARA PASSWORD
ALGORITHM = "HS256"
ACCESS_TOKEN_DURATION = 1
SECRET = "db89ebs4ber89b7s89b1eadb8wf859sd4f89ds4vds8v" #Esta es la semilla para cifrar

router = APIRouter()
oauth2 = OAuth2PasswordBearer(tokenUrl="login")
crypt = CryptContext(schemes=["bcrypt"])

class User(BaseModel):
    username : str
    fullName : str
    email : str
    disabled : bool

#Usuario para trabajar en Server
class UserDB(User):
    password : str

users_db = {
            "Eduardo" : {
                        "username" : "Eduardo",
                        "fullName" : "Marcelino",
                        "email" : "eduardomar@gmail.com",
                        "disabled" : False,
                        "password" : "$2a$12$Eweax0HLu04krAiundTeoecjpYpmqiNLcbbKmrYukIB6e.p/gCxxq"
                        },
            "Mouredev" : {
                        "username" : "Mouredev",
                        "fullName" : "Brais",
                        "email" : "braismoure@gmail.com",
                        "disabled" : True,
                        "password" : "$2a$12$tgENWFXFZw3KmU8vwinn6eaPJtzY5KTfVAg/COcYGrv.fHLnJ2WkG"
                        }
            }

def search_user_db(username:str):
    if username in users_db:
        return UserDB(**users_db[username])
        #Los 2 asteriscos indican que pueden ir varios parametros

def search_user(username:str):
    if username in users_db:
        return User(**users_db[username])
    
async def auth_user(token:str = Depends(oauth2)):
    exception = HTTPException(status_code=401 , detail="Usuario no autorizado",
                            headers={"WWW-Authenticate":"Bearer"})

    try:
        username = jwt.decode(token, SECRET, algorithms=[ALGORITHM]).get("sub")
        if username is None:
            raise exception
        
    except JWTError:
        raise exception
    
    return search_user(username)

    
async def current_user(user:User = Depends(auth_user)):
    if user.disabled:
        raise HTTPException(status_code=400 , detail="Usuario inactivo")
    return user

@router.post("/login")
#Usamos el formulario de la libreria importada
async def login(form: OAuth2PasswordRequestForm = Depends()):
    user_db = users_db.get(form.username)
    if not user_db:
        raise HTTPException(404, detail="No existe usuario")
    
    user = search_user_db(form.username)

    #   Crypt verifica la contrasena crifrada con la que le pasa
    # el usuario ya cifrada
    
    if not crypt.verify(form.password,user.password):
        raise HTTPException(400, detail="Password incorrecto")
    
    #   Creando el token de forma segura
    #   Se crea una fecha de expiracion 
    # que es la hora y fecha actual mas la duracion ya creada
    expire = datetime.utcnow() + timedelta(minutes=ACCESS_TOKEN_DURATION)
    access_token = {
                    "sub" : user.username,
                    "exp" : expire
                    }
    # Se cread un token cifrado de un json
    return {"access_token":jwt.encode(access_token,
                                      SECRET, algorithm=ALGORITHM),
                                      "token_type":"bearer"}

@router.get("/users/me")
async def me(user:User=Depends(current_user)):
    return user