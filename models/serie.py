from dataclasses import dataclass

@dataclass
class Serie:
    id: str
    titulo: str
    sinopse: str
    data_estreia: str
    nota_media: float
    poster_url: str