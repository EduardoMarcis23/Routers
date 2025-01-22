###################################
########## API PARA USERS #########
###################################

from fastapi import APIRouter, HTTPException
from pydantic import BaseModel

#Instanciamos la fastapi
router = APIRouter(prefix="/users",
                   #El tag los agrupo, principalmente para la documentacion
                   tags = ["/users"],
                   responses={404 : {"Message":"No encontrado"}})
# En esta caso el server se inicia con uvicorn users:router --reload

# Entidad user
class User(BaseModel):
    id : int
    name : str
    Surname : str
    url : str
    age : int

users_list = [User(id = 1, name = "Eduardo", Surname = "Marcelino", url = "127.0.0.8", age =27),
            User(id = 2, name = "Moure", Surname = "Dev", url = "https://mouredev.com", age = 35),
            User(id = 3, name = "Haakon", Surname = "Dahlberg", url = "https://haakon", age =33),]

@router.get("/usersjson")
async def usersjson():
    return [{"name":"Eduardo","Surname":"Marcelino","url":"127.0.0.8","age":27},
            {"name":"Moure","Surname":"Dev","url":"https://mouredev.com","age":35},
            {"name":"Haakon","Surname":"Dahlberg","url":"https://haakon","age":33}]

@router.get("/users/")
async def users():
    return users_list

#Pedimos el id mediante el PATH
@router.get("/user/{id}")
async def user(id:int):
    return search_user(id)

# Obtenemos usuario por Query
@router.get("/userquery/")
async def user(id:int):
    return search_user(id)

# Nuestro primer agregacion POST
# De igual manera cambiamos el codigo de status
@router.post("/user/", status_code=201)
#Vemos que ingresamos un objeto de tipo usuario y es todo   
async def user(user: User):
    if type(search_user(user.id)) == User:
        # En caso de querer lanzar nuestro propio codigo de error
        #  y no solo el mensaje con return
        raise HTTPException(304, detail="Ya existe usuario")
        #return {"ERROR":"Ya existe usuario"}
    else:
        users_list.append(user)
        return user 

# Nuestro primer actualizacion PUT 
@router.put("/user/")
# Podemos actualizar el objeto completo o por campo   
async def user(user: User):
    found = False
    for index, saved_user in enumerate(users_list):
        if saved_user.id == user.id:
            users_list[index] = user
            found = True
    if not found:
        return {"ERROR":"No existe usuario"}
    else:
        return user

# Nuestro primer Delete
@router.delete("/user/{id}") 
async def user(id: int):
    found = False
    for index, saved_user in enumerate(users_list):
        if saved_user.id == id:
            del users_list[index]
            found = True

    if not found:
        return {"ERROR":"No existe usuario"}

def search_user(id : int):
    users = filter(lambda user: user.id == id, users_list)
    try:
        return list(users)[0]
    except:
        return {"ERROR":"No existe usuario"}
    
