import streamlit as st
import uuid
import requests
import base64
from datetime import datetime
from typing import List, Dict
from models.filme import Filme
from models.serie import Serie
from models.slap_review import SlapReview
from models.usario import Usuario
from data.usario_repository import UsuarioRepository
from data.review_repository import ReviewRepository

class CinemaController:
    @staticmethod
    def inicializar_estados():
        if "pagina_atual" not in st.session_state: st.session_state["pagina_atual"] = "Login"
        if "item_selecionado" not in st.session_state: st.session_state["item_selecionado"] = None
        if "usuario_logado" not in st.session_state: st.session_state["usuario_logado"] = None
        if "tipo_conteudo" not in st.session_state: st.session_state["tipo_conteudo"] = "Filmes"
        if "gif_selecionado" not in st.session_state: st.session_state["gif_selecionado"] = ""

    @staticmethod
    def converter_upload_para_base64(uploaded_file) -> str:
        if uploaded_file is not None:
            try:
                bytes_data = uploaded_file.getvalue()
                base64_encoded = base64.b64encode(bytes_data).decode("utf-8")
                ext = uploaded_file.name.split(".")[-1].lower()
                if ext not in ["jpg", "jpeg", "png", "webp", "gif"]:
                    ext = "png"
                return f"data:image/{ext};base64,{base64_encoded}"
            except Exception:
                return ""
        return ""

    @staticmethod
    def efetuar_login(username: str, senha_in: str) -> bool:

        u_limpo = username.strip().lower()

        usuario = UsuarioRepository.buscar_por_username(u_limpo)

        if usuario and usuario.senha == senha_in and usuario.ativo:
            st.session_state["usuario_logado"] = usuario
            return True

        return False

    @staticmethod
    def cadastrar_usuario(username: str, nome: str, cpf: str, senha: str) -> tuple[bool, str]:

            u_limpo = username.strip().lower().replace("@", "")
            c_limpo = "".join(filter(str.isdigit, cpf))

            if not u_limpo or not nome.strip() or not senha.strip():
                return False, "Preencha todos os campos obrigatórios."

            if len(c_limpo) != 11:
                return False, "O CPF precisa de ter exatamente 11 dígitos numéricos."

            usuario_existente = UsuarioRepository.buscar_por_username(u_limpo)

            if usuario_existente:
                return False, f"O @{u_limpo} já está registado."

            novo = Usuario(
                username=u_limpo,
                nome_completo=nome.strip(),
                cpf=c_limpo,
                senha=senha
            )

            UsuarioRepository.salvar(novo)

        
            return True, f"Conta @{u_limpo} integrada com sucesso!"

    @staticmethod
    def atualizar_perfil(username: str, nome: str, bio: str, foto_base64: str, idade: str):

        u_limpo = username.strip().lower()

        usuario = UsuarioRepository.buscar_por_username(u_limpo)

        if usuario:

            usuario.nome_completo = nome.strip()
            usuario.bio = bio.strip()

        if foto_base64.strip():
            usuario.foto_url = foto_base64.strip()

        usuario.idade = idade.strip()

        UsuarioRepository.atualizar(usuario)

        st.session_state["usuario_logado"] = usuario

    @staticmethod
    def navegar_para(pagina: str, item=None):
        st.session_state["pagina_atual"] = pagina
        if item:
            st.session_state["item_selecionado"] = item
        st.rerun()

    @staticmethod
    def carregar_catalogo(busca: str, tipo: str) -> List:
        from services.services import CinemaService
        itens = []
        if tipo == "Filmes":
            resultados = CinemaService.buscar_filmes(busca) if busca else CinemaService.buscar_em_cartaz()
            for r in resultados:
                if r.get("poster_path"):
                    itens.append(Filme(
                        id=str(r["id"]), titulo=r["title"], sinopse=r.get("overview", "Sem sinopse."),
                        data_lancamento=r.get("release_date", ""), nota_media=r.get("vote_average", 0.0),
                        poster_url=f"https://image.tmdb.org/t/p/w500{r['poster_path']}"
                    ))
        else:
            resultados = CinemaService.buscar_series(busca) if busca else CinemaService.buscar_series_populares()
            for r in resultados:
                if r.get("poster_path"):
                    itens.append(Serie(
                        id=str(r["id"]), titulo=r["name"], sinopse=r.get("overview", "Sem sinopse."),
                        data_estreia=r.get("first_air_date", ""), nota_media=r.get("vote_average", 0.0),
                        poster_url=f"https://image.tmdb.org/t/p/w500{r['poster_path']}"
                    ))
        return itens

    @staticmethod
    def buscar_filme_detalhes(filme_id: str):
        from services.services import CinemaService
        r = CinemaService.obter_detalhes_filme(filme_id)
        if r and "title" in r:
            return Filme(
                id=str(r["id"]), titulo=r["title"], sinopse=r.get("overview", ""),
                data_lancamento=r.get("release_date", ""), nota_media=r.get("vote_average", 0.0),
                poster_url=f"https://image.tmdb.org/t/p/w500{r.get('poster_path', '')}"
            )
        return None

    @staticmethod
    def buscar_serie_detalhes(serie_id: str):
        from services.services import CinemaService
        r = CinemaService.obter_detalhes_serie(serie_id)
        if r and "name" in r:
            return Serie(
                id=str(r["id"]), titulo=r["name"], sinopse=r.get("overview", ""),
                data_estreia=r.get("first_air_date", ""), nota_media=r.get("vote_average", 0.0),
                poster_url=f"https://image.tmdb.org/t/p/w500{r.get('poster_path', '')}"
            )
        return None

    @staticmethod
    def buscar_gifs_reacao(termo: str) -> List[str]:
        from services.services import GiphyService
        return GiphyService.buscar_gifs(termo)

    @staticmethod
    def disparar_slap_ou_hug(item_id, usuario, nome_usuario, veredito, estrelas, emocao, comentario, gif):

        nova = SlapReview(
            id=str(uuid.uuid4())[:8],
            item_id=str(item_id),
            usuario=usuario,
            nome_usuario=nome_usuario,
            veredito=veredito,
            impacto_moral=estrelas,
            emocao=emocao,
            comentario_acido=comentario,
            gif_url=gif
        )

        ReviewRepository.salvar(nova)

    @staticmethod
    def listar_slaps(item_id: str) -> List[SlapReview]:
        reviews = ReviewRepository.listar_todas()

        return [
            r for r in reviews
            if r.item_id == str(item_id)
        ]

    @staticmethod
    def obter_timeline_de_impacto() -> List[SlapReview]:
        return ReviewRepository.listar_todas()

    @staticmethod
    def alternar_curtida_review(review_id: str, username: str):
        reviews = ReviewRepository.listar_todas()

        for r in reviews:
            if r.id == review_id:
                if username in r.curtidas: r.curtidas.remove(username)
                else: r.curtidas.append(username)
        ReviewRepository.atualizar(r)

    @staticmethod
    def adicionar_comentario_review(review_id: str, username: str, texto: str, veredito: str = "", media_url: str = ""):
        if not texto.strip() and not media_url: return
        reviews = ReviewRepository.listar_todas()
        for r in reviews:
            if r.id == review_id:
                r.respostas.append({
                    "usuario": username, "data": datetime.now().strftime("%d/%m %H:%M"),
                    "texto": f"[{veredito}] {texto.strip()}".strip() if veredito else texto.strip(),
                    "media": media_url if media_url else "NULO"
                })
        ReviewRepository.atualizar(r)

    @staticmethod
    def anular_veredito(review_id: str):
        ReviewRepository.excluir(review_id)