import logging
import os

import discord
from discord import app_commands
from discord.ext import commands
from dotenv import load_dotenv

load_dotenv()

TOKEN = os.getenv("DISCORD_TOKEN", "").strip()
GUILD_ID = os.getenv("GUILD_ID", "").strip()

if not TOKEN:
    raise RuntimeError(".env 파일에 DISCORD_TOKEN을 입력해 주세요.")

logging.basicConfig(level=logging.INFO)

intents = discord.Intents.default()
intents.voice_states = True


class VoiceBot(commands.Bot):
    async def setup_hook(self):
        if GUILD_ID:
            guild = discord.Object(id=int(GUILD_ID))
            self.tree.copy_global_to(guild=guild)
            synced = await self.tree.sync(guild=guild)
            print(f"서버 {GUILD_ID} 명령어 {len(synced)}개 동기화 완료")
        else:
            synced = await self.tree.sync()
            print(f"전역 명령어 {len(synced)}개 동기화 완료 (표시까지 시간이 걸릴 수 있습니다)")


bot = VoiceBot(command_prefix="!", intents=intents)


@bot.event
async def on_ready():
    print(f"로그인 완료: {bot.user} (ID: {bot.user.id})")


@bot.tree.command(name="입장", description="봇이 내가 들어가 있는 음성 채널에 입장합니다.")
@app_commands.guild_only()
async def join(interaction: discord.Interaction):
    if interaction.guild is None:
        await interaction.response.send_message("서버에서만 사용할 수 있습니다.", ephemeral=True)
        return

    member = interaction.user
    if not isinstance(member, discord.Member) or member.voice is None or member.voice.channel is None:
        await interaction.response.send_message("먼저 음성 채널에 들어가 주세요!", ephemeral=True)
        return

    channel = member.voice.channel
    if not isinstance(channel, discord.VoiceChannel):
        await interaction.response.send_message("일반 음성 채널에서 사용해 주세요.", ephemeral=True)
        return

    me = interaction.guild.me
    if me is None or not channel.permissions_for(me).connect:
        await interaction.response.send_message("해당 음성 채널에 연결할 권한이 없습니다.", ephemeral=True)
        return

    await interaction.response.defer(ephemeral=True)
    voice = interaction.guild.voice_client
    try:
        if voice and voice.is_connected():
            if voice.channel.id == channel.id:
                await interaction.followup.send("이미 같은 음성 채널에 들어와 있습니다!", ephemeral=True)
                return
            await voice.move_to(channel)
            message = f"🔊 **{channel.name}** 채널로 이동했습니다!"
        else:
            if voice is not None:
                await voice.disconnect(force=True)
            await channel.connect(timeout=30, reconnect=True)
            message = f"🔊 **{channel.name}** 채널에 입장했습니다!"
        await interaction.followup.send(message, ephemeral=True)
    except (discord.DiscordException, TimeoutError, OSError) as error:
        logging.exception("음성 채널 입장 실패: %s", error)
        await interaction.followup.send("음성 채널에 연결하지 못했습니다. 봇 권한과 연결 상태를 확인해 주세요.", ephemeral=True)


@bot.tree.command(name="퇴장", description="봇이 음성 채널에서 나갑니다.")
@app_commands.guild_only()
async def leave(interaction: discord.Interaction):
    if interaction.guild is None:
        await interaction.response.send_message("서버에서만 사용할 수 있습니다.", ephemeral=True)
        return

    voice = interaction.guild.voice_client
    if voice is None or not voice.is_connected():
        await interaction.response.send_message("봇이 음성 채널에 들어와 있지 않습니다.", ephemeral=True)
        return

    await interaction.response.defer(ephemeral=True)
    try:
        await voice.disconnect(force=True)
        await interaction.followup.send("👋 음성 채널에서 나왔습니다!", ephemeral=True)
    except (discord.DiscordException, OSError) as error:
        logging.exception("음성 채널 퇴장 실패: %s", error)
        await interaction.followup.send("퇴장하는 중 문제가 발생했습니다.", ephemeral=True)


bot.run(TOKEN)
