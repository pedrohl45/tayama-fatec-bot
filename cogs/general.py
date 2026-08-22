import discord
from discord.ext import commands
from discord import app_commands


class General(commands.Cog):
    def __init__(self, bot: commands.Bot):
        self.bot = bot

    @app_commands.command(
        name="ajuda",
        description="Central de Comandos — Bot FATEC DSM & Tayama",
    )
    async def ajuda(self, interaction: discord.Interaction):
        await interaction.response.defer(thinking=True)

        embed = discord.Embed(
            title="📂 Central de Comandos da Tayama",
            description="Comandos de barra (`/`) disponíveis para o seu dia a dia acadêmico e de desenvolvimento:",
            color=discord.Color.from_str("#c82245"),
        )

        embed.add_field(
            name="📖 O Guia Definitivo",
            value="`/tutorial` — Abre o Guia de Sobrevivência paginado (Como começar, setup de perfil, notas).",
            inline=False,
        )

        embed.add_field(
            name="🖤 Aulas & Disciplinas",
            value=(
                "`/materias` — Lista todas as matérias globais e horários.\n"
                "`/aulas_hoje` — Grade de aulas de um dia da semana.\n"
                "`/disciplina` — Detalhes completos de uma matéria.\n"
                "`/adicionar_dp` — Puxa uma matéria de outro semestre pra sua grade.\n"
                "`/remover_materia` — Esconde uma matéria que você não cursa (dispensa)."
            ),
            inline=False,
        )
        embed.add_field(
            name="🩸 Provas, Notas & Boletim",
            value=(
                "`/perfil_setup` — Cria seu perfil para poder gerenciar as PRÓPRIAS notas e faltas.\n"
                "`/lancar_nota` — Lança uma nota na sua grade (P1, P2, Projeto).\n"
                "`/lancar_falta` — Registra suas faltas para cálculo automático da FATEC.\n"
                "`/boletim` — Exibe seu boletim completo de faltas e médias.\n"
                "`/media_necessaria` — Calcula nota mínima para passar nas próximas provas.\n"
                "`/frequencia_risco` — Matérias com risco iminente de reprovação por falta.\n"
                "`/provas` — Cronograma global de provas e entregas.\n"
                "`/avaliacoes` — Cronograma de avaliações com pesos definidos."
            ),
            inline=False,
        )
        embed.add_field(
            name="🎓 Secretaria & Perfil",
            value=(
                "`/meu_perfil` — Vê os seus dados acadêmicos com botão de Editar Perfil.\n"
                "`/perfil_fatec` — Dados resumidos da secretaria e progresso."
            ),
            inline=False,
        )
        embed.add_field(
            name="🚀 Projeto Integrador (API)",
            value="`/api_sprints` — Semestre e metas das Sprints do Projeto Integrador.",
            inline=False,
        )
        embed.add_field(
            name="🛠️ Administração (Apenas Dono)",
            value=(
                "`/admin_alunos` — Painel para gerenciar alunos cadastrados no MySQL.\n"
                "`/admin_checar` — Verifica rapidamente o cadastro de um usuário."
            ),
            inline=False,
        )
        embed.add_field(
            name="🧠 Foco & Estudos",
            value=(
                "`/estudo_resumo` — Relatório de horas dedicadas por matéria.\n"
                "`/registrar_estudo` — Registra uma sessão de estudo via formulário."
            ),
            inline=False,
        )
        embed.add_field(
            name="🚬 Área de Fumantes (Tayama)",
            value=(
                "`/pausa` — Mensagem ácida de reflexão para pausas.\n"
                "`/som` — Recomendação de post-punk e darkwave com botões.\n"
                "`/dica_dev` — Dicas amargas sobre programação e mercado."
            ),
            inline=False,
        )

        embed.set_footer(text="TayamaBot • Seu site dashboard está na Vercel.")
        await interaction.followup.send(embed=embed)


async def setup(bot: commands.Bot):
    await bot.add_cog(General(bot))