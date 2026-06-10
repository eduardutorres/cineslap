import streamlit as st
import time
from datetime import date
from controllers.controllers import CinemaController
from data.usario_repository import UsuarioRepository

st.set_page_config(page_title="CineSlap", page_icon="👋", layout="wide")
CinemaController.inicializar_estados()

# --- ARQUITETURA DE DESIGN APPLE (HUMAN INTERFACE GUIDELINES) ---
st.markdown("""
    <style>
        /* Base e Tipografia de Sistema Apple */
        .stApp { 
            background-color: #F5F5F7; 
            color: #1D1D1F; 
            font-family: -apple-system, BlinkMacSystemFont, "SF Pro Display", "SF Pro Text", "Helvetica Neue", Helvetica, Arial, sans-serif; 
            -webkit-font-smoothing: antialiased;
        }
        
        /* Hierarquia Tipográfica Avançada */
        h1, h2, h3, h4, h5, h6 { 
            color: #1D1D1F !important; 
            font-weight: 600; 
            letter-spacing: -0.022em; 
        }
        
        h1 { font-size: 2.2rem !important; margin-bottom: 1.5rem !important; }
        h4 { font-size: 1.25rem !important; }
        
        /* Sidebar Estilo macOS Navigation */
        section[data-testid="stSidebar"] { 
            background-color: #F5F5F7 !important; 
            border-right: 1px solid #D2D2D7; 
            padding-top: 2rem;
        }
        
        section[data-testid="stSidebar"] .stMarkdown, 
        section[data-testid="stSidebar"] span, 
        section[data-testid="stSidebar"] label,
        section[data-testid="stSidebar"] p { 
            color: #1D1D1F !important; 
        }
        
        /* Itens de Menu - Puramente Tipográficos, Padrão Apple */
        section[data-testid="stSidebar"] button {
            background-color: transparent !important;
            color: #1D1D1F !important;
            border: none !important;
            border-radius: 6px !important;
            text-align: left !important;
            padding: 0.6rem 1rem !important;
            font-size: 0.95rem !important;
            font-weight: 400 !important;
            transition: background-color 0.15s ease;
        }
        section[data-testid="stSidebar"] button:hover {
            background-color: #E8E8ED !important;
        }
        
        /* Botão de Sair Discreto */
        section[data-testid="stSidebar"] div[data-testid="stVerticalBlock"] > div:last-child button {
            color: #FF3B30 !important;
            font-weight: 500 !important;
            margin-top: 3rem;
        }
        
        /* Inputs e Content Controls */
        div[data-testid="stForm"] {
            background-color: #FFFFFF;
            padding: 24px;
            border-radius: 12px;
            border: 1px solid #D2D2D7;
            box-shadow: none;
        }
        
        /* Botões Primários Estilo Apple Control */
        .stButton > button[kind="primary"] {
            background-color: #0071E3 !important;
            color: #FFFFFF !important;
            border: none !important;
            border-radius: 8px !important;
            font-weight: 500 !important;
        }
        .stButton > button[kind="primary"]:hover {
            background-color: #0077ED !important;
        }
        
        /* Cards de Mídia Minimalistas */
        .slap-card { 
            background-color: #FFFFFF; 
            border: 1px solid #D2D2D7; 
            border-radius: 12px; 
            padding: 16px; 
            margin-bottom: 16px; 
            transition: border-color 0.2s ease;
        }
        .slap-card:hover { 
            border-color: #86868B;
        }
        
        /* Container de Críticas - Estilo Clean Content Box */
        .tweet-container { 
            background-color: #FFFFFF; 
            padding: 20px; 
            border-radius: 12px; 
            margin-bottom: 16px; 
            border: 1px solid #D2D2D7; 
        }
        
        .tweet-header { 
            font-size: 0.9rem; 
            margin-bottom: 12px; 
            display: flex; 
            align-items: center; 
        }
        .tweet-name { font-weight: 600; color: #1D1D1F; }
        .tweet-user { color: #86868B; margin-left: 6px; font-size: 0.85rem; }
        .tweet-time { color: #86868B; margin-left: auto; font-size: 0.8rem; }
        
        .avatar-img { width: 34px; height: 34px; border-radius: 50%; object-fit: cover; margin-right: 12px; border: 1px solid #D2D2D7; }
        .profile-header-img { width: 80px; height: 80px; border-radius: 50%; object-fit: cover; border: 1px solid #D2D2D7; }
        
        /* Badges de Estado Suaves */
        .badge-tweet { font-size: 0.75rem; font-weight: 500; padding: 4px 10px; border-radius: 6px; letter-spacing: -0.01em; }
        .bg-slap { background-color: #FFF2F2; color: #FF3B30; border: 1px solid rgba(255, 59, 48, 0.15); }
        .bg-hug { background-color: #F2F9F3; color: #34C759; border: 1px solid rgba(52, 199, 89, 0.15); }
        
        /* Threads Secundárias Encadeadas */
        .sub-thread { 
            background-color: #F5F5F7; 
            border-left: 3px solid #86868B; 
            padding: 12px 14px; 
            margin-top: 8px; 
            border-radius: 0 8px 8px 0; 
            font-size: 0.9rem; 
            color: #1D1D1F;
        }
        
        /* Cor de subtexto Apple */
        .apple-caption {
            font-size: 0.8rem;
            color: #86868B;
            font-weight: 400;
        }
    </style>
""", unsafe_allow_html=True)

