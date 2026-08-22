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
            title="📂 Central de Comandos — Bot FATEC DSM & Tayama",
            description="Comandos de barra (`/`) disponíveis para o seu dia a dia acadêmico e de desenvolvimento:",
            color=discord.Color.from_str("#ff73fa"),
        )

        embed.add_field(
            name="📚 Aulas & Disciplinas",
            value=(
                "`/materias` — Lista todas as matérias e horários.\n"
                "`/aulas_hoje` — Grade de aulas de um dia da semana.\n"
                "`/disciplina` — Detalhes completos de uma matéria (ementa, notas, frequência)."
            ),
            inline=False,
        )
        embed.add_field(
            name="📝 Provas & Avaliações",
            value=(
                "`/provas` — Cronograma de provas e entregas cadastradas.\n"
                "`/avaliacoes` — Cronograma de avaliações com pesos e datas.\n"
                "`/media_necessaria` — Calcula a nota mínima para aprovação em cada matéria.\n"
                "`/frequencia_risco` — Lista matérias com frequência abaixo de 75%."
            ),
            inline=False,
        )
        embed.add_field(
            name="🎓 Perfil & Secretaria",
            value="`/perfil_fatec` — Dados da secretaria, matrícula e horas complementares.",
            inline=False,
        )
        embed.add_field(
            name="🚀 Projeto Integrador (API)",
            value="`/api_sprints` — Semestre e metas das Sprints do Projeto Integrador.",
            inline=False,
        )
        embed.add_field(
            name="📅 Eventos",
            value="`/eventos` — Lista eventos acadêmicos, palestras e workshops.",
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
            name="🖤 Tayama Corner",
            value=(
                "`/pausa` — Mensagem descontraída e reflexão.\n"
                "`/som` — Recomendação de rock, post-punk e darkwave.\n"
                "`/dica_dev` — Dicas de programação, terminal e arquitetura."
            ),
            inline=False,
        )

        embed.set_footer(text="Tayama • FATEC DSM Bot — lembrete matinal ativo às 07:00 ☀️")
        await interaction.followup.send(embed=embed)


async def setup(bot: commands.Bot):
    await bot.add_cog(General(bot))