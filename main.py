import asyncio
import os
import sys
import logging
import discord
from discord.ext import commands
from dotenv import load_dotenv

# Configuração de Logs
logging.basicConfig(
    level=logging.INFO,
    format="%(asctime)s [%(levelname)s] %(name)s: %(message)s",
    handlers=[logging.StreamHandler(sys.stdout)]
)
logger = logging.getLogger("TayamaBot")

load_dotenv()

TOKEN = os.getenv("DISCORD_TOKEN")
SYNC_COMMANDS = os.getenv("SYNC_COMMANDS", "false").lower() == "true"

# Remove < > caso o ID tenha sido colado no formato de menção do Discord
_raw_guild_id = os.getenv("GUILD_ID", "").strip().strip("<>")
if _raw_guild_id and not _raw_guild_id.isdigit():
    logger.error(
        f"GUILD_ID inválido no .env: '{_raw_guild_id}'. "
        "Deve ser apenas o número do ID (ex: 1234567890). Colchetes < > não são necessários."
    )
    _raw_guild_id = ""
GUILD_ID: str = _raw_guild_id


class TayamaBot(commands.Bot):
    def __init__(self):
        intents = discord.Intents.default()
        intents.message_content = True
        super().__init__(
            command_prefix="!",
            intents=intents,
            activity=discord.Activity(
                type=discord.ActivityType.watching,
                name="Depurando sanidades • /ajuda"
            )
        )

    async def setup_hook(self):
        # 1. Carrega todos os cogs dinamicamente
        for filename in sorted(os.listdir("./cogs")):
            if filename.endswith(".py") and not filename.startswith("__"):
                cog_name = f"cogs.{filename[:-3]}"
                try:
                    await self.load_extension(cog_name)
                    logger.info(f"Cog carregado: {cog_name}")
                except Exception as e:
                    logger.error(f"Falha ao carregar cog {cog_name}: {e}", exc_info=True)
                    
        # 2. A Sincronização foi movida para on_ready para podermos limpar as duplicadas.
        pass

    async def on_ready(self):
        logger.info("=" * 45)
        logger.info(" Tayama FATEC Bot Online!")
        logger.info(f" Usuário: {self.user} (ID: {self.user.id})")
        logger.info(f" Conectado em {len(self.guilds)} servidores")
        logger.info("=" * 45)

        if SYNC_COMMANDS:
            if GUILD_ID:
                guild = discord.Object(id=int(GUILD_ID))
                self.tree.copy_global_to(guild=guild)
                await self.tree.sync(guild=guild)
                logger.info(f"Slash commands sincronizados para a guild {GUILD_ID}.")
            else:
                logger.info("Limpando comandos locais antigos para remover DUPLICADAS (bot publico)...")
                for guild in self.guilds:
                    self.tree.clear_commands(guild=guild)
                    await self.tree.sync(guild=guild)
                
                logger.info("Sincronizando a arvore Global do bot...")
                await self.tree.sync()
                logger.info("Sync Global Concluido! Feche e abra o app do seu Discord para atualizar.")


async def main():
    if not TOKEN or TOKEN.strip() == "" or "seu_token" in TOKEN:
        logger.error("Erro: DISCORD_TOKEN inválido ou não definido no arquivo .env!")
        logger.error("Preencha o arquivo .env com seu token do Discord Developer Portal.")
        return

    bot = TayamaBot()
    async with bot:
        await bot.start(TOKEN)


if __name__ == "__main__":
    asyncio.run(main())
