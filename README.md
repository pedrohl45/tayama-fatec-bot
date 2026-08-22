# 🚬 Tayama FATEC Bot

Bot de Discord desenvolvido em Python (`discord.py` 2.x) para automação e organização da rotina acadêmica do curso de **Desenvolvimento de Software Multiplataforma (FATEC São José dos Campos)**.

O bot conta com carregamento modular via Cogs, interface interativa (Slash Commands, Menus de Seleção e Modals), camada de serviços dedicada e rotinas automatizadas em segundo plano, além de comandos temáticos inspirados na personagem **Tayama** (*Smoking Behind the Supermarket with You*).

---

## ⚡ Funcionalidades

### 📚 Grade de Aulas & Disciplinas
- `/aulas_hoje [dia]`: Exibe a grade de horários, professores e salas do dia especificado.
- `/materias`: Visão geral de todas as matérias cadastradas no semestre.
- `/disciplina`: Menu de seleção (`Select Menu`) interativo que exibe ementa, horários, frequência e notas detalhadas de cada matéria.

### 📊 Desempenho, Notas & Frequência
- `/boletim`: Resumo de frequência percentual, total de faltas e situação de cada matéria.
- `/avaliacoes`: Cronograma detalhado de provas, projetos e pesos avaliativos.
- `/frequencia_risco`: Identifica matérias com frequência igual ou inferior a 75%, calculando o teto e as faltas excedentes.
- `/media_necessaria`: Menu interativo que calcula a nota mínima necessária para aprovação (critério FATEC DSM: $P_1 \times 0.35 + P_2 \times 0.35 + \text{Projeto} \times 0.30 \ge 5.0$).

### 🎓 Secretaria & Matrícula
- `/perfil_fatec`: Exibe status da matrícula, horas complementares cumpridas/exigidas e avisos acadêmicos.

### 🚀 Projeto Integrador (API / Scrum)
- `/api_sprints`: Acompanhamento de metas, datas de início/fim e status das sprints do projeto ágil.

### 📝 Prazos & Provas
- `/provas`: Listagem direta de entregas e datas limites cadastradas.

### 🧠 Gestão de Estudos & Produtividade
- `/registrar_estudo`: Abre um formulário interativo (`Modal`) para registro de tempo dedicado por matéria com anotações opcionais.
- `/estudo_resumo`: Relatório consolidado do tempo total acumulado em cada matéria (em horas/minutos).

### 🔔 Rotinas Automáticas
- **Lembrete Matinal de Aulas**: Envio automático da grade do dia de segunda a sexta às **07:00 (BRT)** no canal configurado (`CANAL_AVISOS_ID`).

### 🖤 Tayama Corner & Eventos
- `/pausa`: Citações e reflexões da personagem para pausas de estudo/trabalho.
- `/som`: Recomendações musicais (Post-punk, Darkwave, Deftones, Gothic Rock).
- `/dica_dev`: Dicas rápidas sobre Git, Python, terminal Linux e modelagem de software.
- `/eventos`: Calendário de palestras, workshops e semanas acadêmicas.
- `/ajuda`: Guia categorizado de todos os comandos do bot.

---

## 🛠️ Arquitetura & Tecnologias

- **Linguagem**: Python 3.10+
- **Framework Discord**: `discord.py` >= 2.3.2 (Slash Commands / `app_commands`, `ui.Select`, `ui.Modal`, `tasks.loop`)
- **Persistência de Dados**: JSON local não-bloqueante (`database/json_db.py`) utilizando `asyncio.Lock` para isolamento de escrita concorrente e `run_in_executor` para chamadas assíncronas.
- **Camada de Negócio**: `services/fatec_service.py` isolando lógica de cálculos, filtros de aulas e validações de frequência.
- **Fuso Horário**: `zoneinfo` com suporte via `tzdata` (compatível com Windows/Linux/macOS no fuso `America/Sao_Paulo`).

---

## 📁 Estrutura do Projeto

```text
tayama-fatec-bot/
├── cogs/
│   ├── __init__.py
│   ├── estudos.py        # Tracking e modals de estudo
│   ├── fatec_aluno.py    # Dados de secretaria e horas complementares
│   ├── fatec_api.py      # Sprints do Projeto Integrador
│   ├── fatec_aulas.py    # Horários, matérias e select menu de disciplinas
│   ├── fatec_eventos.py  # Eventos e palestras
│   ├── fatec_notas.py    # Boletim, médias e alerta de frequência
│   ├── fatec_provas.py   # Cronograma de provas e entregas
│   ├── general.py        # Central de ajuda (/ajuda)
│   ├── rotinas.py        # Task loop de lembrete matinal às 07:00
│   └── tayama.py         # Interações temáticas da Tayama
├── database/
│   ├── __init__.py
│   └── json_db.py        # I/O assíncrono e thread-safe do dados.json
├── services/
│   ├── __init__.py
│   └── fatec_service.py  # Regras de negócio e cálculos acadêmicos
├── .env.example
├── .gitignore
├── dados.json            # Fonte de dados acadêmicos local
├── main.py               # Inicialização, setup_hook e carregamento de cogs
└── requirements.txt
```

---

## 🚀 Instalação e Execução

### 1. Clonar o repositório
```bash
git clone https://github.com/seu-usuario/tayama-fatec-bot.git
cd tayama-fatec-bot
```

### 2. Criar e ativar o ambiente virtual

**No Windows (PowerShell):**
```powershell
python -m venv venv
.\venv\Scripts\Activate.ps1
```

**No Linux / macOS:**
```bash
python3 -m venv venv
source venv/bin/activate
```

### 3. Instalar as dependências
```bash
pip install -r requirements.txt
```

### 4. Configurar as variáveis de ambiente
Crie um arquivo `.env` na raiz do projeto a partir do `.env.example`:

```env
DISCORD_TOKEN=seu_token_aqui
GUILD_ID=seu_id_de_servidor_aqui
SYNC_COMMANDS=true
CANAL_AVISOS_ID=seu_id_de_canal_de_texto_aqui
```

| Variável | Descrição |
|---|---|
| `DISCORD_TOKEN` | Token do bot obtido no Discord Developer Portal. |
| `GUILD_ID` | ID numérico do servidor Discord (sem colchetes ou aspas). |
| `SYNC_COMMANDS` | `true` para sincronizar os Slash Commands na inicialização; `false` em produção normal. |
| `CANAL_AVISOS_ID` | *(Opcional)* ID do canal de texto para o envio das rotinas de aula matinais. |

### 5. Executar o bot
```bash
python main.py
```

> **Nota sobre sincronização de comandos:** Ao iniciar o bot pela primeira vez (ou ao cadastrar novos comandos), deixe `SYNC_COMMANDS=true`. Assim que as interações estiverem disponíveis no Discord, altere para `SYNC_COMMANDS=false` para evitar requisições desnecessárias à API do Discord a cada reinício.
