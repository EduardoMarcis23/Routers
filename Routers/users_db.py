#####################################
########## API USERS CON DB #########
#####################################

from fastapi import APIRouter, HTTPException, status
from db.models.user import User
from db.client import db_client
from db.schemas.user import user_schema, users_schema
from typing import List
from bson import ObjectId

#Instanciamos la fastapi
router = APIRouter(prefix="/userdb",
                   #El tag los agrupo, principalmente para la documentacion
                   tags = ["/userdb"],
                   responses={status.HTTP_404_NOT_FOUND : {"Message":"No encontrado"}})


@router.get("/", response_model=List[User])
async def users():
    return users_schema(db_client.users.find())

#Pedimos el id mediante el PATH
@router.get("/{id}")
async def user(id:str):
    return search_user("_id",ObjectId(id))

# Obtenemos usuario por Query
@router.get("/userquerydb")
async def user(id:str):
    return search_user("_id",ObjectId(id))

# Este post mete usuarios a la BD
@router.post("/", response_model=User, status_code=status.HTTP_201_CREATED)
async def user(user: User):

    if type(search_user("email",user.email)) == User:
        raise HTTPException(404, detail="Ya existe usuario")
    
    user_dict = dict(user)
    #Eliminamos el campo id al insertar para que Mongo lo genere
    del user_dict["id"]

    #Inserta un id Mongo
    id = db_client.users.insert_one(user_dict).inserted_id
    
    #Por convencio la el id por defecto que crea Mongo es "_id"
    # Ya que fue el autogenerado
    new_user = user_schema(db_client.users.find_one({"_id":id}))

    return User(**new_user) 

@router.put("/",response_model=User)
# Podemos actualizar el objeto completo o por campo   
async def user(user: User):
    try:
        user_dict = dict(user)
        del user_dict["id"]
        #   El critero para buscar el que remplazar es el id
        # y le pasamos el diccionario a remplazar
        db_client.users.find_one_and_replace({"_id":ObjectId(user.id)},user_dict)
    except:
        return {"ERROR":"No existe usuario"}
    return search_user("_id",ObjectId(user.id))

@router.delete("/{id}",status_code=status.HTTP_204_NO_CONTENT) 
async def user(id: str):
    found = db_client.users.find_one_and_delete({"_id":ObjectId(id)})
    if not found:
        return {"ERROR":"No existe usuario"}

def search_user(field : str, key):
    try:
        user = db_client.users.find_one({field:key})
        return User(**user_schema(user))
    except:
        return {"ERROR":"No existe usuario"}
    