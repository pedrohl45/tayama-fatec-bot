<div align="center">
  <img src="https://raw.githubusercontent.com/pedrohl45/tayama-fatec-bot/main/website/public/tayama.jpg" width="180" style="border-radius: 50%; box-shadow: 0 0 20px rgba(200, 34, 69, 0.8);" />
  
  # TayamaBot
  *A assistente noturna que organiza a sua faculdade, calcula seus riscos e gerencia a sua sanidade.*
  <br><br>

  [![Python](https://img.shields.io/badge/Python-3.10+-3776AB?style=for-the-badge&logo=python&logoColor=white)](https://python.org)
  [![Discord.py](https://img.shields.io/badge/Discord.py-2.x-5865F2?style=for-the-badge&logo=discord&logoColor=white)](https://discordpy.readthedocs.io/)
  [![Next.js](https://img.shields.io/badge/Next.js-14+-000000?style=for-the-badge&logo=next.js&logoColor=white)](https://nextjs.org/)
  [![Status](https://img.shields.io/badge/Status-Estável-C82245?style=for-the-badge)](#)
</div>

---

## 🖤 O que é a Tayama?

Acabou o caos acadêmico, as planilhas feias e o desespero de calcular frequência no final do semestre. A **TayamaBot** é um ecossistema completo (Bot de Discord + Web Landing Page) construído para gerenciar turmas, faltas, notas e projetos de forma **automatizada, isolada por usuário e altamente responsiva**.

Ela tem uma personalidade sarcástica, ácida e foi desenvolvida para ambientes de **Engenharia de Software (FATEC)**, mas serve perfeitamente para qualquer universitário que não aguenta mais perder prazos.

### 🔗 Acesse a Página Oficial (Web)
Nosso projeto possui um site super minimalista integrado com **Audio Player (Darkwave/Post-Punk)** e guias rápidos para iniciantes. A landing page foi feita em React/Next.js.

---

## ✨ O que há de novo? (Atualização 2.0)

A arquitetura passou por uma revolução gigante para suportar escala global sem perder a identidade e velocidade:

- **🔐 Banco de Dados Híbrido (Multi-usuário)**: Antes, todo mundo dividia o mesmo arquivo. Agora, através do `/perfil_setup`, a Tayama gera um contêiner virtual JSON isolado (`alunos_data.json`) para as notas e faltas **de cada estudante**. As aulas globais são lidas de um arquivo mestre.
- **⚡ Sistema de Cache em Memória**: O disco não sofre mais. A Tayama agora carrega os bancos na RAM e otimiza a latência das mensagens em *milisegundos*.
- **🎮 Tutorial Paginado In-App**: Criamos o comando `/tutorial`, uma View Interativa no Discord (com botões de página) que ensina os novos alunos como usarem a Tayama passo a passo.
- **🎵 Tayama FM (API Offline de Músicas)**: O comando `/som` foi reformulado com um banco interno contendo as melhores recomendações de *Darkwave*, *Sovietwave* e *Goth Rock*, injetando no chat botões perfeitamente linkados para o **Spotify, YouTube e SoundCloud**.
- **🧠 Autocomplete Dinâmico**: Ao usar `/lancar_nota` ou `/lancar_falta`, o Discord puxa em tempo real a grade oficial do semestre para sugerir o nome correto da disciplina.

---

## 🛠️ Funcionalidades Principais

### 🎓 Gestão Acadêmica Pessoal
- `/lancar_nota`: Adicione as notas das provas (P1, P2 e Projeto).
- `/lancar_falta`: Contabiliza uma nova falta e a Tayama recalcula se você corre risco.
- `/media_necessaria`: Com base nas notas já tiradas, a bot calcula exatamente os pontos que faltam para você fechar a matéria (Levando em conta os pesos da sua instituição).
- `/boletim`: Um relatório brutal e direto do seu desempenho.
- `/frequencia_risco`: Identifica imediatamente as matérias que você não pode mais faltar (Alerta Vermelho).

### 📚 Grade de Aulas Globais
- `/aulas_hoje`: Mostra a grade do dia (Horários, Sala, Professor).
- `/disciplina`: Um *Select Menu* estilizado que retorna horários, a ementa inteira e o professor titular de uma matéria.

### ⏳ Produtividade e Agilidade
- `/api_sprints`: Acompanhamento de metas e sprints para o Projeto Integrador (Scrum/Agile).
- `/registrar_estudo` & `/estudo_resumo`: Trackeamento de horas. Acompanhe quantas madrugadas você já gastou focando num projeto específico.

### 🖤 Tayama Corner
- `/pausa`: Quotes da Tayama para te lembrar que compilar café no cérebro 24 horas por dia não faz bem.
- `/som`: Sugestão imersiva e de alta curadoria de sons profundos pra recuperar o foco.
- `/dica_dev`: Alertas e lições amargas sobre engenharia de software (Git, Python, Clean Code).

---

## 🚀 Como instalar na sua máquina?

A Tayama é dividida em duas partes: O **Discord Bot** (Python) e o **Website** (Next.js).

### 1. Inicializando o Bot (Python)

Requisitos: Python 3.10+
```bash
# Clone o repositório
git clone https://github.com/seu-usuario/tayama-fatec-bot.git
cd tayama-fatec-bot

# Crie e ative um ambiente virtual
python -m venv venv
# Windows: .\venv\Scripts\Activate.ps1
# Linux/Mac: source venv/bin/activate

# Instale as dependências
pip install -r requirements.txt
```

Crie um arquivo `.env` na pasta raiz e insira seu token:
```env
DISCORD_TOKEN=seu_token_aqui
SYNC_COMMANDS=true
```

Inicie o bot:
```bash
python main.py
```
*(Após o primeiro início, mude SYNC_COMMANDS para false para não sofrer Rate Limit do Discord nas próximas inicializações).*

### 2. Inicializando o Website (Next.js)
```bash
cd website

# Instale as dependências
npm install

# Suba a aplicação local
npm run dev
```
Para o Audio Player funcionar no site, basta colocar o seu arquivo `darkwave.mp3` favorito na pasta `website/public/`.

---

## 🤝 Arquitetura & Stack

- **Linguagem**: Python 3.10+ / TypeScript
- **Framework Discord**: `discord.py` >= 2.3.2
- **Front-end**: React, Next.js 14, Tailwind CSS, Lucide Icons.
- **Banco de Dados**: JSON Isolado (Híbrido) protegido por assincronismo e cache.
- **UI UX**: Botões Interativos (`discord.ui.Button`), Menus e Autocompletes Nativos do Discord. 
- **Temática Visual**: Carmesim (`#C82245`), Amolado, Sombrio e Brutalista.

Feito para estudantes exaustos que merecem um sistema que funciona. 🖤
