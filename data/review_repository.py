from data.database import get_connection
from models.models import SlapReview

class ReviewRepository:

    @staticmethod
    def salvar(review: SlapReview):

        conn = get_connection()
        cursor = conn.cursor()

        curtidas = ",".join(review.curtidas)

        respostas = "||".join([
            f"{r['usuario']}#{r['data']}#{r['texto']}#{r.get('media','NULO')}"
            for r in review.respostas
        ])

        sql = """
        INSERT INTO reviews
        (
            id,
            item_id,
            usuario,
            nome_usuario,
            veredito,
            impacto_moral,
            emocao,
            comentario_acido,
            gif_url,
            curtidas,
            respostas,
            data_criacao
        )
        VALUES
        (%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s)
        """

        cursor.execute(sql, (
            review.id,
            review.item_id,
            review.usuario,
            review.nome_usuario,
            review.veredito,
            review.impacto_moral,
            review.emocao,
            review.comentario_acido,
            review.gif_url,
            curtidas,
            respostas,
            review.data_criacao
        ))

        conn.commit()

        cursor.close()
        conn.close()

    @staticmethod
    def listar_todas():

        conn = get_connection()
        cursor = conn.cursor(dictionary=True)

        cursor.execute("SELECT * FROM reviews")

        resultados = cursor.fetchall()

        reviews = []

        for row in resultados:

            curtidas = []

            if row["curtidas"]:
                curtidas = row["curtidas"].split(",")

            respostas = []

            if row["respostas"]:

                for resp in row["respostas"].split("||"):

                    partes = resp.split("#")

                    respostas.append({
                        "usuario": partes[0],
                        "data": partes[1],
                        "texto": partes[2],
                        "media": partes[3]
                    })

            reviews.append(
                SlapReview(
                    id=row["id"],
                    item_id=row["item_id"],
                    usuario=row["usuario"],
                    nome_usuario=row["nome_usuario"],
                    veredito=row["veredito"],
                    impacto_moral=row["impacto_moral"],
                    emocao=row["emocao"],
                    comentario_acido=row["comentario_acido"],
                    gif_url=row["gif_url"],
                    curtidas=curtidas,
                    respostas=respostas,
                    data_criacao=row["data_criacao"]
                )
            )

        cursor.close()
        conn.close()

        return reviews

    @staticmethod
    def excluir(review_id):

        conn = get_connection()
        cursor = conn.cursor()

        cursor.execute(
            "DELETE FROM reviews WHERE id=%s",
            (review_id,)
        )

        conn.commit()

        cursor.close()
        conn.close()

    @staticmethod
    def atualizar(review):

        conn = get_connection()
        cursor = conn.cursor()

        curtidas = ",".join(review.curtidas)

        respostas = "||".join([
            f"{r['usuario']}#{r['data']}#{r['texto']}#{r.get('media','NULO')}"
            for r in review.respostas
        ])

        sql = """
        UPDATE reviews
        SET curtidas=%s,
            respostas=%s
        WHERE id=%s
        """

        cursor.execute(
            sql,
            (curtidas, respostas, review.id)
        )

        conn.commit()
        cursor.close()
        conn.close()