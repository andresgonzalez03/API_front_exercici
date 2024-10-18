from client import db_client
import csv

# llegir tots els camps de la taula alumne 
def read(orderby: str | None = None,  contain: str | None = None, skip: int = 0, limit: int | None = None):
    try:
        conn = db_client()
        cur = conn.cursor()
        query = "select a.NomAlumne, a.Cicle, a.Curs, a.Grup, au.DescAula from Alumne a join Aula au on a.IdAula = au.IdAula"
        
        if contain:
            query += f" WHERE a.NomAlumne LIKE '%{contain}%'"

        if orderby:
            if orderby.lower() == "asc":
                query += " order by a.NomAlumne asc"
            elif orderby.lower() == "desc":
                query += " order by a.NomAlumne desc"

        if limit is not None:
            query += f" LIMIT {limit}"
            if skip:
                query += f" OFFSET {skip}"
        
        cur.execute(query)
        alumnes = cur.fetchall()
    
    except Exception as e:
        return {"status": -1, "message": f"Error de connexió:{e}" }
    
    finally:
        conn.close()
    
    return alumnes

# llegir tots els camps de la taula alumne filtrat per id
def read_id(id):
    try:
        conn = db_client()
        cur = conn.cursor()
        query = "SELECT * from Alumne where IdAlumne = %s;"
        value = (id,)
        cur.execute(query,value)
        alumne = cur.fetchone()
    except Exception as e:
        return {"status": -1, "message": f"Error de connexió:{e}" }
    finally: 
        conn.close()
    return alumne

# llegir tots els camps de la taula alumne i també veure la descripció de l'aula, l'edifici i el pis
def read_alumneAll():
    try:
        conn = db_client()
        cur = conn.cursor()
        query = "SELECT Alumne.*, Aula.DescAula, Aula.Edifici, Aula.Pis from Alumne join Aula on Alumne.IdAula = Aula.IdAula;"
        cur.execute(query)
        alumne = cur.fetchall()
    except Exception as e:
        return {"status": -1, "message": f"Error de connexió:{e}" }
    finally: 
        conn.close()
    return alumne

# crear alumne amb idAula
def create_alumne(IdAula, NomAlumne, Cicle, Curs, Grup):
        
    try:
        conn = db_client()
        cur = conn.cursor()
        query =  "INSERT INTO Alumne (IdAula, NomAlumne, Cicle, Curs, Grup) VALUES (%s,%s,%s,%s,%s);"
        values = (IdAula, NomAlumne, Cicle, Curs, Grup)
        cur.execute(query,values)
        conn.commit()
        alumne_id = cur.lastrowid
    except Exception as e:
        return {"status": -1, "message": f"Error de connexió:{e}" }
    
    finally:
        conn.close()
    return alumne_id

# crear alumne amb DescAula

# modificar alumne
def update_alumne(IdAlumne, IdAula, NomAlumne, Cicle, Curs, Grup):
    try:
        conn = db_client()
        cur = conn.cursor()  
        
        if not check_idAlumne_exists(IdAlumne):
            return {"status": -1, "message": "IdAlumne no existeix"}
        
        query = "update Alumne SET IdAula = %s, NomAlumne = %s, Cicle = %s, Curs = %s, Grup = %s where IdAlumne = %s;"
        values=(IdAula, NomAlumne, Cicle, Curs, Grup, IdAlumne)
        cur.execute(query,values)
        updated_alumnes = cur.rowcount
    
        conn.commit()
    
    except Exception as e:
        return {"status": -1, "message": f"Error de connexió:{e}" }
    
    finally:
        conn.close()

    return updated_alumnes

# eliminar un alumne a partir de la seva id
def delete_alumne(id):
    if not check_idAlumne_exists(id):
        return {"status": -1, "message": "IdAlumne no existeix"}  
    try:
        conn = db_client()
        cur = conn.cursor()
        query = "delete from Alumne where IdAlumne = %s"
        cur.execute(query,(id,))
        deleted_alumnes = cur.rowcount
        conn.commit()
    except Exception as e:
        return {"status": -1, "message": f"Error de connexió:{e}" }
    
    finally:
        conn.close()
        
    return deleted_alumnes