def renderizar_bloco_tweet(s, user):
    badge_style = "bg-slap" if "SLAP" in s.veredito.upper() else "bg-hug"
    estrelas = "★" * s.impacto_moral + "☆" * (5 - s.impacto_moral)
    
    # --- MOTOR DE RESOLUÇÃO DE TÍTULO PARA A TIMELINE ---
    nome_da_obra = f"Produção {s.item_id}"
    if st.session_state.get("item_selecionado") and str(st.session_state["item_selecionado"].id) == str(s.item_id):
        nome_da_obra = st.session_state["item_selecionado"].titulo
    else:
        try:
            # Consulta direta à API do TMDB através do controlador para decodificar o ID em título real
            obra_info = CinemaController.buscar_filme_detalhes(s.item_id)
            if not obra_info:
                obra_info = CinemaController.buscar_serie_detalhes(s.item_id)
            
            if obra_info:
                nome_da_obra = obra_info.titulo
        except Exception:
            pass

    autor = UsuarioRepository.buscar_por_username(s.usuario)

    foto_autor = (
        autor.foto_url
        if autor
        else "https://cdn-icons-png.flaticon.com/512/149/149071.png"
    )

    st.markdown(f"""
        <div class='tweet-container'>
            <div style='display: flex; justify-content: space-between; align-items: center; margin-bottom: 12px;'>
                <span class='apple-caption' style='text-transform: uppercase; letter-spacing: 0.02em;'>
                    Foco / <span style='color: #1D1D1F; font-weight: 500;'>{nome_da_obra}</span>
                </span>
                <span class='badge-tweet {badge_style}'>{s.veredito}</span>
            </div>
            <div class='tweet-header'>
                <img src='{foto_autor}' class='avatar-img'/>
                <div>
                    <span class='tweet-name'>{s.nome_usuario}</span>
                    <span class='tweet-user'>@{s.usuario}</span>
                </div>
                <span class='tweet-time'>{s.data_criacao}</span>
            </div>
            <div style='margin: 6px 0 10px 0; font-size: 0.85rem;'>
                <span style='color: #FF9500;'>{estrelas}</span> 
                <span style='color: #86868B; margin-left: 12px;'>Estado: <strong>{s.emocao}</strong></span>
            </div>
            <p style='font-size: 0.95rem; line-height: 1.5; color: #1D1D1F; margin: 8px 0 12px 0;'>{s.comentario_acido}</p>
        </div>
    """, unsafe_allow_html=True)
    
    if s.gif_url:
        st.image(s.gif_url, width=240)
        st.markdown("<br>", unsafe_allow_html=True)
        
    c_like, c_comp, _ = st.columns([1, 1.5, 4])
    with c_like:
        liked = user.username in s.curtidas
        if st.button(f"Gostar ({len(s.curtidas)})", key=f"lk_{s.id}"):
            CinemaController.alternar_curtida_review(s.id, user.username)
            st.rerun()
            
    with c_comp:
        for resp in s.respostas:
            st.markdown(f"<div class='sub-thread'><strong>@{resp['usuario']}</strong> <span class='apple-caption'>· {resp['data']}</span><br>{resp['texto']}</div>", unsafe_allow_html=True)
            if resp.get('media') and resp['media'] != "NULO": 
                st.image(resp['media'], width=180)
            
        with st.popover(f"Comentários ({len(s.respostas)})"):
            v_coment = st.text_input("Veredito Curto", value="💬", key=f"v_c_{s.id}")
            txt_reply = st.text_input("Escreva a sua resposta", key=f"rep_in_{s.id}")
            
            t1, t2 = st.tabs(["Ficheiro Local", "Giphy"])
            url_anexo = ""
            with t1:
                up_file_c = st.file_uploader("Anexar imagem", type=["png", "jpg", "jpeg", "webp"], key=f"file_c_{s.id}", label_visibility="collapsed")
                if up_file_c:
                    url_anexo = CinemaController.converter_upload_para_base64(up_file_c)
            with t2:
                termo_c = st.text_input("Procurar GIF", value="meme", key=f"term_c_{s.id}", label_visibility="collapsed")
                gifs_c = CinemaController.buscar_gifs_reacao(termo_c)
                if gifs_c:
                    cols_gc = st.columns(3)
                    for cg_idx, c_url in enumerate(gifs_c[:3]):
                        with cols_gc[cg_idx % 3]: 
                            st.image(c_url, width="stretch")
                    op_esc = st.radio("Escolha:", ["Nenhum", "Opção #1", "Opção #2", "Opção #3"], key=f"rad_g_c_{s.id}", horizontal=True)
                    if op_esc != "Nenhum": 
                        url_anexo = gifs_c[int(op_esc.split("#")[1]) - 1]

            if st.button("Enviar", key=f"rep_btn_{s.id}", type="primary", use_container_width=True):
                CinemaController.adicionar_comentario_review(s.id, user.username, txt_reply, v_coment.strip(), url_anexo)
                st.rerun()

