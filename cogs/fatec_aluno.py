import discord
from discord.ext import commands
from discord import app_commands
from database.mysql_db import get_aluno

class FatecAluno(commands.Cog):
    def __init__(self, bot):
        self.bot = bot

    @app_commands.command(name="perfil_fatec", description="Dados da secretaria, matrícula e horas complementares.")
    async def perfil(self, interaction: discord.Interaction):
        await interaction.response.defer(thinking=True)
        aluno = await get_aluno(str(interaction.user.id))
        
        if not aluno:
            await interaction.followup.send("⚠️ Você não possui perfil cadastrado. Use `/perfil_setup` para se cadastrar.", ephemeral=True)
            return
        
        embed = discord.Embed(title="🎓 Secretaria Virtual FATEC", color=discord.Color.from_str("#c82245"))
        
        # Exibe apenas nome e curso (sem dados sensíveis como RA e e-mail)
        embed.add_field(
            name="Aluno", 
            value=f"**Nome:** {aluno.get('nome', 'Aluno')}\n**Curso:** {aluno.get('curso', 'DSM')} - {aluno.get('semestre', 1)}º Sem.", 
            inline=False
        )
        embed.add_field(
            name="Status Acadêmico", 
            value=f"**Matrícula:** {aluno.get('status_matricula', 'Matriculado')}\n**Progresso:** {aluno.get('progresso_curso', 0)}%", 
            inline=True
        )
        embed.add_field(
            name="Horas Complementares", 
            value=f"{aluno.get('horas_cumpridas', 0)} / {aluno.get('horas_exigidas', 120)}h", 
            inline=True
        )
            
        await interaction.followup.send(embed=embed)

async def setup(bot):
    await bot.add_cog(FatecAluno(bot))
