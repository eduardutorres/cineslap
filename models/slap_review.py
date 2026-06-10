from dataclasses import dataclass, field
from datetime import datetime

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