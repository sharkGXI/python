"""
Instagram Post Scheduler
------------------------
Programa para logar no Instagram (conta pessoal) e publicar posts
automaticamente em datas/horários pré-agendados.

ATENÇÃO:
- Usa a biblioteca não-oficial "instagrapi". Isso NÃO é aprovado
  pelo Instagram/Meta e existe risco de bloqueio temporário da conta
  em caso de uso muito frequente ou agressivo.
- Use por sua conta e risco, apenas para publicar conteúdo seu.
- Recomenda-se não postar mais que algumas vezes ao dia e sempre
  incluir intervalos (delays) entre ações, como já está configurado
  neste script.

Como usar:
1. pip install -r requirements.txt
2. Copie .env.example para .env e preencha usuário/senha
3. Coloque suas imagens na pasta "posts/"
4. Edite o arquivo schedule_config.json com data, hora, imagem e legenda
5. Rode: python main.py
   (deixe rodando em segundo plano; ele checa a cada minuto se é hora
   de publicar algo)
"""

import json
import os
import sys
import time
from datetime import datetime
from pathlib import Path

from dotenv import load_dotenv
from instagrapi import Client
from instagrapi.exceptions import (
    LoginRequired,
    ChallengeRequired,
    TwoFactorRequired,
    BadPassword,
)

BASE_DIR = Path(__file__).resolve().parent
SESSION_FILE = BASE_DIR / "session.json"
CONFIG_FILE = BASE_DIR / "schedule_config.json"
LOG_FILE = BASE_DIR / "scheduler.log"

load_dotenv(BASE_DIR / ".env")


def log(msg: str):
    timestamp = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
    line = f"[{timestamp}] {msg}"
    print(line)
    with open(LOG_FILE, "a", encoding="utf-8") as f:
        f.write(line + "\n")


def load_config() -> dict:
    with open(CONFIG_FILE, "r", encoding="utf-8") as f:
        return json.load(f)


def save_config(config: dict):
    with open(CONFIG_FILE, "w", encoding="utf-8") as f:
        json.dump(config, f, ensure_ascii=False, indent=2)


def get_client() -> Client:
    """
    Loga no Instagram, reaproveitando a sessão salva sempre que possível
    para reduzir o número de logins (o que ajuda a evitar bloqueios).
    """
    username = os.getenv("IG_USERNAME")
    password = os.getenv("IG_PASSWORD")

    if not username or not password:
        log("ERRO: defina IG_USERNAME e IG_PASSWORD no arquivo .env")
        sys.exit(1)

    cl = Client()

    if SESSION_FILE.exists():
        try:
            cl.load_settings(SESSION_FILE)
            cl.login(username, password)
            # valida se a sessão ainda é válida
            cl.get_timeline_feed()
            log("Login feito reaproveitando sessão salva.")
            return cl
        except LoginRequired:
            log("Sessão salva expirou, fazendo novo login...")
        except Exception as e:
            log(f"Falha ao reaproveitar sessão ({e}), tentando novo login...")

    try:
        cl.login(username, password)
        cl.dump_settings(SESSION_FILE)
        log("Login realizado com sucesso e sessão salva.")
    except TwoFactorRequired:
        code = input("Digite o código de verificação em duas etapas (2FA): ")
        cl.login(username, password, verification_code=code)
        cl.dump_settings(SESSION_FILE)
        log("Login com 2FA realizado com sucesso.")
    except ChallengeRequired:
        log(
            "ERRO: Instagram pediu um desafio de segurança (challenge). "
            "Abra o app/site do Instagram, confirme que é você, e rode o "
            "script novamente."
        )
        sys.exit(1)
    except BadPassword:
        log("ERRO: usuário ou senha incorretos.")
        sys.exit(1)

    return cl


def publish_post(cl: Client, post: dict) -> bool:
    media_path = BASE_DIR / post["media_path"]

    if not media_path.exists():
        log(f"ERRO: arquivo não encontrado: {media_path}")
        return False

    caption = post.get("caption", "")
    post_type = post.get("type", "photo")

    try:
        if post_type == "photo":
            cl.photo_upload(media_path, caption)
        elif post_type == "video":
            cl.video_upload(media_path, caption)
        elif post_type == "reel":
            cl.clip_upload(media_path, caption)
        else:
            log(f"Tipo de post desconhecido: {post_type}")
            return False

        log(f"Post '{post['id']}' publicado com sucesso!")
        return True

    except Exception as e:
        log(f"ERRO ao publicar post '{post['id']}': {e}")
        return False


def check_and_publish(cl: Client):
    config = load_config()
    now = datetime.now()
    changed = False

    for post in config["posts"]:
        if post.get("posted"):
            continue

        scheduled_dt = datetime.strptime(
            f"{post['date']} {post['time']}", "%Y-%m-%d %H:%M"
        )

        if now >= scheduled_dt:
            log(f"Publicando post agendado: {post['id']}")
            success = publish_post(cl, post)
            if success:
                post["posted"] = True
                changed = True
                # pequeno delay de segurança entre uploads
                time.sleep(15)

    if changed:
        save_config(config)


def main():
    log("Iniciando Instagram Post Scheduler...")
    cl = get_client()

    log("Monitorando agendamentos (verificação a cada 60 segundos)...")
    try:
        while True:
            check_and_publish(cl)
            time.sleep(60)
    except KeyboardInterrupt:
        log("Encerrado pelo usuário.")


if __name__ == "__main__":
    main()
