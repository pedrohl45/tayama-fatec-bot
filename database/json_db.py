import json
import asyncio
from pathlib import Path

# Caminho absoluto relativo a este arquivo — não depende do CWD
JSON_PATH = Path(__file__).parent.parent / "dados.json"

# Lock global: garante que leituras e escritas nunca ocorram simultaneamente
_lock = asyncio.Lock()
_cache = None


def _ler_sync() -> dict:
    """Leitura síncrona do JSON (executada em thread separada)."""
    with JSON_PATH.open("r", encoding="utf-8") as f:
        return json.load(f)


def _salvar_sync(dados: dict) -> None:
    """Escrita síncrona do JSON (executada em thread separada)."""
    with JSON_PATH.open("w", encoding="utf-8") as f:
        json.dump(dados, f, indent=2, ensure_ascii=False)


async def carregar_dados() -> dict:
    """
    Carrega o dados.json de forma assíncrona, sem bloquear o event loop.
    Usa asyncio.Lock para evitar leituras durante escritas.
    """
    global _cache
    if _cache is not None:
        return _cache
    async with _lock:
        if not JSON_PATH.exists():
            dados_iniciais = {
                "disciplinas": [],
                "provas": [],
                "sprints_api": [],
                "estudos_foco": [],
            }
            await salvar_dados(dados_iniciais)
            return dados_iniciais

        loop = asyncio.get_event_loop()
        _cache = await loop.run_in_executor(None, _ler_sync)
        return _cache


async def salvar_dados(dados: dict) -> None:
    """
    Salva o dados.json de forma assíncrona, sem bloquear o event loop.
    Usa asyncio.Lock para garantir escrita atômica (sem race condition).
    """
    global _cache
    async with _lock:
        loop = asyncio.get_event_loop()
        await loop.run_in_executor(None, _salvar_sync, dados)
        _cache = dados
