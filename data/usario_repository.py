from data.database import get_connection
from models.usario import Usuario
from models.filme import Filme
from models.serie import Serie
from models.slap_review import SlapReview

class UsuarioRepository:

    @staticmethod
    def salvar(usuario: Usuario):

        conn = get_connection()
        cursor = conn.cursor()

        sql = """
        INSERT INTO usuarios
        (username,nome_completo,cpf,senha,bio,foto_url,idade,ativo)
        VALUES (%s,%s,%s,%s,%s,%s,%s,%s)
        """

        cursor.execute(sql, (
            usuario.username,
            usuario.nome_completo,
            usuario.cpf,
            usuario.senha,
            usuario.bio,
            usuario.foto_url,
            usuario.idade,
            usuario.ativo
        ))

        conn.commit()
        cursor.close()
        conn.close()

    @staticmethod
    def buscar_por_username(username):

        conn = get_connection()
        cursor = conn.cursor(dictionary=True)

        sql = """
        SELECT *
        FROM usuarios
        WHERE username = %s
        """

        cursor.execute(sql, (username,))
        resultado = cursor.fetchone()

        cursor.close()
        conn.close()

        if resultado:

            return Usuario(
                username=resultado["username"],
                nome_completo=resultado["nome_completo"],
                cpf=resultado["cpf"],
                senha=resultado["senha"],
                bio=resultado["bio"],
                foto_url=resultado["foto_url"],
                idade=resultado["idade"],
                ativo=resultado["ativo"]
            )

        return None

    @staticmethod
    def buscar_por_cpf(cpf):

        conn = get_connection()
        cursor = conn.cursor(dictionary=True)

        sql = """
        SELECT *
        FROM usuarios
        WHERE cpf = %s
        """

        cursor.execute(sql, (cpf,))
        resultado = cursor.fetchone()

        cursor.close()
        conn.close()

        if resultado:

            return Usuario(
                username=resultado["username"],
                nome_completo=resultado["nome_completo"],
                cpf=resultado["cpf"],
                senha=resultado["senha"],
                bio=resultado["bio"],
                foto_url=resultado["foto_url"],
                idade=resultado["idade"],
                ativo=resultado["ativo"]
            )

        return None
 
    @staticmethod
    def listar_todos():

        conn = get_connection()
        cursor = conn.cursor(dictionary=True)

        cursor.execute("SELECT * FROM usuarios")

        resultados = cursor.fetchall()

        usuarios = []

        for row in resultados:
            usuarios.append(
                Usuario(
                    username=row["username"],
                    nome_completo=row["nome_completo"],
                    cpf=row["cpf"],
                    senha=row["senha"],
                    bio=row["bio"],
                    foto_url=row["foto_url"],
                    idade=row["idade"],
                    ativo=row["ativo"]
                )
            )

        cursor.close()
        conn.close()

        return usuarios

    @staticmethod
    def atualizar(usuario):

        conn = get_connection()
        cursor = conn.cursor()

        sql = """
        UPDATE usuarios
        SET nome_completo=%s,
            bio=%s,
            foto_url=%s,
            idade=%s
        WHERE username=%s
        """

        cursor.execute(sql, (
            usuario.nome_completo,
            usuario.bio,
            usuario.foto_url,
            usuario.idade,
            usuario.username
        ))

        conn.commit()
        cursor.close()
        conn.close()