"""
services/fatec_service.py
Camada de serviço: toda lógica de negócio fica aqui.
Os cogs apenas formatam Embeds e chamam estas funções.
"""
from __future__ import annotations

from __future__ import annotations

from database.json_db import carregar_dados
from database.mysql_db import get_aluno, get_notas

# ──────────────────────────────────────────────
# Constantes
# ──────────────────────────────────────────────
LIMITE_FREQUENCIA = 75.0  # % mínima exigida pela FATEC para não reprovar por falta
MEDIA_APROVACAO = 5.0     # média mínima para aprovação

# Pesos de avaliação padrão FATEC DSM
PESOS = {"p1": 0.35, "p2": 0.35, "projeto": 0.30}


# ──────────────────────────────────────────────
# Aulas
# ──────────────────────────────────────────────

async def get_aulas_do_dia(dia: str, discord_id: int = None) -> list[dict]:
    """
    Retorna lista de dicionários com informações das aulas para o dia informado,
    filtradas pelo semestre/curso do aluno no MySQL.
    """
    dados = await carregar_dados()
    
    # Filtro por perfil do aluno
    semestre_aluno = 1
    curso_aluno = "Desenvolvimento de Software Multiplataforma (DSM)"
    
    aluno = {}
    if discord_id:
        aluno = await get_aluno(str(discord_id)) or {}
        
    semestre_aluno = aluno.get("semestre", 1)
    curso_aluno = aluno.get("curso", "DSM")
    # Tenta ler campos JSON do MySQL se existirem. Se for string vazia ou nula, usa lista vazia
    import json
    dps_str = aluno.get("dps", "[]")
    ocultas_str = aluno.get("ocultas", "[]")
    dps = json.loads(dps_str) if isinstance(dps_str, str) and dps_str.startswith("[") else []
    ocultas = json.loads(ocultas_str) if isinstance(ocultas_str, str) and ocultas_str.startswith("[") else []

    resultado: list[dict] = []

    for disc in dados.get("disciplinas", []):
        codigo = disc.get("codigo", "?")
        d_semestre = disc.get("semestre", 1)
        d_curso = disc.get("curso", "DSM")
        
        # Verifica se o curso bate (suporta "DSM" in "Desenvolvimento de... (DSM)")
        if d_curso not in curso_aluno and curso_aluno not in d_curso:
            continue
            
        # Pula se foi removida pelo aluno
        if codigo in ocultas:
            continue
            
        # Inclui se for do semestre atual OU se for uma DP adicionada
        is_grade_regular = str(d_semestre) == str(semestre_aluno)
        is_dp = codigo in dps
        
        if not (is_grade_regular or is_dp):
            continue

        for horario in disc.get("horarios", []):
            if horario.get("dia_semana", "").lower() == dia.lower():
                profs = disc.get("professores", [])
                professor = profs[0].get("nome", "A definir") if profs else "A definir"
                resultado.append({
                    "codigo": codigo,
                    "nome": disc.get("nome", "?"),
                    "inicio": horario.get("inicio", "?"),
                    "fim": horario.get("fim", "?"),
                    "sala": horario.get("sala", "?"),
                    "professor": professor,
                })

    resultado.sort(key=lambda a: a["inicio"])
    return resultado


