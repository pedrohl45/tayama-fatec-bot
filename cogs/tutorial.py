import discord
from discord import app_commands
from discord.ext import commands

class TutorialView(discord.ui.View):
    def __init__(self):
        super().__init__(timeout=180)
        self.current_page = 0
        self.pages = [
            self.build_page_setup,
            self.build_page_academico,
            self.build_page_produtividade,
            self.build_page_som
        ]

    def build_page_setup(self) -> discord.Embed:
        embed = discord.Embed(
            title="📖 Tutorial da Tayama (1/4) - Setup Inicial",
            description="Bem-vindo. A primeira coisa que você precisa fazer para que eu possa gerenciar a sua sanidade é configurar o seu perfil.",
            color=discord.Color.from_str("#c82245")
        )
        embed.add_field(
            name="1. Crie seu perfil",
            value="Digite `/perfil_setup nome:Seu Nome curso:Seu Curso`. Isso criará um banco de dados isolado só seu.",
            inline=False
        )
        embed.add_field(
            name="2. E a FATEC?",
            value="Você pode puxar os dados oficiais da grade e secretaria usando `/perfil_fatec` e `/materias`. Seus dados não se misturam com a turma.",
            inline=False
        )
        embed.set_footer(text="Clique em 'Próximo' para ver como lançar faltas e notas.")
        return embed

    def build_page_academico(self) -> discord.Embed:
        embed = discord.Embed(
            title="📖 Tutorial da Tayama (2/4) - Vida Acadêmica",
            description="Não seja reprovado por falta. Use meus comandos para não se perder nas contas matemáticas.",
            color=discord.Color.from_str("#c82245")
        )
        embed.add_field(
            name="📉 Faltas (O limite do desespero)",
            value="Voltou para casa mais cedo? Use `/lancar_falta`. Eu vou recalcular automaticamente sua frequência. Para ver se você está no limite de reprovação, chame o `/frequencia_risco`.",
            inline=False
        )
        embed.add_field(
            name="📝 Notas (O milagre da aprovação)",
            value="Tirou nota na P1? Use `/lancar_nota`. Quer saber quanto precisa tirar na P2 e na API (Projeto) para passar? Use `/media_necessaria`.",
            inline=False
        )
        embed.add_field(
            name="📋 Boletim Geral",
            value="Para ver o resumo de toda sua tragédia acadêmica, simplesmente chame o `/boletim`.",
            inline=False
        )
        return embed
        
    def build_page_produtividade(self) -> discord.Embed:
        embed = discord.Embed(
            title="📖 Tutorial da Tayama (3/4) - Produtividade & APIs",
            description="Além de contar suas faltas, eu te ajudo a se organizar para entregar as Sprints do Projeto Integrador.",
            color=discord.Color.from_str("#c82245")
        )
        embed.add_field(
            name="🚀 Cronogramas Globais",
            value="Temos o `/provas` e o `/avaliacoes` para o calendário de testes, além de `/api_sprints` para checar as datas e metas do Projeto Integrador (API).",
            inline=False
        )
        embed.add_field(
            name="⏳ Registro de Estudo",
            value="Ficou até às 3h da manhã codando? Use `/registrar_estudo` para me contar quantas horas gastou. Use `/estudo_resumo` para ver o gráfico de horas dedicadas.",
            inline=False
        )
        return embed

    def build_page_som(self) -> discord.Embed:
        embed = discord.Embed(
            title="📖 Tutorial da Tayama (4/4) - Área de Fumantes",
            description="Chega de trabalho. Até código precisa compilar de vez em quando.",
            color=discord.Color.from_str("#c82245")
        )
        embed.add_field(
            name="🚬 Tayama Corner",
            value="Se a sanidade baixar, chame o `/pausa` para reflexões duvidosas ou o `/dica_dev` para tentar melhorar suas práticas.",
            inline=False
        )
        embed.add_field(
            name="🎧 Post-Punk na Veia",
            value="Para entrar no foco profundo, digite `/som`. Vou te recomendar uma pedrada Goth/Darkwave pra você parar de chorar e começar a programar. Tem links diretos pro Spotify, YouTube e SoundCloud.",
            inline=False
        )
        embed.set_footer(text="Fim do Tutorial. Agora vai trabalhar.")
        return embed

    async def update_message(self, interaction: discord.Interaction):
        embed = self.pages[self.current_page]()
        
        # Lógica dos botões
        self.btn_prev.disabled = (self.current_page == 0)
        self.btn_next.disabled = (self.current_page == len(self.pages) - 1)
        
        await interaction.response.edit_message(embed=embed, view=self)

    @discord.ui.button(label="◀ Anterior", style=discord.ButtonStyle.secondary, disabled=True)
    async def btn_prev(self, interaction: discord.Interaction, button: discord.ui.Button):
        self.current_page -= 1
        await self.update_message(interaction)

    @discord.ui.button(label="Próximo ▶", style=discord.ButtonStyle.primary)
    async def btn_next(self, interaction: discord.Interaction, button: discord.ui.Button):
        self.current_page += 1
        await self.update_message(interaction)


class Tutorial(commands.Cog):
    def __init__(self, bot: commands.Bot):
        self.bot = bot

    @app_commands.command(name="tutorial", description="Aprenda a usar a Tayama sem se perder na burocracia.")
    async def tutorial(self, interaction: discord.Interaction):
        view = TutorialView()
        embed = view.pages[0]()
        
        if self.bot.user.display_avatar:
            embed.set_thumbnail(url=self.bot.user.display_avatar.url)
            
        await interaction.response.send_message(embed=embed, view=view)


async def setup(bot: commands.Bot):
    await bot.add_cog(Tutorial(bot))
