import mysql.connector
    
def db_client():
    
    try:
        dbname = "Alumnat"
        user = "root"
        password = ""
        host = "localhost"
        port = "3306"
        
        return mysql.connector.connect(
            host = host,
            port = port,
            user = user,
            password = password,
            database = dbname 
        ) 
            
    except Exception as e:
            return {"status": -1, "message": f"Error de connexió:{e}" }