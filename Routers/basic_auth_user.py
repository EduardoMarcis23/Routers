#########################################
########## AUTENTICACION AUTH2  #########
#########################################

from fastapi import APIRouter, Depends, HTTPException
from pydantic import BaseModel
from fastapi.security import OAuth2PasswordBearer, OAuth2PasswordRequestForm

router = APIRouter()

#Pasamos la URL donde se autenticara
oauth2 = OAuth2PasswordBearer(tokenUrl="login")

#Usuario para trabajar en el cliente
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
                        "password" : "123456"
                        },
            "Mouredev" : {
                        "username" : "Mouredev",
                        "fullName" : "Brais",
                        "email" : "braismoure@gmail.com",
                        "disabled" : True,
                        "password" : "654321"
                        }
            }


#   Verificacion de usuario (recuerde tipar datos)
# Buscamos el usuario recibido en cliente dentro del server
def search_user_db(username:str):
    if username in users_db:
        return UserDB(**users_db[username])
        #Los 2 asteriscos indican que pueden ir varios parametros

def search_user(username:str):
    if username in users_db:
        return User(**users_db[username])
    

#criterio de dependencia para cuando valide
async def current_user(token:str = Depends(oauth2)):
    user = search_user(token)
    if not user:
        raise HTTPException(status_code=401 , detail="Usuario no autorizado",
                            headers={"WWW-Authenticate":"Bearer"})
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
    if not form.password == user.password:
        raise HTTPException(400, detail="Password incorrecto")
    
    return {"access_token":user.username,"token_type":"bearer"}

@router.get("/users/me")
async def me(user:User=Depends(current_user)):
    return user