from fastapi import FastAPI,HTTPException
import db_alumnes
import alumnes
from typing import List
from pydantic import BaseModel
from fastapi.middleware.cors import CORSMiddleware
import csv
from fastapi import FastAPI, File, UploadFile



app = FastAPI()

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],  
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)


# model d'alumne
class Alumne(BaseModel):
    IdAlumne: int
    IdAula: int
    NomClient: str
    Cicle : str
    Curs: str
    Grup: str

# model d'alumne actualitzat (no posso idAlumne, perquè no es pot actualitzar)
class AlumneUpdate(BaseModel):
    IdAula: int
    NomAlumne: str
    Cicle: str
    Curs: str
    Grup: str
    
class tablaAlumne(BaseModel):
    NomAlumne:str
    Cicle:str
    Curs:str
    Grup:str
    DescAula:str
  
class Aula(BaseModel):
    DescAula:str
    Edifici:str
    Pis:str

@app.get("/")
def read_root():
    return{"Alumnes API"}
        
# método que devuelve una lista de alumnos y permite usar cláusulas de query
@app.get("/alumne/list", response_model=List[tablaAlumne])
def read_alumnes(orderby: str | None = None,  contain: str | None = None, skip: int = 0, limit: int | None = None ):
    alumnes_data = db_alumnes.read(orderby=orderby, contain=contain, skip=skip, limit=limit)
    if not alumnes_data:  
        raise HTTPException(status_code=404, detail="No s'ha trobat cap alumne")
    
    return alumnes.alumnes_schema(alumnes_data)

# método que devuelve un alumno por su id
@app.get("/alumne/show/{id}")
def read_alumne_id(id:int):
    if db_alumnes.read_id(id) is not None:
        alumne = alumnes.alumne_schema(db_alumnes.read_id(id))
    else:
        raise HTTPException(status_code=404, detail="No s'ha trobat cap alumne amb aquesta ID")
    return alumne

@app.get("/alumne/listAll")
def read_alumne_all():
    alumnes_data = db_alumnes.read_alumneAll()
    if alumnes_data:
       return alumnes.alumnes_schema_all(alumnes_data)
    else:
        raise HTTPException(status_code=404, detail="No s'ha trobat cap alumne amb aquesta ID")
    return 

# crea un alumne 
"""
@app.post("/alumne/add")
def create_alumne(data: Alumne):
    
    # obtener los datos del alumno que recibe el método por parametro
    idAula = data.idAula
    nom = data.nom
    cicle = data.cicle
    curs = data.curs
    grup = data.grup
    
    # verificar si el aula existe, gracias al idAula proporcionado por ese alumno nuevo, si no existe, lanzar excepción
    idAula_exists = db_alumnes.check_idAula(idAula)
    if not idAula_exists:
        raise HTTPException(status_code=400, detail="L'aula no existeix. Si us plau, creeu l'aula abans d'afegir un alumne. Fes /aula/add per afegir un aula")
    
    # verificar si el alumno existe, si ya existe lanzar excepción, si no existe, seguir con la creación
    alumne_exists = db_alumnes.check_Alumne(nom,cicle,curs,grup)
    if alumne_exists:
        raise HTTPException(status_code=400, detail="L'alumne ja existeix.")
    
    # crea el alumno si todas las verificaciones pasan
    alumne_id = db_alumnes.create_alumne(idAula,nom,cicle, curs, grup)
    
    # mensaje para que el usuario obtenga feedback de lo que ha hecho
    return {
        "msg": "S’ha afegit correctement",
        "id Alumne": alumne_id,
        "nom": nom
    }
"""

@app.post("/alumne/add")
def create_alumneDescAula(data: tablaAlumne):
    # obtener los datos del alumno que recibe el método por parametro
    NomAlumne = data.NomAlumne
    Cicle = data.Cicle
    Curs = data.Curs
    Grup = data.Grup
    DescAula = data.DescAula
    
    # verificar si el aula existe, gracias al idAula proporcionado por ese alumno nuevo, si no existe, lanzar excepción
    idAula_exists = db_alumnes.check_DescAula(DescAula)
    if not idAula_exists:
        #TODO: si el aula no existe, crearla directamente con los valores obtenidos
       create_aula()
    
    # verificar si el alumno existe, si ya existe lanzar excepción, si no existe, seguir con la creación
    alumne_exists = db_alumnes.check_Alumne(NomAlumne, Cicle, Curs, Grup)
    if alumne_exists:
        raise HTTPException(status_code=400, detail="L'alumne ja existeix.")
    
    # crea el alumno si todas las verificaciones pasan
    alumne_id = db_alumnes.create_alumneDescAula(NomAlumne, Cicle, Curs, Grup, DescAula)
    
    # mensaje para que el usuario obtenga feedback de lo que ha hecho
    return {
        "msg": "S’ha afegit correctement",
        "id Alumne": alumne_id,
        "nom": NomAlumne
    }


# endpoint que actualiza a un alumno a partir de su id
@app.put("/alumne/update/{id}")
def update_alumne(id:int, data: AlumneUpdate): # hago id:int porque en este caso los objetos de tipo AlumneUpdate no tienen la propiedad IdAlumne y por lo tanto no puedo acceder a ella
    updated_alumnes = db_alumnes.update_alumne(id, data.IdAula, data.NomAlumne, data.Cicle, data.Curs, data.Grup)
    if updated_alumnes == 0:
        raise HTTPException(status_code=404, detail="No s'ha trobat res per actualitzar")  

# endpoint que borra un alumno a partir de su id    
@app.delete("/alumne/delete/{id}")
def delete_alumne(id:int):
    # trobem el nom de l'alumne per poder mostrar-lo per pantalla
    alumne_data = db_alumnes.read_id(id)
    if not alumne_data:
        raise HTTPException(status_code=404, detail="Alumne no trobat")
    # ara ja podem elimninar l'alumne
    db_alumnes.delete_alumne(id)
    return {"msg": f"S'ha eliminat l'alumne: {alumne_data[2]}"}

@app.post("/alumne/loadAlumnes")
def load_alumnes(fitxer: UploadFile):
    content = fitxer.file.read().decode()
    reader = csv.reader(content.splitlines(), delimiter=",")
    header = next(reader)
    for row in reader:
        row_formatted = [
            row[3], row[4], row[5], row[6], row[0]       
        ]
        ALUMNE = tablaAlumne(
            NomAlumne = row_formatted[0],
            Cicle = row_formatted[1],
            Curs = row_formatted[2],
            Grup = row_formatted[3],
            DescAula = row_formatted[4]
        )
        create_alumneDescAula(ALUMNE)
        

    
        

# endpoint que crea un aula a partir de su Descripción, si la descripción se repite en otro aula, lanza una excepción.
# TODO: "debo llamar a este método a la hora de leer el csv y tener que insertar los datos en la base de datos."
@app.post("/aula/add")
def create_aula(data: Aula):
    DescAula_exists = db_alumnes.check_DescAula(data.DescAula)
    if DescAula_exists:
        raise HTTPException(status_code=400, detail="El DescAula ja existeix.")

    DescAula = data.DescAula
    Edifici = data.Edifici
    Pis = data.Pis
    aula_id= db_alumnes.create_aula(DescAula, Edifici, Pis)
    
    return {
        "msg": "S’ha afegit correctement",
        "id Aula": aula_id,
        "DescAula": DescAula
    }