# crear un aula
def create_aula(DescAula, Edifici, Pis):
    if check_DescAula(DescAula):
        return {"status": -1, "message": "L'aula amb aquesta Descripció ja existeix"}
    try:
        conn = db_client()
        cur = conn.cursor()
        query =  "INSERT INTO Aula (DescAula, Edifici, Pis) VALUES (%s,%s,%s);"
        values = (DescAula, Edifici, Pis)
        cur.execute(query,values)
        conn.commit()
        aula_id = cur.lastrowid # accedeix a l'id de l'última fila que s'ha afegit
    except Exception as e:
        return {"status": -1, "message": f"Error de connexió:{e}" }
    
    finally:    
        conn.close()
    return aula_id

# llegeix un csv
def llegirCsv(file):
    
    # llegir el csv
    contents = file.file.read() 
    lines = contents.decode().splitlines() 

    reader = csv.reader(lines[1:])  
    for row in reader:
        if len(row) < 7:  # verifica que el csv sempre tingui 6 columnes
            continue

        DescAula, Edifici, Pis, NomAlumne, Cicle, Curs, Grup = row # a la variable row, li asigna els valors del csv
        
        # verificar si el aula ya existe
        if not check_DescAula(DescAula):
            # insertar el aula en la base de datos
            create_aula(DescAula, Edifici, Pis) 

        # verificar si l'alumne existeix
        if not check_Alumne(NomAlumne, Cicle, Curs, Grup):
            IdAula = get_IdAulaByDescAula(DescAula)
            # fer insert de l'alumne
            create_alumne(IdAula, NomAlumne, Cicle, Curs, Grup) 
    
    return "Càrrega feta amb èxit"

##################### CHECKS #####################

# verifica si el id de l'aula existeix
def check_idAula(idAula):
    try: 
        conn = db_client()
        cur = conn.cursor()
        query = "select count(*) from Aula where IdAula = %s;"
        cur.execute(query,(idAula,))
        count = cur.fetchone()[0]
        return count > 0
    except Exception as e:
        print(f"Error al verificar IdAula: {e}")
        return False
    finally:
        conn.close()    
        
# verifica si el id de l'alumne existeix
def check_idAlumne_exists(IdAlumne):
    try:
        conn = db_client()
        cur = conn.cursor()
        query = "select count(*) from Alumne where IdAlumne = %s;"
        cur.execute(query, (IdAlumne,))
        count = cur.fetchone()
        return count[0] > 0 if count else False
    except Exception as e:
        print(f"Error al verificar IdAlumne: {e}")
        return False 
    finally:
        conn.close()
    
# verifica l'aula depenent de la seva descripció
def check_DescAula(DescAula): 
    try:
        conn = db_client()
        cur = conn.cursor()
        query = "select count(*) from Aula where DescAula = %s;"
        cur.execute(query, (DescAula,))
        count = cur.fetchone()
        return count[0] > 0 if count else False
    except Exception as e:
        print(f"Error al verificar DescAula: {e}")
        return False 
    finally:
        conn.close()
    
# getter per obtenir el IdAula a partir de la seva descripció
def get_IdAulaByDescAula(DescAula): 
    try:
        conn = db_client()
        cur = conn.cursor()
        query = "select IdAula from Aula where DescAula = %s;"
        cur.execute(query, (DescAula,))
        count = cur.fetchone()
        return count[0] if count else False
    except Exception as e:
        print(f"Error al verificar DescAula: {e}")
        return False
    finally:
        conn.close()
    
# verifica un alumne a partir de certs paràmetres    
def check_Alumne(NomAlumne, Cicle, Curs, Grup):
    try:
        conn = db_client()
        cur = conn.cursor()
        query = "select count(*) from Alumne where NomAlumne = %s and Cicle = %s and Curs = %s and Grup = %s;"
        cur.execute(query, (NomAlumne,Cicle,Curs,Grup,))
        count = cur.fetchone()
        return count[0] > 0 if count else False
    except Exception as e:
        print(f"Error al verificar NomAlumne: {e}")
        return False 
    finally:
        conn.close()
