# 디스코드 음성 채널 입장 봇

## 준비
- Python 3.10 이상 (권장 3.11~3.13)
- [Discord Developer Portal](https://discord.com/developers/applications) 에서 애플리케이션 생성 → Bot 토큰 발급
- OAuth2 URL Generator에서 `bot`, `applications.commands` 선택 후 서버에 초대
- 봇에는 음성 채널의 **연결(Connect)** 권한 부여

## 실행
1. `.env.example`을 `.env`로 복사합니다.
2. `.env`의 `DISCORD_TOKEN`에 봇 토큰을, `GUILD_ID`에 명령어를 쓸 디스코드 서버 ID를 입력합니다. (GUILD_ID를 비우면 전역 명령어를 사용합니다.)
3. 터미널에서 다음을 실행합니다.

```bash
python -m pip install -r requirements.txt
python bot.py
```

## 명령어
- `/입장`: 명령어를 쓴 이용자가 접속해 있는 음성 채널로 입장 또는 이동
- `/퇴장`: 음성 채널 연결 종료

## 참고
- `.env` 파일이나 봇 토큰을 공개 저장소에 올리지 마세요.
- `GUILD_ID`를 입력하면 해당 서버의 슬래시 명령어가 빠르게 등록됩니다.
- 이 봇은 입장·퇴장만 하며 음악을 재생하지 않습니다.
