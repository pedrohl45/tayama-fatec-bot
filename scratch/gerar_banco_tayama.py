import json

# Carrega o arquivo atual para manter o 1º semestre (e links, etc)
with open('dados.json', 'r', encoding='utf-8') as f:
    dados = json.load(f)

# Mantém apenas as disciplinas do 1º semestre
disciplinas = [d for d in dados.get("disciplinas", []) if d.get("semestre") == 1]

novas_disciplinas = [
    # ==========================
    # 2º SEMESTRE
    # ==========================
    {
        "codigo": "IBD015", "nome": "Banco de Dados – Relacional", "carga_horaria": 80, "semestre": 2, "curso": "DSM",
        "professores": [{"nome": "JULIANA FORIN PASQUINI MARTINEZ"}],
        "horarios": [
            {"dia_semana": "Segunda-feira", "inicio": "07:10", "fim": "08:50", "sala": "A definir"},
            {"dia_semana": "Quinta-feira", "inicio": "10:55", "fim": "12:35", "sala": "A definir"}
        ]
    },
    {
        "codigo": "ISW029", "nome": "Desenvolvimento Web II", "carga_horaria": 80, "semestre": 2, "curso": "DSM",
        "professores": [{"nome": "CLAUDIO ETELVINO DE LIMA"}],
        "horarios": [
            {"dia_semana": "Terça-feira", "inicio": "07:10", "fim": "08:50", "sala": "A definir"},
            {"dia_semana": "Sexta-feira", "inicio": "09:15", "fim": "10:55", "sala": "A definir"}
        ]
    },
    {
        "codigo": "IMT001", "nome": "Matemática para Computação", "carga_horaria": 80, "semestre": 2, "curso": "DSM",
        "professores": [{"nome": "REINALDO GEN ICHIRO ARAKAKI"}],
        "horarios": [
            {"dia_semana": "Quarta-feira", "inicio": "07:10", "fim": "08:50", "sala": "A definir"},
            {"dia_semana": "Quinta-feira", "inicio": "09:15", "fim": "10:55", "sala": "A definir"}
        ]
    },
    {
        "codigo": "ILP001", "nome": "Técnica de Programação I", "carga_horaria": 80, "semestre": 2, "curso": "DSM",
        "professores": [{"nome": "GERSON DA PENHA NETO"}],
        "horarios": [
            {"dia_semana": "Quinta-feira", "inicio": "07:10", "fim": "08:50", "sala": "A definir"},
            {"dia_semana": "Quarta-feira", "inicio": "10:55", "fim": "12:35", "sala": "A definir"}
        ]
    },
    {
        "codigo": "IES012", "nome": "Engenharia de Software II", "carga_horaria": 80, "semestre": 2, "curso": "DSM",
        "professores": [{"nome": "JOSÉ WALMIR GONÇALVES DUQUE"}],
        "horarios": [
            {"dia_semana": "Segunda-feira", "inicio": "09:15", "fim": "10:55", "sala": "A definir"},
            {"dia_semana": "Terça-feira", "inicio": "09:15", "fim": "10:55", "sala": "A definir"}
        ]
    },
    {
        "codigo": "IED001", "nome": "Estruturas de Dados", "carga_horaria": 80, "semestre": 2, "curso": "DSM",
        "professores": [{"nome": "FERNANDO MASANORI ASHIKAGA"}],
        "horarios": [
            {"dia_semana": "Quarta-feira", "inicio": "09:15", "fim": "10:55", "sala": "A definir"},
            {"dia_semana": "Terça-feira", "inicio": "10:55", "fim": "12:35", "sala": "A definir"}
        ]
    },

    # ==========================
    # 3º SEMESTRE
    # ==========================
    {
        "codigo": "IMT002", "nome": "Álgebra Linear", "carga_horaria": 80, "semestre": 3, "curso": "DSM",
        "professores": [{"nome": "DANIELLE CRISTINA DE MORAIS AMORIM"}],
        "horarios": [
            {"dia_semana": "Terça-feira", "inicio": "07:10", "fim": "10:55", "sala": "A definir"}
        ]
    },
    {
        "codigo": "ISW030", "nome": "Desenvolvimento Web III", "carga_horaria": 80, "semestre": 3, "curso": "DSM",
        "professores": [{"nome": "GERSON DA PENHA NETO"}],
        "horarios": [
            {"dia_semana": "Quarta-feira", "inicio": "07:10", "fim": "08:50", "sala": "A definir"},
            {"dia_semana": "Quinta-feira", "inicio": "09:15", "fim": "10:55", "sala": "A definir"}
        ]
    },
    {
        "codigo": "IIG001", "nome": "Inglês I", "carga_horaria": 40, "semestre": 3, "curso": "DSM",
        "professores": [{"nome": "MARLUCE GAVIÃO SACRAMENTO DIAS"}],
        "horarios": [
            {"dia_semana": "Quinta-feira", "inicio": "07:10", "fim": "08:50", "sala": "A definir"}
        ]
    },
    {
        "codigo": "ILP002", "nome": "Técnica de Programação II", "carga_horaria": 80, "semestre": 3, "curso": "DSM",
        "professores": [{"nome": "GERSON DA PENHA NETO"}],
        "horarios": [
            {"dia_semana": "Sexta-feira", "inicio": "07:10", "fim": "08:50", "sala": "A definir"},
            {"dia_semana": "Quarta-feira", "inicio": "09:15", "fim": "10:55", "sala": "A definir"}
        ]
    },
    {
        "codigo": "IGP001", "nome": "Gestão Ágil de Projetos de Software", "carga_horaria": 80, "semestre": 3, "curso": "DSM",
        "professores": [{"nome": "EDUARDO SAKAUE"}],
        "horarios": [
            {"dia_semana": "Segunda-feira", "inicio": "09:15", "fim": "12:35", "sala": "A definir"}
        ]
    },
    {
        "codigo": "IHC001", "nome": "Interação Humano Computador", "carga_horaria": 40, "semestre": 3, "curso": "DSM",
        "professores": [{"nome": "GIULIANO ARAUJO BERTOTI"}],
        "horarios": [
            {"dia_semana": "Sexta-feira", "inicio": "09:15", "fim": "10:55", "sala": "A definir"}
        ]
    },
    {
        "codigo": "IBD016", "nome": "Banco de Dados - Não relacional", "carga_horaria": 80, "semestre": 3, "curso": "DSM",
        "professores": [{"nome": "DIOGO BRANQUINHO RAMOS"}],
        "horarios": [
            {"dia_semana": "Terça-feira", "inicio": "10:55", "fim": "12:35", "sala": "A definir"},
            {"dia_semana": "Quarta-feira", "inicio": "10:55", "fim": "12:35", "sala": "A definir"}
        ]
    },

    # ==========================
    # 4º SEMESTRE
    # ==========================
    {
        "codigo": "IES013", "nome": "Integração e Entrega Contínua", "carga_horaria": 80, "semestre": 4, "curso": "DSM",
        "professores": [{"nome": "EDUARDO SAKAUE"}],
        "horarios": [
            {"dia_semana": "Segunda-feira", "inicio": "07:10", "fim": "08:50", "sala": "A definir"},
            {"dia_semana": "Quarta-feira", "inicio": "07:10", "fim": "08:50", "sala": "A definir"}
        ]
    },
    {
        "codigo": "IHC002", "nome": "Experiência do Usuário", "carga_horaria": 40, "semestre": 4, "curso": "DSM",
        "professores": [{"nome": "A DEFINIR"}],
        "horarios": [
            {"dia_semana": "Terça-feira", "inicio": "07:10", "fim": "08:50", "sala": "A definir"}
        ]
    },
    {
        "codigo": "IMT003", "nome": "Estatística Aplicada", "carga_horaria": 80, "semestre": 4, "curso": "DSM",
        "professores": [{"nome": "NANCI DE OLIVEIRA"}],
        "horarios": [
            {"dia_semana": "Quinta-feira", "inicio": "07:10", "fim": "08:50", "sala": "A definir"},
            {"dia_semana": "Sexta-feira", "inicio": "07:10", "fim": "08:50", "sala": "A definir"}
        ]
    },
    {
        "codigo": "ILP003", "nome": "Programação para Dispositivos Móveis I", "carga_horaria": 80, "semestre": 4, "curso": "DSM",
        "professores": [{"nome": "GERSON DA PENHA NETO"}],
        "horarios": [
            {"dia_semana": "Segunda-feira", "inicio": "09:15", "fim": "12:35", "sala": "A definir"}
        ]
    },
    {
        "codigo": "IRC001", "nome": "Internet das Coisas e Aplicações", "carga_horaria": 80, "semestre": 4, "curso": "DSM",
        "professores": [{"nome": "DIOGO BRANQUINHO RAMOS"}],
        "horarios": [
            {"dia_semana": "Terça-feira", "inicio": "09:15", "fim": "10:55", "sala": "A definir"},
            {"dia_semana": "Quarta-feira", "inicio": "09:15", "fim": "10:55", "sala": "A definir"}
        ]
    },
    {
        "codigo": "ILP004", "nome": "Laboratório de Desenvolvimento Web", "carga_horaria": 80, "semestre": 4, "curso": "DSM",
        "professores": [{"nome": "CARLOS HENRIQUE LOUREIRO FEICHAS"}],
        "horarios": [
            {"dia_semana": "Quinta-feira", "inicio": "09:15", "fim": "10:55", "sala": "A definir"},
            {"dia_semana": "Sexta-feira", "inicio": "10:55", "fim": "12:35", "sala": "A definir"}
        ]
    },
    {
        "codigo": "IIG002", "nome": "Inglês II", "carga_horaria": 40, "semestre": 4, "curso": "DSM",
        "professores": [{"nome": "MARLUCE GAVIÃO SACRAMENTO DIAS"}],
        "horarios": [
            {"dia_semana": "Quinta-feira", "inicio": "10:55", "fim": "12:35", "sala": "A definir"}
        ]
    },

    # ==========================
    # 5º SEMESTRE
    # ==========================
    {
        "codigo": "IAM001", "nome": "Aprendizagem de Máquina", "carga_horaria": 80, "semestre": 5, "curso": "DSM",
        "professores": [{"nome": "EMANUEL MINEDA CARNEIRO"}],
        "horarios": [
            {"dia_semana": "Segunda-feira", "inicio": "07:10", "fim": "08:50", "sala": "A definir"},
            {"dia_semana": "Terça-feira", "inicio": "10:55", "fim": "12:35", "sala": "A definir"}
        ]
    },
    {
        "codigo": "ILP005", "nome": "Laboratório de Desenvolvimento para Dispositivos Móveis", "carga_horaria": 80, "semestre": 5, "curso": "DSM",
        "professores": [{"nome": "GERSON DA PENHA NETO"}],
        "horarios": [
            {"dia_semana": "Terça-feira", "inicio": "07:10", "fim": "10:55", "sala": "A definir"}
        ]
    },
    {
        "codigo": "ISE001", "nome": "Segurança no Desenvolvimento de Aplicações", "carga_horaria": 80, "semestre": 5, "curso": "DSM",
        "professores": [{"nome": "CARLOS HENRIQUE LOUREIRO FEICHAS"}],
        "horarios": [
            {"dia_semana": "Quarta-feira", "inicio": "07:10", "fim": "10:55", "sala": "A definir"}
        ]
    },
    {
        "codigo": "IRT001", "nome": "Fundamentos da Redação Técnica", "carga_horaria": 40, "semestre": 5, "curso": "DSM",
        "professores": [{"nome": "ELIANE PENHA MERGULHÃO DIAS"}],
        "horarios": [
            {"dia_semana": "Quinta-feira", "inicio": "07:10", "fim": "08:50", "sala": "A definir"}
        ]
    },
    {
        "codigo": "ILP006", "nome": "Programação para dispositivos móveis II", "carga_horaria": 80, "semestre": 5, "curso": "DSM",
        "professores": [{"nome": "CARLOS HENRIQUE LOUREIRO FEICHAS"}],
        "horarios": [
            {"dia_semana": "Sexta-feira", "inicio": "07:10", "fim": "10:55", "sala": "A definir"}
        ]
    },
    {
        "codigo": "ICN001", "nome": "Computacao em Nuvem I", "carga_horaria": 80, "semestre": 5, "curso": "DSM",
        "professores": [{"nome": "GILDARCIO SOUSA GONÇALVES"}],
        "horarios": [
            {"dia_semana": "Segunda-feira", "inicio": "09:15", "fim": "12:35", "sala": "A definir"}
        ]
    },
    {
        "codigo": "IIG003", "nome": "Inglês III", "carga_horaria": 40, "semestre": 5, "curso": "DSM",
        "professores": [{"nome": "ANDREA MARQUES DE CARVALHO"}],
        "horarios": [
            {"dia_semana": "Quinta-feira", "inicio": "10:55", "fim": "12:35", "sala": "A definir"}
        ]
    },

    # ==========================
    # 6º SEMESTRE (Noturno)
    # ==========================
    {
        "codigo": "IPL001", "nome": "Processamento de Linguagem Natural", "carga_horaria": 80, "semestre": 6, "curso": "DSM",
        "professores": [{"nome": "FABRICIO GALENDE MARQUES DE CARVALHO"}],
        "horarios": [
            {"dia_semana": "Segunda-feira", "inicio": "18:45", "fim": "22:15", "sala": "A definir"}
        ]
    },
    {
        "codigo": "IEP001", "nome": "Ética Profissional e Patente", "carga_horaria": 40, "semestre": 6, "curso": "DSM",
        "professores": [{"nome": "SAMUEL MARTIN MARESTI"}],
        "horarios": [
            {"dia_semana": "Terça-feira", "inicio": "18:45", "fim": "20:25", "sala": "A definir"}
        ]
    },
    {
        "codigo": "IMD001", "nome": "Mineração de Dados", "carga_horaria": 80, "semestre": 6, "curso": "DSM",
        "professores": [{"nome": "CARLOS HENRIQUE LOUREIRO FEICHAS"}],
        "horarios": [
            {"dia_semana": "Quinta-feira", "inicio": "18:45", "fim": "19:35", "sala": "A definir"},
            {"dia_semana": "Sexta-feira", "inicio": "20:25", "fim": "23:05", "sala": "A definir"}
        ]
    },
    {
        "codigo": "IIG004", "nome": "Inglês IV", "carga_horaria": 40, "semestre": 6, "curso": "DSM",
        "professores": [{"nome": "LISE VIRGINIA VIEIRA DE AZEVEDO"}],
        "horarios": [
            {"dia_semana": "Sexta-feira", "inicio": "18:45", "fim": "20:25", "sala": "A definir"}
        ]
    },
    {
        "codigo": "ILP007", "nome": "Laboratório de Desenvolvimento Multiplataforma", "carga_horaria": 80, "semestre": 6, "curso": "DSM",
        "professores": [{"nome": "LEONIDAS LOPES DE MELO"}],
        "horarios": [
            {"dia_semana": "Quarta-feira", "inicio": "19:35", "fim": "23:05", "sala": "A definir"}
        ]
    },
    {
        "codigo": "IQS001", "nome": "Qualidade e Testes de Software", "carga_horaria": 80, "semestre": 6, "curso": "DSM",
        "professores": [{"nome": "LUCAS GONÇALVES NADALETE"}],
        "horarios": [
            {"dia_semana": "Quinta-feira", "inicio": "19:35", "fim": "22:15", "sala": "A definir"},
            {"dia_semana": "Segunda-feira", "inicio": "22:15", "fim": "23:05", "sala": "A definir"}
        ]
    },
    {
        "codigo": "ICN002", "nome": "Computação em Nuvem II", "carga_horaria": 80, "semestre": 6, "curso": "DSM",
        "professores": [{"nome": "DAWILMAR GUIMARÃES DE ARAÚJO"}],
        "horarios": [
            {"dia_semana": "Terça-feira", "inicio": "20:25", "fim": "23:05", "sala": "A definir"},
            {"dia_semana": "Quinta-feira", "inicio": "22:15", "fim": "23:05", "sala": "A definir"}
        ]
    }
]

for mat in novas_disciplinas:
    mat["ementa"] = "Adicionada pela base global da FATEC SJC."
    mat["bibliografia"] = []
    disciplinas.append(mat)

dados["disciplinas"] = disciplinas

with open('dados.json', 'w', encoding='utf-8') as f:
    json.dump(dados, f, indent=2, ensure_ascii=False)
