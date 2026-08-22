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
            name="📝 Provas, Notas & Boletim",
            value=(
                "`/boletim` — Exibe seu boletim completo de faltas e médias.\n"
                "`/lancar_nota` — (NOVO) Lança uma nota na sua grade (P1, P2, Projeto).\n"
                "`/lancar_falta` — (NOVO) Registra suas faltas para cálculo da FATEC.\n"
                "`/media_necessaria` — Calcula nota mínima para passar.\n"
                "`/frequencia_risco` — Matérias com risco de reprovação por falta.\n"
                "`/provas` — Cronograma global de provas e entregas.\n"
                "`/avaliacoes` — Cronograma de avaliações com pesos definidos."
            ),
            inline=False,
        )
        embed.add_field(
            name="🎓 Perfil & Secretaria",
            value=(
                "`/perfil_setup` — (NOVO) Cria seu perfil isolado para gerenciamento de notas.\n"
                "`/perfil_fatec` — Dados da secretaria e horas complementares."
            ),
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