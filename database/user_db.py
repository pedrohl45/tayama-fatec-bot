import json
import asyncio
from pathlib import Path

JSON_PATH = Path(__file__).parent.parent / "alunos_data.json"
_lock = asyncio.Lock()


def _ler_sync() -> dict:
    if not JSON_PATH.exists():
        return {}
    with JSON_PATH.open("r", encoding="utf-8") as f:
        return json.load(f)


def _salvar_sync(dados: dict) -> None:
    with JSON_PATH.open("w", encoding="utf-8") as f:
        json.dump(dados, f, indent=2, ensure_ascii=False)


async def carregar_usuarios() -> dict:
    """Carrega o arquivo alunos_data.json."""
    async with _lock:
        if not JSON_PATH.exists():
            await salvar_usuarios({})
            return {}
        loop = asyncio.get_event_loop()
        return await loop.run_in_executor(None, _ler_sync)


async def salvar_usuarios(dados: dict) -> None:
    """Salva o arquivo alunos_data.json."""
    async with _lock:
        loop = asyncio.get_event_loop()
        await loop.run_in_executor(None, _salvar_sync, dados)


async def get_user_data(discord_id: int) -> dict:
    """Retorna os dados específicos de um usuário."""
    usuarios = await carregar_usuarios()
    id_str = str(discord_id)
    
    if id_str not in usuarios:
        # Recuperação Mágica (Migration): Se existe a chave 'MIGRACAO' deixada pelo script
        # e é a primeira pessoa chamando, vamos assumir que é o dono original.
        if "MIGRACAO" in usuarios:
            usuarios[id_str] = usuarios.pop("MIGRACAO")
            await salvar_usuarios(usuarios)
        else:
            # Template vazio para um usuário novo
            usuarios[id_str] = {
                "estudos_foco": [],
                "desempenho_disciplinas": {}
            }
            await salvar_usuarios(usuarios)
            
    return usuarios[id_str]


async def update_user_data(discord_id: int, user_data: dict) -> None:
    """Atualiza e salva os dados específicos de um usuário."""
    usuarios = await carregar_usuarios()
    usuarios[str(discord_id)] = user_data
    await salvar_usuarios(usuarios)