def render_login():
    st.markdown("<br><br>", unsafe_allow_html=True)
    _, cc, _ = st.columns([1.5, 1.8, 1.5])
    with cc:
        st.markdown("<h1 style='text-align: center; color: #1D1D1F;'>CineSlap</h1>", unsafe_allow_html=True)
        login_tab, signup_tab = st.tabs(["Login", "Criar Conta"])
        with login_tab:
            with st.form("form_login"):
                u_in = st.text_input("Usuário")
                p_in = st.text_input("Senha", type="password")
                if st.form_submit_button("Entrar", use_container_width=True):
                    if CinemaController.efetuar_login(u_in, p_in): 
                        CinemaController.navegar_para("Home")
                    else: 
                        st.error("Credenciais incorretas.")
        with signup_tab:
            with st.form("form_cadastro"):
                new_u = st.text_input("Usuário")
                new_n = st.text_input("Nome completo")
                new_c = st.text_input("CPF (apenas dígitos)", max_chars=11)
                new_p = st.text_input("Senha", type="password")
                if st.form_submit_button("Concluir Cadastro", use_container_width=True):
                    s, m = CinemaController.cadastrar_usuario(new_u, new_n, new_c, new_p)
                    if s: st.success(m)
                    else: st.error(m)

def render_home():
    st.title("Catálogo")
    col1, col2, _ = st.columns([0.8, 0.8, 5])
    with col1:
        if st.button("Filmes", use_container_width=True, type="primary" if st.session_state["tipo_conteudo"] == "Filmes" else "secondary"): 
            st.session_state["tipo_conteudo"] = "Filmes"
            st.rerun()
    with col2:
        if st.button("Séries", use_container_width=True, type="primary" if st.session_state["tipo_conteudo"] == "Séries" else "secondary"): 
            st.session_state["tipo_conteudo"] = "Séries"
            st.rerun()
            
    busca = st.text_input("Pesquisar...", placeholder="Pesquisar produções...", label_visibility="collapsed")
    itens = CinemaController.carregar_catalogo(busca, st.session_state["tipo_conteudo"])
    if itens:
        cols = st.columns(3)
        for idx, item in enumerate(itens):
            with cols[idx % 3]:
                st.markdown("<div class='slap-card'>", unsafe_allow_html=True)
                st.image(item.poster_url, width="stretch")
                st.markdown(f"<h4>{item.titulo}</h4>", unsafe_allow_html=True)
                if st.button("Avaliar", key=f"it_{item.id}", use_container_width=True): 
                    CinemaController.navegar_para("Detalhes", item=item)
                st.markdown("</div>", unsafe_allow_html=True)

