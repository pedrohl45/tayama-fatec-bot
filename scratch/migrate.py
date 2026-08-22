import json
from pathlib import Path
import os

ROOT = Path(__file__).parent.parent
DADOS_JSON = ROOT / "dados.json"
ALUNOS_JSON = ROOT / "alunos_data.json"

def migrar():
    if not DADOS_JSON.exists():
        print("dados.json não existe.")
        return

    with open(DADOS_JSON, "r", encoding="utf-8") as f:
        dados = json.load(f)

    # 1. Puxar os dados pessoais dele
    perfil_migracao = {
        "aluno": dados.get("aluno", {}),
        "secretaria": dados.get("secretaria", {}),
        "horas_complementares": dados.get("horas_complementares", {}),
        "estudos_foco": dados.get("estudos_foco", []),
        "desempenho_disciplinas": {}
    }

    # 2. Puxar desempenho das disciplinas dele
    for disc in dados.get("disciplinas", []):
        codigo = disc.get("codigo")
        if codigo and "desempenho" in disc:
            perfil_migracao["desempenho_disciplinas"][codigo] = disc["desempenho"]

    # 3. Criar alunos_data.json com a chave MIGRACAO
    if ALUNOS_JSON.exists():
        with open(ALUNOS_JSON, "r", encoding="utf-8") as f:
            alunos = json.load(f)
    else:
        alunos = {}
        
    alunos["MIGRACAO"] = perfil_migracao

    with open(ALUNOS_JSON, "w", encoding="utf-8") as f:
        json.dump(alunos, f, indent=2, ensure_ascii=False)
        
    print("Migração bem sucedida. Os desempenhos e horas foram movidos para alunos_data.json (sob a chave MIGRACAO).")

if __name__ == "__main__":
    migrar()

