from dataclasses import dataclass

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