def render_detalhes(user):
    item = st.session_state["item_selecionado"]
    if st.button("Voltar"): 
        CinemaController.navegar_para("Home")
    
    st.markdown("<br>", unsafe_allow_html=True)
    c_img, c_data = st.columns([1, 2.5])
    with c_img: 
        st.image(item.poster_url, width="stretch")
    with c_data:
        st.title(item.titulo)
        st.write(item.sinopse)
        
        st.markdown("<br><h5>Nova Crítica</h5>", unsafe_allow_html=True)

        col_v, col_e = st.columns(2)
        with col_v: 
            veredito = st.text_input("Veredito Curto (Ex: SLAP ou HUG):", value="SLAP")
        with col_e: 
            emocao = st.text_input("Estado de Espírito:", value="Chocado")

        estrelas = st.selectbox("Classificação:", ["★☆☆☆☆", "★★☆☆☆", "★★★☆☆", "★★★★☆", "★★★★★"])
        comentario = st.text_area("Texto da Crítica (Máximo de 280 caracteres):", max_chars=280)
        
        termo = st.text_input("Procurar GIF de reação:", value="slap" if "SLAP" in veredito.upper() else "happy")
        gifs = CinemaController.buscar_gifs_reacao(termo)
        if gifs:
            cg = st.columns(4)
            for gi, url in enumerate(gifs[:4]):
                with cg[gi % 4]: 
                    st.image(url, width="stretch")
            id_g = st.radio("Selecionar GIF:", options=list(range(len(gifs[:4]))), format_func=lambda x: f"GIF #{x+1}", horizontal=True)
            st.session_state["gif_selecionado"] = gifs[id_g]
            
        if st.button("Publicar Review", type="primary", use_container_width=True):
            if comentario.strip():
                # Passa o número de estrelas corretamente (como int) sem quebrar a assinatura modificada do controller
                CinemaController.disparar_slap_ou_hug(item.id, user.username, user.nome_completo, veredito, estrelas.count("★"), emocao, comentario, st.session_state["gif_selecionado"])
                time.sleep(0.2)
                st.session_state["gif_selecionado"] = ""
                st.rerun()

        st.markdown("<br><h5>Discussões Ativas</h5>", unsafe_allow_html=True)
        tweets = CinemaController.listar_slaps(item.id)
        if tweets:
            for t in tweets:
                renderizar_bloco_tweet(t, user)
                if user.username == t.usuario:
                    if st.button("Remover Crítica", key=f"del_{t.id}"): 
                        CinemaController.anular_veredito(t.id)
                        st.rerun()

