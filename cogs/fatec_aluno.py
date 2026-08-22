import discord
from discord.ext import commands
from discord import app_commands
from database.user_db import get_user_data

class FatecAluno(commands.Cog):
    def __init__(self, bot):
        self.bot = bot

    @app_commands.command(name="perfil_fatec", description="Dados da secretaria, matrícula e horas complementares.")
    async def perfil(self, interaction: discord.Interaction):
        await interaction.response.defer(thinking=True)
        dados = await get_user_data(interaction.user.id)
        
        aluno = dados.get("aluno", {}) if isinstance(dados, dict) else {}
        sec = dados.get("secretaria", {}) if isinstance(dados, dict) else {}
        hc = dados.get("horas_complementares", {}) if isinstance(dados, dict) else {}
        
        embed = discord.Embed(title="🎓 Secretaria Virtual FATEC", color=discord.Color.from_str("#c82245"))
        
        # Exibe apenas nome e curso (sem dados sensíveis como RA e e-mail)
        embed.add_field(
            name="Aluno", 
            value=f"**Nome:** {aluno.get('nome', 'Aluno')}\n**Curso:** {aluno.get('curso', 'DSM')}", 
            inline=False
        )
        embed.add_field(
            name="Status Acadêmico", 
            value=f"**Matrícula:** {sec.get('status_matricula', 'Ativa')}\n**Progresso:** {aluno.get('progresso_curso_percentual', 0)}%", 
            inline=True
        )
        embed.add_field(
            name="Horas Complementares", 
            value=f"{hc.get('carga_horaria_cumprida', 0)} / {hc.get('carga_horaria_exigida', 120)}h", 
            inline=True
        )
        
        avisos = sec.get('avisos', [])
        if avisos:
            embed.add_field(name=f"🔔 Último Aviso ({avisos[0].get('data', '')})", value=avisos[0].get('assunto', ''), inline=False)
            
        await interaction.followup.send(embed=embed)

async def setup(bot):
    await bot.add_cog(FatecAluno(bot))
