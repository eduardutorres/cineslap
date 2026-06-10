from dataclasses import dataclass, field
from datetime import datetime

@dataclass
class Usuario:
    username: str
    nome_completo: str
    cpf: str
    senha: str
    bio: str = "Sem bio ainda."
    foto_url: str = "https://cdn-icons-png.flaticon.com/512/149/149071.png"
    idade: str = ""
    ativo: bool = True

@dataclass
class Filme:
    id: str
    titulo: str
    sinopse: str
    data_lancamento: str
    nota_media: float
    poster_url: str

@dataclass
class Serie:
    id: str
    titulo: str
    sinopse: str
    data_estreia: str
    nota_media: float
    poster_url: str

@dataclass
class SlapReview:
    id: str
    item_id: str
    usuario: str
    nome_usuario: str
    veredito: str  
    impacto_moral: int 
    emocao: str        
    comentario_acido: str 
    gif_url: str
    curtidas: list = field(default_factory=list) 
    respostas: list = field(default_factory=list) 
    data_criacao: str = field(default_factory=lambda: datetime.now().strftime("%d/%m/%Y %H:%M"))