def render_feed(user):
    st.title("Tendências")
    st.markdown("<br>", unsafe_allow_html=True)
    for r in CinemaController.obter_timeline_de_impacto():
        renderizar_bloco_tweet(r, user)
        if user.username == r.usuario:
            if st.button("Remover Crítica", key=f"mod_{r.id}"): 
                CinemaController.anular_veredito(r.id)
                st.rerun()

def render_perfil(user):
    st.title("Definições de Perfil")
    st.markdown("<br>", unsafe_allow_html=True)
    
    col_av, col_form = st.columns([1, 3])
    with col_av:
        st.markdown(f"<img src='{user.foto_url}' class='profile-header-img'/>", unsafe_allow_html=True)
        st.markdown(f"<p style='margin-top:12px; font-weight:600; margin-bottom: 2px;'>{user.nome_completo}</p>", unsafe_allow_html=True)
        st.markdown(f"<p class='apple-caption'>@{user.username}</p>", unsafe_allow_html=True)
        st.caption(f"Idade: {user.idade if user.idade else 'Não definida'}")
        st.write(f"*{user.bio}*")
        
    with col_form:
        with st.form("form_edicao_perfil"):
            name_f = st.text_input("Nome de exibição", value=user.nome_completo)
            data_nasc = st.date_input(
                "Data de nascimento", 
                value=date(2000, 1, 1),
                min_value=date(1920, 1, 1),
                max_value=date.today()
            )
            up_avatar = st.file_uploader("Alterar imagem de perfil", type=["png", "jpg", "jpeg", "webp"])
            bio_f = st.text_area("Biografia (Máximo de 160 caracteres)", value=user.bio, max_chars=160)
            
            if st.form_submit_button("Guardar Alterações", use_container_width=True):
                hoje = date.today()
                idade_calculada = hoje.year - data_nasc.year - ((hoje.month, hoje.day) < (data_nasc.month, data_nasc.day))
                idade_str = f"{idade_calculada} anos"
                
                base64_img = CinemaController.converter_upload_para_base64(up_avatar) if up_avatar else ""
                CinemaController.atualizar_perfil(user.username, name_f, bio_f, base64_img, idade_str)
                st.success("Perfil atualizado.")
                time.sleep(0.5)
                st.rerun()

# --- CONTROLADOR DE NAVEGAÇÃO / SIDEBAR (ESTILO APPLE) ---
if st.session_state["pagina_atual"] == "Login":
    render_login()
else:
    user_ativo = st.session_state["usuario_logado"]
    with st.sidebar:
        st.markdown(f"""
            <div style='display: flex; align-items: center; margin-bottom: 2.5rem; padding: 0 1rem;'>
                <img src='{user_ativo.foto_url}' style='width:34px; height:34px; border-radius:50%; object-fit:cover; margin-right:12px; border:1px solid #D2D2D7;'/>
                <div>
                    <strong style='font-size:0.9rem; color:#1D1D1F; font-weight:600;'>{user_ativo.nome_completo}</strong><br>
                    <span class='apple-caption'>@{user_ativo.username}</span>
                </div>
            </div>
        """, unsafe_allow_html=True)
        
        if st.button("Catálogo", use_container_width=True): CinemaController.navegar_para("Home")
        if st.button("Timeline", use_container_width=True): CinemaController.navegar_para("Feed")
        if st.button("Perfil", use_container_width=True): CinemaController.navegar_para("Perfil")
        if st.button("Sair da Conta", use_container_width=True):
            st.session_state["usuario_logado"] = None
            CinemaController.navegar_para("Login")

    p = st.session_state["pagina_atual"]
    if p == "Home": 
        render_home()
    elif p == "Detalhes": 
        render_detalhes(user_ativo)
    elif p == "Feed": 
        render_feed(user_ativo)
    elif p == "Perfil":
        render_perfil(user_ativo)