import sqlite3 as sql

def createDB():
    conn = sql.connect("Rose.db")
    conn.commit()
    conn.close()


def createTable():
    conn = sql.connect("Rose.db")
    cursor = conn.cursor()
    
    
    cursor.execute(
        """CREATE TABLE IF NOT EXISTS usuarios (
            correo TEXT,
            contraseña TEXT
            )"""
    )
    
   
    cursor.execute(
        """CREATE TABLE IF NOT EXISTS registrarse (
            correo TEXT,
            contraseña TEXT,
            repetir contraseña TEXT
            )"""
    )

    conn.commit()
    conn.close()

    
    
def insertRow(correo, contraseña):
    conn = sql.connect("Rose.db")
    cursor = conn.cursor()
    instruccion = f"INSERT INTO usuarios VALUES ('{correo}', '{contraseña}')"
    cursor.execute(instruccion)  
    conn.commit()
    conn.close()


if __name__ == "__main__":
    createDB()
    createTable()
    insertRow("Administrador", "Admin")