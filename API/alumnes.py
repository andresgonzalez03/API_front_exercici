def alumne_schema(alumne) -> dict:
    return {"NomAlumne": alumne[0],
            "Cicle": alumne[1],
            "Curs": alumne[2],
            "Grup": alumne[3],
            "DescAula": alumne[4]
            }
def alumnes_schema(alumnes) -> dict:
    return[alumne_schema(alumne) for alumne in alumnes]

def alumne_schema_all(alumne) -> dict:
    return {
        "IdAlumne": alumne[0],
        "IdAula": alumne[1],
        "NomAlumne": alumne[2],
        "Cicle": alumne[3],
        "Curs": alumne[4],
        "Grup": alumne[5],
        "DescAula": alumne[8],
        "Edifici": alumne[9],
        "Pis": alumne[10]
    }
def alumnes_schema_all(alumnes) -> dict:
    return[alumne_schema_all(alumne) for alumne in alumnes]