async def get_todas_disciplinas(discord_id: int) -> list[dict]:
    """Retorna a lista completa de disciplinas do semestre do aluno com o desempenho do MySQL."""
    dados = await carregar_dados()
    
    aluno = await get_aluno(str(discord_id)) or {}
    semestre_aluno = aluno.get("semestre", 1)
    curso_aluno = aluno.get("curso", "DSM")
    
    import json
    dps_str = aluno.get("dps", "[]")
    ocultas_str = aluno.get("ocultas", "[]")
    dps = json.loads(dps_str) if isinstance(dps_str, str) and dps_str.startswith("[") else []
    ocultas = json.loads(ocultas_str) if isinstance(ocultas_str, str) and ocultas_str.startswith("[") else []

    # Busca notas do MySQL e transforma em dicionário indexado pelo código
    notas_lista = await get_notas(str(discord_id))
    notas_map = {n["codigo_disciplina"]: n for n in notas_lista}

    disciplinas = []
    
    for disc in dados.get("disciplinas", []):
        codigo = disc.get("codigo")
        d_semestre = disc.get("semestre", 1)
        d_curso = disc.get("curso", "DSM")
        
        if d_curso not in curso_aluno and curso_aluno not in d_curso:
            continue
            
        if codigo in ocultas:
            continue
            
        is_grade_regular = str(d_semestre) == str(semestre_aluno)
        is_dp = codigo in dps
        
        if not (is_grade_regular or is_dp):
            continue

        codigo = disc.get("codigo")
        desemp_mysql = notas_map.get(codigo, {})
        
        desemp_aluno = {
            "notas": {
                "p1": desemp_mysql.get("p1"),
                "p2": desemp_mysql.get("p2"),
                "projeto": desemp_mysql.get("projeto"),
                "exame_final": desemp_mysql.get("exame_final")
            },
            "faltas": desemp_mysql.get("faltas", 0),
            "situacao": "Cursando"
        }
        
        carga = disc.get("carga_horaria", 80)
        faltas = desemp_aluno["faltas"]
        frequencia = round(100.0 * (carga - faltas) / carga, 2) if carga > 0 else 100.0
        
        desemp_aluno["aulas_dadas"] = carga
        desemp_aluno["frequencia_percentual"] = frequencia
        
        disc["desempenho"] = desemp_aluno
        disciplinas.append(disc)
        
    return disciplinas


# ──────────────────────────────────────────────
# Frequência
# ──────────────────────────────────────────────

async def get_disciplinas_em_risco(discord_id: int) -> list[dict]:
    """
    Retorna disciplinas com frequência <= LIMITE_FREQUENCIA (75%).
    """
    disciplinas = await get_todas_disciplinas(discord_id)
    em_risco: list[dict] = []

    for disc in disciplinas:
        desemp = disc.get("desempenho", {})
        freq = desemp.get("frequencia_percentual", 100.0)

        if freq <= LIMITE_FREQUENCIA:
            aulas_dadas = desemp.get("aulas_dadas", 0)
            faltas = desemp.get("faltas", 0)
            # Máximo de faltas permitidas = 25% das aulas dadas
            faltas_max = int(aulas_dadas * 0.25)

            em_risco.append({
                "nome": disc.get("nome", "?"),
                "codigo": disc.get("codigo", "?"),
                "frequencia": freq,
                "faltas": faltas,
                "aulas_dadas": aulas_dadas,
                "faltas_max_permitidas": faltas_max,
                "faltas_acima_limite": faltas - faltas_max,
            })

    return em_risco


# ──────────────────────────────────────────────
# Notas e Média
# ──────────────────────────────────────────────

def calcular_media_necessaria(notas: dict) -> dict:
    media_parcial = 0.0
    peso_ja_computado = 0.0
    notas_faltantes: list[str] = []

    for chave, peso in PESOS.items():
        valor = notas.get(chave)
        if valor is not None:
            media_parcial += float(valor) * peso
            peso_ja_computado += peso
        else:
            notas_faltantes.append(chave)

    # Caso todas as notas já estejam lançadas
    if not notas_faltantes:
        aprovado = media_parcial >= MEDIA_APROVACAO
        return {
            "media_parcial": round(media_parcial, 2),
            "media_final": round(media_parcial, 2),
            "aprovado": aprovado,
            "notas_faltantes": [],
            "necessaria_por_avaliacao": None,
            "possivel": aprovado,
        }

    peso_faltante = sum(PESOS[k] for k in notas_faltantes)
    necessaria = (MEDIA_APROVACAO - media_parcial) / peso_faltante if peso_faltante > 0 else 0.0
    possivel = necessaria <= 10.0

    return {
        "media_parcial": round(media_parcial, 2),
        "media_final": None,
        "aprovado": None,
        "notas_faltantes": notas_faltantes,
        "necessaria_por_avaliacao": round(necessaria, 2) if possivel else None,
        "possivel": possivel,
    }
