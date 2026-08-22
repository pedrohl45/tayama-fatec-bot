import os
import logging
from datetime import time, timezone, timedelta
from zoneinfo import ZoneInfo, ZoneInfoNotFoundError

import discord
from discord.ext import commands, tasks

from services.fatec_service import get_aulas_do_dia

logger = logging.getLogger("TayamaBot")

# Fuso horário de Brasília (UTC-3).
# Brasil aboliu o horário de verão em 2019 — UTC-3 fixo é sempre correto.
# Tenta usar o banco de dados de fuso horário do sistema/tzdata;
# se não estiver disponível (comum no Windows sem tzdata instalado), usa offset fixo.
try:
    BRT = ZoneInfo("America/Sao_Paulo")
except ZoneInfoNotFoundError:
    logger.warning(
        "tzdata nao encontrado — usando offset fixo UTC-3 para BRT. "
        "Instale com: pip install tzdata"
    )
    BRT = timezone(timedelta(hours=-3))

DIAS_SEMANA = {
    0: "Segunda-feira",
    1: "Terça-feira",
    2: "Quarta-feira",
    3: "Quinta-feira",
    4: "Sexta-feira",
    5: "Sábado",
    6: "Domingo",
}


class Rotinas(commands.Cog):
    def __init__(self, bot: commands.Bot):
        self.bot = bot
        self._canal_id: int | None = self._ler_canal_id()
        self.lembrete_matinal.start()
        logger.info(f"Rotinas iniciadas. Canal de avisos: {self._canal_id}")

    def cog_unload(self):
        self.lembrete_matinal.cancel()

    @staticmethod
    def _ler_canal_id() -> int | None:
        raw = os.getenv("CANAL_AVISOS_ID", "").strip()
        if raw.isdigit():
            return int(raw)
        return None

    # ──────────────────────────────────────────
    # Task: lembrete matinal às 07:00 BRT
    # ──────────────────────────────────────────

    @tasks.loop(time=time(hour=7, minute=0, tzinfo=BRT))
    async def lembrete_matinal(self):
        """Posta a grade do dia no canal configurado, de segunda a sexta."""
        if self._canal_id is None:
            logger.warning(
                "Lembrete matinal: CANAL_AVISOS_ID não definido no .env — pulando."
            )
            return

        canal = self.bot.get_channel(self._canal_id)
        if canal is None:
            logger.warning(
                f"Lembrete matinal: canal {self._canal_id} não encontrado. "
                "Verifique se o bot tem acesso ao canal."
            )
            return

        from datetime import datetime

        hoje_num = datetime.now(tz=BRT).weekday()
        hoje_nome = DIAS_SEMANA[hoje_num]

        # Não posta nos fins de semana
        if hoje_num >= 5:
            return

        try:
            aulas = await get_aulas_do_dia(hoje_nome)
        except Exception:
            logger.error("Lembrete matinal: erro ao carregar aulas", exc_info=True)
            return

        if not aulas:
            return  # Dia sem aulas — sem mensagem

        embed = discord.Embed(
            title=f"☀️ Bom dia! Grade de hoje — {hoje_nome}",
            description="Não esquece de tomar café antes de sair. ☕",
            color=discord.Color.from_str("#ff73fa"),
        )

        for aula in aulas:
            embed.add_field(
                name=f"{aula['codigo']} — {aula['nome']}",
                value=(
                    f"⏰ **{aula['inicio']} às {aula['fim']}**\n"
                    f"👨‍🏫 {aula['professor']}\n"
                    f"🏫 {aula['sala']}"
                ),
                inline=False,
            )

        embed.set_footer(text="Tayama • FATEC DSM — bora lá! 📚")

        try:
            await canal.send(embed=embed)
            logger.info(f"Lembrete matinal enviado para canal {self._canal_id}.")
        except discord.Forbidden:
            logger.error(
                f"Lembrete matinal: sem permissão para postar no canal {self._canal_id}."
            )
        except Exception:
            logger.error("Lembrete matinal: erro ao enviar mensagem", exc_info=True)

    @lembrete_matinal.before_loop
    async def before_lembrete(self):
        await self.bot.wait_until_ready()


async def setup(bot: commands.Bot):
    await bot.add_cog(Rotinas(bot))

