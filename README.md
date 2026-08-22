# 🚬 Tayama FATEC DSM Bot

> Bot de Discord modular em Python (`discord.py` 2.x) desenvolvido para centralizar rotinas acadêmicas do curso de **Desenvolvimento de Software Multiplataforma (FATEC São José dos Campos)**, tracking de estudos, Sprints do API (Aprendizagem por Projetos Integrados), eventos de tecnologia e interações temáticas da personagem **Tayama** (*Smoking Behind the Supermarket with You*).

---

## 🚀 Funcionalidades Principais

### 1. 📚 Gestão Acadêmica e Aulas
- `/materias`: Exibe todas as matérias cadastradas, docentes, salas e horários.
- `/aulas_hoje [dia]`: Mostra a grade do dia atual ou de um dia específico.
- `/disciplina [codigo]`: Detalha ementa e próximas avaliações da disciplina (ex: `ALP`, `ES1`, `MBD`, `DW1`, `DD`, `SO`).

### 2. 📝 Provas, Trabalhos e Prazos
- `/provas [status]`: Lista avaliações com status (Pendente, Concluído ou Todas), ordenadas pelas datas mais próximas.
- `/add_prova`: Cadastra provas (P1, P2), trabalhos, listas de exercícios ou seminários.
- `/concluir_prova [id]`: Marca uma avaliação ou trabalho como entregue.

### 3. 🚀 Metodologia API (Projetos Integradores FATEC)
- `/api_sprints [semestre]`: Acompanhamento do cronograma das Sprints do projeto ágil (Scrum).
- `/update_sprint [id] [status]`: Atualiza o status da Sprint (A Fazer, Em Andamento, Entregue).
- `/api_guia`: Guia de boas práticas ágeis, papéis da equipe (PO, SM, Dev Team) e estrutura de repositório.

### 4. 🎪 Eventos e Radar de Tecnologia
- `/eventos`: Lista eventos acadêmicos, semanas de tecnologia e conferências (como a Innovation Week no PIT).
- `/add_evento`: Cadastra novos workshops, hackathons ou palestras.

### 5. ⏱️ Produtividade e Estudos
- `/estudo_registrar`: Registra sessões de estudo com tempo e matéria.
- `/estudo_resumo`: Relatório analítico de horas estudadas por disciplina.
- `/pomodoro`: Temporizador Pomodoro interativo no canal com avisos sonoros/textuais de foco e pausa.

### 6. 🚬 Tayama Corner
- `/pausa`: Frases reflexivas e descontraídas para descansar a mente.
- `/som`: Recomendações de Rock, Post-Punk, Darkwave e Deftones para focar no código.
- `/dica_dev`: Dicas práticas de Git, Python, terminal Linux e arquitetura de software.

---

## 🛠️ Tecnologias Utilizadas

- **Linguagem**: Python 3.10+
- **Biblioteca Discord**: `discord.py` 2.3+ (usando `app_commands` para Slash Commands)
- **Banco de Dados**: SQLite3 assíncrono via `aiosqlite`
- **Configuração**: `python-dotenv`

---

## 📦 Como Instalar e Rodar Localmente

### 1. Clonar o repositório
```bash
git clone https://github.com/seu-usuario/tayama-fatec-bot.git
cd tayama-fatec-bot
```

### 2. Criar e ativar o ambiente virtual
```bash
# Linux / macOS
python3 -m venv venv
source venv/bin/activate

# Windows
python -m venv venv
venv\Scripts\activate
```

### 3. Instalar dependências
```bash
pip install -r requirements.txt
```

### 4. Configurar variáveis de ambiente
Crie um arquivo `.env` baseado no `.env.example`:
```env
DISCORD_TOKEN=seu_token_aqui
GUILD_ID=seu_id_de_servidor_de_testes_opcional
DB_PATH=fatec_bot.db
```

### 5. Executar o bot
```bash
python3 main.py
```

---

## 🗂️ Estrutura do Projeto

```text
tayama-fatec-bot/
├── .env.example
├── .gitignore
├── README.md
├── requirements.txt
├── main.py
├── database/
│   ├── __init__.py
│   └── db.py
└── cogs/
    ├── __init__.py
    ├── fatec_aulas.py
    ├── fatec_provas.py
    ├── fatec_api.py
    ├── fatec_eventos.py
    ├── estudos.py
    ├── tayama.py
    └── general.py
```

---

## 🌟 Active Developer Badge do Discord
Ao executar qualquer comando de barra (`/ping`, `/ajuda`, `/materias`, etc.), o bot registrará a interação nos servidores do Discord, habilitando a elegibilidade da insígnia de **Active Developer** no [Discord Developer Portal](https://discord.com/developers/active-developer).
