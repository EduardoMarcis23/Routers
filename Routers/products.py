###################################
########## MAIN DE FASTAPI ########
###################################

from fastapi import APIRouter

#Si se le indica el prefijo esa sera la ruta que tomara despues de la raiz
router = APIRouter(prefix="/products",
                   #El tag los agrupo, principalmente para la doc
                   tags = ["producst"],
                   responses={404 : {"Message":"No encontrado"}})

products_list = ["Producto 1", "Producto 2",
                 "Producto 3", "Producto 4", "Producto 5"]

# Sin el prefix queda asi
#@router.get("/products")
@router.get("/")
async def products():
    return products_list

@router.get("/{id}")
async def products(id:int):
    return products_list[id-1]