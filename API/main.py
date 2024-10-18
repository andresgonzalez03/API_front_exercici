from fastapi import FastAPI,HTTPException
import db_alumnes
import alumnes
from typing import List
from pydantic import BaseModel
from fastapi.middleware.cors import CORSMiddleware
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
    NomAlumne: str
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
        
# endpoint que retorna una llista d'alumnes i permet utilitzar paràmeters de query
@app.get("/alumne/list", response_model=List[tablaAlumne])
def read_alumnes(orderby: str | None = None,  contain: str | None = None, skip: int = 0, limit: int | None = None ):
    alumnes_data = db_alumnes.read(orderby=orderby, contain=contain, skip=skip, limit=limit)
    if not alumnes_data:  
        raise HTTPException(status_code=404, detail="No s'ha trobat cap alumne")
    
    return alumnes.alumnes_schema(alumnes_data)

# endpoint que retorna un alumne pel seu id
@app.get("/alumne/show/{id}")
def read_alumne_id(id:int):
    if db_alumnes.read_id(id) is not None:
        alumne = alumnes.alumne_schema(db_alumnes.read_id(id))
    else:
        raise HTTPException(status_code=404, detail="No s'ha trobat cap alumne amb aquesta ID")
    return alumne

# endpoint que retorna una llista de tots els alumnes i les seves dades
@app.get("/alumne/listAll")
def read_alumne_all():
    alumnes_data = db_alumnes.read_alumneAll()
    if alumnes_data:
       return alumnes.alumnes_schema_all(alumnes_data)
    else:
        raise HTTPException(status_code=404, detail="No s'ha trobat cap alumne amb aquesta ID")
    

# crea un alumne 
@app.post("/alumne/add")
def create_alumne(data: Alumne):
    
    # obtenir les dades de l'alumne a partir de l'objecte que li passem per paràmetre
    IdAula = data.IdAula
    NomAlumne = data.NomAlumne
    Cicle = data.Cicle
    Curs = data.Curs
    Grup = data.Grup
    
    # verificar si l'aula existeix, gràcies al idAula proporcionat pel nou alumne si no existeix, llança una excepció
    idAula_exists = db_alumnes.check_idAula(IdAula)
    if not idAula_exists:
        raise HTTPException(status_code=400, detail="L'aula no existeix. Si us plau, creeu l'aula abans d'afegir un alumne. Fes /aula/add per afegir un aula")
    
    #  verificar si l'alumne existeix, si ja existeix llança una excepció, sinó segueix amb la creació de l'alumne
    alumne_exists = db_alumnes.check_Alumne(NomAlumne, Cicle, Curs, Grup)
    if alumne_exists:
        raise HTTPException(status_code=400, detail="L'alumne ja existeix.")
    
    # crea l'alumne si tot va bé
    alumne_id = db_alumnes.create_alumne(IdAula,NomAlumne, Cicle, Curs, Grup)
    
    return {
        "msg": "S’ha afegit correctement",
        "id Alumne": alumne_id,
        "nom": NomAlumne
    }


# endpoint que actualitza un alumne a partir de la seva id
@app.put("/alumne/update/{id}")
def update_alumne(id:int, data: AlumneUpdate): # hago id:int porque en este caso los objetos de tipo AlumneUpdate no tienen la propiedad IdAlumne y por lo tanto no puedo acceder a ella
    if not db_alumnes.check_idAlumne_exists(id):
        raise HTTPException(status_code=404, detail=f"No s'ha trobat cap alumne amb id: {id}") 
    db_alumnes.update_alumne(id, data.IdAula, data.NomAlumne, data.Cicle, data.Curs, data.Grup)
    return {
        "msg": f"S'ha modificat l'alumne amb id: {id}"
    } 

# endpoint que esborrra un alumne a partir de la seva id    
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
    return db_alumnes.llegirCsv(fitxer)
    
# endpoint que crea un aula, però verifica si no es repeteix la descripció d'aquesta nova aula en una que ja existeix
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