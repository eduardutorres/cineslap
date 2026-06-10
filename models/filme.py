from dataclasses import dataclass

@dataclass
class Filme:
    id: str
    titulo: str
    sinopse: str
    data_lancamento: str
    nota_media: float
    poster_url: str