import os
import asyncio
import logging
import pymysql
import pymysql.cursors
from typing import Optional

logger = logging.getLogger("TayamaBot")

# ==============================================
# Pool de conexões MySQL (simples, thread-safe via executor)
# ==============================================

def _get_connection():
    """Cria uma conexão síncrona com o MySQL."""
    return pymysql.connect(
        host=os.getenv("MYSQL_HOST", "localhost"),
        port=int(os.getenv("MYSQL_PORT", "3306")),
        user=os.getenv("MYSQL_USER", "root"),
        password=os.getenv("MYSQL_PASSWORD", ""),
        database=os.getenv("MYSQL_DATABASE", "tayamabot"),
        charset="utf8mb4",
        cursorclass=pymysql.cursors.DictCursor,
        autocommit=True,
        connect_timeout=10,
    )


async def _execute(query: str, params: tuple = (), fetch: str = None):
    """Executa uma query no MySQL de forma assíncrona (via executor)."""
    loop = asyncio.get_event_loop()
    
    def _run():
        conn = _get_connection()
        try:
            with conn.cursor() as cursor:
                cursor.execute(query, params)
                if fetch == "one":
                    return cursor.fetchone()
                elif fetch == "all":
                    return cursor.fetchall()
                return cursor.lastrowid
        finally:
            conn.close()
    
    try:
        return await loop.run_in_executor(None, _run)
    except Exception as e:
        logger.error(f"MySQL query error: {e} | Query: {query[:80]}")
        raise


async def testar_conexao() -> bool:
    """Testa se a conexão com o MySQL está funcionando."""
    try:
        await _execute("SELECT 1", fetch="one")
        return True
    except Exception:
        return False


# ==============================================
# ALUNOS
# ==============================================

async def get_aluno(discord_id: str) -> Optional[dict]:
    """Busca um aluno pelo discord_id. Retorna None se não existir."""
    try:
        return await _execute(
            "SELECT * FROM alunos WHERE discord_id = %s",
            (discord_id,),
            fetch="one"
        )
    except Exception:
        return None


async def upsert_aluno(discord_id: str, dados: dict) -> bool:
    """Cria ou atualiza um aluno."""
    try:
        campos = ", ".join(f"`{k}` = %s" for k in dados)
        valores = list(dados.values()) + [discord_id]
        await _execute(
            f"""INSERT INTO alunos (discord_id, {', '.join(f'`{k}`' for k in dados)})
                VALUES (%s, {', '.join(['%s'] * len(dados))})
                ON DUPLICATE KEY UPDATE {campos}""",
            [discord_id] + list(dados.values()) + list(dados.values())
        )
        return True
    except Exception as e:
        logger.error(f"upsert_aluno erro: {e}")
        return False


async def listar_alunos(limit: int = 50) -> list:
    """Lista todos os alunos cadastrados."""
    try:
        return await _execute(
            "SELECT * FROM alunos ORDER BY criado_em DESC LIMIT %s",
            (limit,),
            fetch="all"
        ) or []
    except Exception:
        return []


async def deletar_aluno(discord_id: str) -> bool:
    """Remove um aluno do banco."""
    try:
        await _execute("DELETE FROM alunos WHERE discord_id = %s", (discord_id,))
        return True
    except Exception:
        return False


# ==============================================
# NOTAS E FALTAS
# ==============================================

async def get_notas(discord_id: str) -> list:
    """Busca todas as notas e faltas de um aluno."""
    try:
        return await _execute(
            "SELECT * FROM notas_faltas WHERE discord_id = %s",
            (discord_id,),
            fetch="all"
        ) or []
    except Exception:
        return []


async def get_nota_disciplina(discord_id: str, codigo: str) -> Optional[dict]:
    """Retorna notas e faltas de uma disciplina específica."""
    try:
        return await _execute(
            "SELECT * FROM notas_faltas WHERE discord_id = %s AND codigo_disciplina = %s",
            (discord_id, codigo),
            fetch="one"
        )
    except Exception:
        return None


async def upsert_nota(discord_id: str, codigo: str, campo: str, valor) -> bool:
    """Atualiza um campo (p1, p2, projeto, exame_final, faltas) de uma disciplina."""
    campos_validos = {"p1", "p2", "projeto", "exame_final", "faltas"}
    if campo not in campos_validos:
        return False
    try:
        await _execute(
            f"""INSERT INTO notas_faltas (discord_id, codigo_disciplina, `{campo}`)
                VALUES (%s, %s, %s)
                ON DUPLICATE KEY UPDATE `{campo}` = %s""",
            (discord_id, codigo, valor, valor)
        )
        return True
    except Exception as e:
        logger.error(f"upsert_nota erro: {e}")
        return False


# ==============================================
# SESSÕES DE ESTUDO
# ==============================================

async def registrar_sessao(discord_id: str, disciplina: str, minutos: int, anotacao: str = "") -> bool:
    """Registra uma sessão de estudo."""
    try:
        await _execute(
            "INSERT INTO sessoes_estudo (discord_id, disciplina, minutos, anotacao) VALUES (%s, %s, %s, %s)",
            (discord_id, disciplina, minutos, anotacao)
        )
        return True
    except Exception:
        return False


async def get_sessoes(discord_id: str) -> list:
    """Retorna todas as sessões de estudo de um aluno."""
    try:
        return await _execute(
            "SELECT * FROM sessoes_estudo WHERE discord_id = %s ORDER BY registrado_em DESC",
            (discord_id,),
            fetch="all"
        ) or []
    except Exception:
        return []
