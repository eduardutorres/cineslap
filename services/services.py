import requests
import os
from dotenv import load_dotenv
from typing import List, Dict

load_dotenv()

TMDB_BEARER_TOKEN = os.getenv("TMDB_BEARER_TOKEN")
GIPHY_API_KEY = os.getenv("GIPHY_API_KEY")

class CinemaService:
    @staticmethod
    def _obter_headers():
        return {
            "accept": "application/json",
            "Authorization": f"Bearer {TMDB_BEARER_TOKEN}"
        }

   
    @staticmethod
    def buscar_filmes(query_busca: str) -> List[Dict]:
        if not query_busca: return []
        url = f"https://api.themoviedb.org/3/search/movie?query={query_busca}&language=pt-BR&page=1&region=BR"
        try:
            res = requests.get(url, headers=CinemaService._obter_headers())
            return res.json().get("results", []) if res.status_code == 200 else []
        except Exception: 
            return []

    @staticmethod
    def buscar_em_cartaz() -> List[Dict]:
        url = "https://api.themoviedb.org/3/movie/now_playing?language=pt-BR&page=1&region=BR"
        try:
            res = requests.get(url, headers=CinemaService._obter_headers())
            return res.json().get("results", []) if res.status_code == 200 else []
        except Exception: 
            return []

    @staticmethod
    def obter_detalhes_filme(filme_id: str) -> Dict:
        url = f"https://api.themoviedb.org/3/movie/{filme_id}?language=pt-BR"
        try:
            res = requests.get(url, headers=CinemaService._obter_headers())
            return res.json() if res.status_code == 200 else {}
        except Exception:
            return {}

 
    @staticmethod
    def buscar_series(query_busca: str) -> List[Dict]:
        if not query_busca: return []
        url = f"https://api.themoviedb.org/3/search/tv?query={query_busca}&language=pt-BR&page=1"
        try:
            res = requests.get(url, headers=CinemaService._obter_headers())
            return res.json().get("results", []) if res.status_code == 200 else []
        except Exception: 
            return []

    @staticmethod
    def buscar_series_populares() -> List[Dict]:
        url = "https://api.themoviedb.org/3/tv/popular?language=pt-BR&page=1"
        try:
            res = requests.get(url, headers=CinemaService._obter_headers())
            return res.json().get("results", []) if res.status_code == 200 else []
        except Exception: 
            return []

    @staticmethod
    def obter_detalhes_serie(serie_id: str) -> Dict:
        url = f"https://api.themoviedb.org/3/tv/{serie_id}?language=pt-BR"
        try:
            res = requests.get(url, headers=CinemaService._obter_headers())
            return res.json() if res.status_code == 200 else {}
        except Exception:
            return {}


class GiphyService:
   
    @staticmethod
    def buscar_gifs(termo: str) -> List[str]:
        if not termo: 
            termo = "slap"
            
        url = f"https://api.giphy.com/v1/gifs/search?api_key={GIPHY_API_KEY}&q={termo}&limit=8&rating=g&lang=pt"
        try:
            res = requests.get(url)
            if res.status_code == 200:
                dados = res.json().get("data", [])
                links_limpos = [gif["images"]["fixed_height"]["url"] for gif in dados if "images" in gif]
                return links_limpos if links_limpos else GiphyService._obter_fallbacks(termo)
            else:
                return GiphyService._obter_fallbacks(termo)
        except Exception:
            return GiphyService._obter_fallbacks(termo)

    @staticmethod
    def _obter_fallbacks(termo: str) -> List[str]:
        if "slap" in termo.lower() or "tapa" in termo.lower():
            return [
                "https://media.giphy.com/media/v1.Y2lkPTc5MGI3NjExbXN6cmNndmpxbmt6bXN4cXFvZXB5b3RscXg1M3RndXNoNnd0Zmk3biZlcD12MV9pbnRlcm5hbF9naWZfYnlfaWQmY3Q9Zw/mEtUpzSbS9QQ0/giphy.gif",
                "https://media.giphy.com/media/v1.Y2lkPTc5MGI3NjExb3NndmZ3bmh5N3B0cnl0M3g4M2pxMGszbTV1M2J3N3lxdDcxbnljZiZlcD12MV9pbnRlcm5hbF9naWZfYnlfaWQmY3Q9Zw/IYXme8E06SskY/giphy.gif",
                "https://media.giphy.com/media/v1.Y2lkPTc5MGI3NjExbDRwM3BndjhhZXlsbTdkYTM5azFmYmd1aWFmZGl6ZXE4cmN0eWZndCZlcD12MV9pbnRlcm5hbF9naWZfYnlfaWQmY3Q9Zw/dBf0OpOH96MTBz6bS5/giphy.gif",
                "https://media.giphy.com/media/v1.Y2lkPTc5MGI3NjExNmt4MHBvN2p5dmxhZW44bzhvdmw3NXBxZXZnbWN5NjRhOXd4ZnIwaCZlcD12MV9pbnRlcm5hbF9naWZfYnlfaWQmY3Q9Zw/js58S8JmSOp6gIA9as/giphy.gif"
            ]
        return [
            "https://media.giphy.com/media/v1.Y2lkPTc5MGI3NjExbW1wM2dtbW84M3E4Z3A3b2VwM2Z4N3F5ZTZidXdzbmpyYXZjMCZlcD12MV9pbnRlcm5hbF9naWZfYnlfaWQmY3Q9Zw/G8xwi3ghEd02c/giphy.gif",
            "https://media.giphy.com/media/v1.Y2lkPTc5MGI3NjExM3M3M29idXBtczB6aHgzYzh4bTZ4Nmd3c3g5dHByczloOW8xYjQ2dyZlcD12MV9pbnRlcm5hbF9naWZfYnlfaWQmY3Q9Zw/91f7RYUc97veE/giphy.gif"
        ]