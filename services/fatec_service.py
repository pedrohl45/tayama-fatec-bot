"""
services/fatec_service.py
Camada de serviço: toda lógica de negócio fica aqui.
Os cogs apenas formatam Embeds e chamam estas funções.
"""
from __future__ import annotations

from database.json_db import carregar_dados
from database.user_db import get_user_data

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

async def get_aulas_do_dia(dia: str) -> list[dict]:
    """
    Retorna lista de dicionários com informações das aulas para o dia informado.
    Cada item: {codigo, nome, inicio, fim, sala, professor}
    Esta função é genérica (serve para todos os alunos), pois a grade é a mesma.
    """
    dados = await carregar_dados()
    resultado: list[dict] = []

    for disc in dados.get("disciplinas", []):
        for horario in disc.get("horarios", []):
            if horario.get("dia_semana", "").lower() == dia.lower():
                profs = disc.get("professores", [])
                professor = profs[0].get("nome", "A definir") if profs else "A definir"
                resultado.append({
                    "codigo": disc.get("codigo", "?"),
                    "nome": disc.get("nome", "?"),
                    "inicio": horario.get("inicio", "?"),
                    "fim": horario.get("fim", "?"),
                    "sala": horario.get("sala", "?"),
                    "professor": professor,
                })

    # Ordena por horário de início
    resultado.sort(key=lambda a: a["inicio"])
    return resultado


async def get_todas_disciplinas() -> list[dict]:
    """Retorna a lista completa de disciplinas do dados.json."""
async def get_todas_disciplinas(discord_id: int) -> list[dict]:
    """
    Retorna a lista completa de disciplinas do dados.json, MAS injeta 
    o 'desempenho' pessoal do aluno puxado do arquivo dele.
    """
    dados = await carregar_dados()
    return dados.get("disciplinas", [])
    user_data = await get_user_data(discord_id)
    
    disciplinas_globais = dados.get("disciplinas", [])
    
    for disc in disciplinas_globais:
        codigo = disc.get("codigo")
        # Substitui o "desempenho" pelo do aluno (ou vazio se não tiver)
        desemp_aluno = user_data.get("desempenho_disciplinas", {}).get(codigo, {
            "notas": {"p1": None, "p2": None, "projeto": None},
            "faltas": 0,
            "frequencia_percentual": 100.0,
            "aulas_dadas": 0,
            "situacao": "Cursando"
        })
        disc["desempenho"] = desemp_aluno
        
    return disciplinas_globais


# ──────────────────────────────────────────────
# Frequência
# ──────────────────────────────────────────────

async def get_disciplinas_em_risco() -> list[dict]:
async def get_disciplinas_em_risco(discord_id: int) -> list[dict]:
    """
    Retorna disciplinas com frequência <= LIMITE_FREQUENCIA (75%).
    Cada item: {nome, codigo, frequencia, faltas, aulas_dadas, faltas_max_permitidas}
    """
    dados = await carregar_dados()
    disciplinas = await get_todas_disciplinas(discord_id)
    em_risco: list[dict] = []

    for disc in dados.get("disciplinas", []):
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
    """
    Calcula a nota mínima necessária nas avaliações restantes para aprovação.

    Fórmula FATEC DSM: média = P1*0.35 + P2*0.35 + Projeto*0.30 >= 5.0

    Args:
        notas: dict com chaves 'p1', 'p2', 'projeto' (float ou None)

    Returns:
        dict com:
          - media_parcial: soma ponderada das notas já lançadas
          - media_final: média final calculada (se todas as notas existem)
          - aprovado: bool (se todas as notas existem)
          - notas_faltantes: lista de avaliações ainda não lançadas
          - necessaria_por_avaliacao: nota necessária em cada avaliação faltante (se possível)
          - possivel: bool — ainda é matematicamente possível atingir 5.0
    """
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

    # Peso total das avaliações ainda não lançadas
    peso_faltante = sum(PESOS[k] for k in notas_faltantes)

    # Nota necessária nas avaliações restantes (assumindo mesma nota em todas)
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

