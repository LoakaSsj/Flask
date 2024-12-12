import mysql.connector

class UserModel:
    def __init__(self):
        self.con = mysql.connector.connect(
            host="185.232.14.52",
            database="u760464709_tst_sep",
            user="u760464709_tst_sep_usr",
            password="dJ0CIAFF="
        )
    
    def verificar_conexion(self):
        if not self.con.is_connected():
            self.con.reconnect()

    def obtener_usuarios(self):
        self.verificar_conexion()
        cursor = self.con.cursor()
        cursor.execute("SELECT * FROM tst0_usuarios ORDER BY Id_Usuario DESC")
        return cursor.fetchall()

    def guardar_usuario(self, usuario, contrasena):
        self.verificar_conexion()
        cursor = self.con.cursor()
        sql = "INSERT INTO tst0_usuarios (Nombre_Usuario, Contrasena) VALUES (%s, %s)"
        cursor.execute(sql, (usuario, contrasena))
        self.con.commit()

    def actualizar_usuario(self, id, usuario, contrasena):
        self.verificar_conexion()
        cursor = self.con.cursor()
        sql = "UPDATE tst0_usuarios SET Nombre_Usuario = %s, Contrasena = %s WHERE Id_Usuario = %s"
        cursor.execute(sql, (usuario, contrasena, id))
        self.con.commit()

    def eliminar_usuario(self, id):
        self.verificar_conexion()
        cursor = self.con.cursor()
        sql = "DELETE FROM tst0_usuarios WHERE Id_Usuario = %s"
        cursor.execute(sql, (id,))
        self.con.commit()
