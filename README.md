<div align="center">
  <img src="https://raw.githubusercontent.com/pedrohl45/tayama-fatec-bot/main/website/public/tayama.jpg" width="180" style="border-radius: 50%; box-shadow: 0 0 20px rgba(200, 34, 69, 0.8);" />
  
  # TayamaBot
  *A assistente noturna que organiza a sua faculdade, calcula seus riscos e gerencia a sua sanidade.*
  <br><br>

  [![Python](https://img.shields.io/badge/Python-3.10+-3776AB?style=for-the-badge&logo=python&logoColor=white)](https://python.org)
  [![Discord.py](https://img.shields.io/badge/Discord.py-2.x-5865F2?style=for-the-badge&logo=discord&logoColor=white)](https://discordpy.readthedocs.io/)
  [![MySQL](https://img.shields.io/badge/MySQL-8.0+-4479A1?style=for-the-badge&logo=mysql&logoColor=white)](https://www.mysql.com/)
  [![Next.js](https://img.shields.io/badge/Next.js-14+-000000?style=for-the-badge&logo=next.js&logoColor=white)](https://nextjs.org/)
  [![Status](https://img.shields.io/badge/Status-Estável-C82245?style=for-the-badge)](#)
</div>

---

## 🖤 O que é a Tayama?

Acabou o caos acadêmico, as planilhas feias e o desespero de calcular frequência no final do semestre. A **TayamaBot** é um ecossistema completo (Bot de Discord + Web Landing Page) construído para gerenciar turmas, faltas, notas e projetos de forma **automatizada, isolada por usuário e altamente responsiva**.

Ela tem uma personalidade sarcástica, ácida e foi desenvolvida para ambientes de **Engenharia de Software (FATEC)**, mas serve perfeitamente para qualquer universitário que não aguenta mais perder prazos.

### 🔗 Acesse a Página Oficial (Web)
Nosso projeto possui um site super minimalista integrado com **Audio Player Contínuo (Darkwave/Post-Punk)** e guias rápidos para iniciantes. A landing page foi feita em React/Next.js e a música não para de tocar mesmo quando você navega entre as páginas!

---

## ✨ O que há de novo? (Atualização 3.0)

A arquitetura passou por uma revolução gigante para suportar escala global, múltiplos cursos e regras acadêmicas avançadas:

- **🔐 Migração Completa para MySQL**: Abandonamos os arquivos de texto para perfis. Toda a gestão de alunos, notas, faltas e sessões de estudo agora ocorre em tabelas relacionais de alta performance no **MySQL**. Seus dados estão seguros, blindados e processados em milissegundos.
- **🧬 Gestão Inteligente de Grade e Semestres**: A Tayama agora sabe em qual semestre e curso você está. Quando você pede a grade do dia, ela filtra a base de dados global e exibe **apenas os professores, salas e horários da sua turma específica**.
- **🔄 Sistema Avançado de Dependências (DPs) e Dispensas**: Pegou DP? Dispensou matéria? Sem problemas. Introduzimos os novos comandos `/adicionar_dp` e `/remover_materia`. A Tayama manipula dados estruturados em JSON direto nas colunas do MySQL para injetar disciplinas extras no seu boletim ou esconder as que você não cursa.
- **🛠️ Painel de Administração Seguro**: Exclusivo para o desenvolvedor. Comandos como `/admin_alunos` invocam painéis (Select Menus) para editar, banir ou checar logs de usuários diretamente pelo Discord.
- **🎵 Tayama FM (API Offline de Músicas)**: O comando `/som` foi reformulado com um banco interno contendo as melhores recomendações de *Darkwave* e *Goth Rock*, injetando no chat botões perfeitamente linkados para **Spotify, YouTube e Apple Music**.

---

## 🛠️ Funcionalidades Principais

### 🎓 Secretaria & Perfil (Integração MySQL)
- `/meu_perfil`: Uma interface limpa que mostra seu semestre, curso, matrícula e horas complementares, equipado com um Modal de edição instantânea.
- `/perfil_setup`: O passo inicial. Cadastre-se na base de dados e defina sua grade.

### 📚 Aulas & Disciplinas (Filtragem Dinâmica)
- `/materias`: Lista a ementa, horário e professor de todas as disciplinas da **sua** grade.
- `/aulas_hoje`: Mostra a grade do dia (Horários, Sala, Professor).
- `/disciplina`: Um *Select Menu* estilizado que retorna o raio-X completo da matéria.
- `/adicionar_dp`: Puxe uma matéria de outro semestre (ou curso) para a sua grade pessoal.
- `/remover_materia`: Esconda matérias da qual você foi dispensado.

### 🩸 Provas, Notas & Faltas
- `/lancar_nota`: Grave suas pontuações de P1, P2 ou Projeto no banco.
- `/lancar_falta`: Contabilize faltas. A Tayama recalcula se você corre risco na hora.
- `/media_necessaria`: Com base nas notas tiradas, a bot calcula matematicamente os pontos exatos que faltam para você ser aprovado.
- `/frequencia_risco`: Identifica imediatamente as matérias que você não pode mais faltar (Alerta Vermelho).
- `/boletim`: Um relatório brutal e direto do seu desempenho.

### ⏳ Produtividade & Agilidade
- `/api_sprints`: Acompanhamento de metas para o Projeto Integrador (Scrum/Agile).
- `/registrar_estudo` & `/estudo_resumo`: Trackeamento de horas. Acompanhe quantas madrugadas você já gastou focando num projeto específico.

### 🖤 Tayama Corner
- `/pausa`: Quotes da Tayama para te lembrar que compilar café no cérebro 24h não faz bem.
- `/som`: Sugestão imersiva e de alta curadoria de sons profundos pra recuperar o foco.
- `/dica_dev`: Alertas e lições amargas sobre engenharia de software e mercado de trabalho.

---

## ⚙️ Arquitetura & Stack Tecnológica

O projeto foi modernizado para separar responsabilidades (Lógica de Negócios vs. Interface de Usuário), garantindo um código limpo (Clean Architecture).

### Backend (Bot)
- **Linguagem**: Python 3.10+
- **Framework Discord**: `discord.py` >= 2.3.2 (Uso extensivo de Slash Commands, Modals, Views e Autocompletes)
- **Banco de Dados Principal**: MySQL (Tabelas relacionais: `alunos`, `notas_faltas`, `sessoes_estudo`). Utiliza colunas `JSON` dinâmicas para gerenciar DPs flexivelmente.
- **Banco de Dados Global (Grade)**: Arquivo JSON sincronizado via `asyncio.Lock` para leituras super rápidas das informações estáticas da instituição.
- **Lib DB**: `pymysql` integrado a um executor assíncrono do `asyncio` (`run_in_executor`) para não bloquear o Event Loop durante operações pesadas de banco de dados.

### Frontend (Dashboard Website)
- **Framework Web**: Next.js 14 (React) e TypeScript.
- **Estilização**: Tailwind CSS, UI brutalista, paleta em tons carmesim (`#C82245`) e preto.
- **Ícones**: Lucide Icons.
- **Componentes**: Global Continuous Audio Player em Client Components injetados via Root Layout.

---

## 🚀 Como instalar na sua máquina?

### 1. Preparando o Banco de Dados (MySQL)
Crie um banco de dados vazio no seu MySQL e execute o script SQL que preparamos:
```bash
mysql -u root -p < database/setup.sql
```

### 2. Inicializando o Bot (Python)

Requisitos: Python 3.10+
```bash
# Clone o repositório
git clone https://github.com/pedrohl45/tayama-fatec-bot.git
cd tayama-fatec-bot

# Crie e ative um ambiente virtual
python -m venv venv
# Windows: .\venv\Scripts\Activate.ps1
# Linux/Mac: source venv/bin/activate

# Instale as dependências
pip install -r requirements.txt
```

Crie um arquivo `.env` na pasta raiz:
```env
DISCORD_TOKEN=seu_token_aqui
ADMIN_DISCORD_ID=seu_id_do_discord_aqui
SYNC_COMMANDS=true

MYSQL_HOST=localhost
MYSQL_PORT=3306
MYSQL_USER=root
MYSQL_PASSWORD=sua_senha
MYSQL_DATABASE=tayama_bot
```

Inicie o bot:
```bash
python main.py
```
*(Após o primeiro início, mude SYNC_COMMANDS para false para não sofrer Rate Limit do Discord).*

### 3. Inicializando o Website (Next.js)
```bash
cd website

# Instale as dependências
npm install

# Suba a aplicação local
npm run dev
```

---

Feito para estudantes exaustos que merecem um sistema que funciona. 🖤
