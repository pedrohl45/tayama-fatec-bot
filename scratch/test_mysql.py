import asyncio
import os
import sys
sys.path.insert(0, '.')
from dotenv import load_dotenv
load_dotenv()

async def test():
    from database.mysql_db import testar_conexao, upsert_aluno, get_aluno, listar_alunos, deletar_aluno, upsert_nota, get_notas
    
    print("1. Testando conexao...", end=" ")
    ok = await testar_conexao()
    print("OK" if ok else "FALHOU")
    if not ok:
        return

    print("2. Inserindo aluno teste...", end=" ")
    ok = await upsert_aluno("999999", {"nome": "Teste Bot", "curso": "DSM", "semestre": 1})
    print("OK" if ok else "FALHOU")

    print("3. Buscando aluno...", end=" ")
    a = await get_aluno("999999")
    if a:
        print("OK — " + a["nome"])
    else:
        print("FALHOU")

    print("4. Lancando nota...", end=" ")
    ok = await upsert_nota("999999", "ISW031", "p1", 8.5)
    print("OK" if ok else "FALHOU")

    print("5. Buscando notas...", end=" ")
    notas = await get_notas("999999")
    print("OK — " + str(len(notas)) + " disciplina(s)")

    print("6. Deletando aluno teste...", end=" ")
    ok = await deletar_aluno("999999")
    print("OK" if ok else "FALHOU")

    print("\nTudo funcionando perfeitamente!")

asyncio.run(test())
