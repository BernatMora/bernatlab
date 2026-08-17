#!/usr/bin/env python
# -*- coding: utf-8 -*-
"""
Bot de Telegram per Hort Osona.

Permet preguntar a l'hort amb el mobil sense instalar res.
Utilitza el RAG local (Ollama + rag.py) per respondre.

CONFIGURACIO SEGURA:
  - El token es llegeix del fitxer .env (NO esta al codi)
  - El fitxer .env ja esta al .gitignore
  - Si no tens .env, el bot t'ho dira en arrencar

US:
  python telegram_bot.py
"""

import os
import sys
import logging
import subprocess
from pathlib import Path
from http.server import BaseHTTPRequestHandler, HTTPServer
import json

# Carregar .env si existeix
try:
    from dotenv import load_dotenv
    env_path = Path(__file__).parent / '.env'
    if env_path.exists():
        load_dotenv(env_path)
    else:
        # Provar al directori pare tambe
        env_path = Path(__file__).parent.parent / '.env'
        if env_path.exists():
            load_dotenv(env_path)
except ImportError:
    print("AVIS: python-dotenv no instal.lat. Usant os.environ directament.")
    print("  Instal.la amb: pip install python-dotenv")

# Configurar logging
logging.basicConfig(
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s',
    level=os.environ.get('LOG_LEVEL', 'INFO')
)
logger = logging.getLogger(__name__)

# Llegir token del .env
TELEGRAM_BOT_TOKEN = os.environ.get('TELEGRAM_BOT_TOKEN')
if not TELEGRAM_BOT_TOKEN:
    print("=" * 70)
    print("ERROR: TELEGRAM_BOT_TOKEN no definit!")
    print("=" * 70)
    print()
    print("Has de crear un fitxer .env amb el token:")
    print()
    print("  1. cp .env.example .env")
    print("  2. Edita .env i posa el teu token real")
    print("  3. Torna a arrencar el bot")
    print()
    print("El token el tens al missatge del BotFather del Telegram.")
    print("Mes info a TELEGRAM-SETUP.md")
    print()
    sys.exit(1)

# Directori del projecte
IOT_DIR = Path(__file__).parent
RAG_SCRIPT = IOT_DIR / 'rag.py'

# Importar la llibreria de Telegram
try:
    from telegram import Update
    from telegram.ext import (
        Application, CommandHandler, MessageHandler, filters,
        ContextTypes
    )
except ImportError:
    print("ERROR: python-telegram-bot no instal.lat!")
    print()
    print("Instal.la amb:")
    print("  pip install python-telegram-bot")
    print()
    print("Si vols, tambe cal:")
    print("  pip install python-dotenv  # per carregar el .env")
    print()
    sys.exit(1)


async def start(update: Update, context: ContextTypes.DEFAULT_TYPE):
    """Handler per /start - missatge de benvinguda."""
    user = update.effective_user
    nom = user.first_name or 'amic'
    text = (
        f"Hola {nom}! Soc el bot de l' *Hort Osona* �\n\n"
        "Pots preguntar-me coses sobre l'hort. Exemples:\n\n"
        "* Quan sembrar carbassa a Osona?\n"
        "* Com combatre el pugo al tomaquet?\n"
        "* Quines plantes adventicies son utils?\n"
        "* Que fer al juliol a l'hort?\n\n"
        "Comandes:\n"
        "* /start - aquest missatge\n"
        "* /ajuda - ajuda\n"
        "* /info - info del sistema\n"
        "* /stats - estadistiques\n"
        "* /sensors - dades dels sensors (si RPi esta configurada)"
    )
    await update.message.reply_text(text, parse_mode='Markdown')


async def ajuda(update: Update, context: ContextTypes.DEFAULT_TYPE):
    """Handler per /ajuda."""
    text = (
        "🌱 *Hort Osona - Ajuda*\n\n"
        "Nomes escriu la teva pregunta en catala i jo la respondre "
        "basant-me en les fitxes locals del projecte.\n\n"
        "Per preguntes llargues pots usar /pregunta <text>.\n\n"
        "Si vols veure l'ultima pregunta amb format, prova:\n"
        "* _Quan sembrar carbassa a Osona?_\n"
        "* _Com fer planter de tomaguets?_\n"
        "* _Plantes medicinals per a l'hivern?_"
    )
    await update.message.reply_text(text, parse_mode='Markdown')


async def info(update: Update, context: ContextTypes.DEFAULT_TYPE):
    """Handler per /info - info del sistema."""
    text = (
        "🤖 *Hort Osona Bot - Info tecnica*\n\n"
        f"*Stack*:\n"
        f"* Python 3.12\n"
        f"* python-telegram-bot\n"
        f"* RAG local (Ollama + rag.py)\n"
        f"* {os.environ.get('OLLAMA_MODEL', 'gemma3:1b')} model\n\n"
        f"*Resposta*:\n"
        f"* En catala\n"
        f"* Basada SOLS en les teves fitxes\n"
        f"* Sense enviar res a Internet (tot local)\n\n"
        f"*Latencia*: 5-60 segons per resposta (depen del model)"
    )
    await update.message.reply_text(text, parse_mode='Markdown')


async def sensors(update: Update, context: ContextTypes.DEFAULT_TYPE):
    """Handler per /sensors - dades dels sensors (placeholder)."""
    text = (
        "📡 *Sensors IoT*\n\n"
        "Encara no configurat en aquest entorn. "
        "Quan la Raspberry Pi estigui operativa, aixo mostrara:\n\n"
        "* Humitat del sol per parcel·la\n"
        "* Temperatura ambient\n"
        "* Lluminositat\n"
        "* Bateria dels nodes\n\n"
        "Mes info: hort-osona-iot/README.md"
    )
    await update.message.reply_text(text, parse_mode='Markdown')


async def pregunta_llarga(update: Update, context: ContextTypes.DEFAULT_TYPE):
    """Handler per /pregunta <text> - permet espais."""
    if not context.args:
        await update.message.reply_text(
            "Us: /pregunta <la teva pregunta>\n"
            "Exemple: /pregunta Quan sembrar carbassa?"
        )
        return
    pregunta = ' '.join(context.args)
    await respond_with_rag(update, pregunta)


async def stats(update: Update, context: ContextTypes.DEFAULT_TYPE):
    """Handler per /stats - estadistiques d'us."""
    import shutil
    disk = shutil.disk_usage("/")
    disk_free_gb = round(disk.free / (1024**3), 1)
    disk_used_gb = round(disk.used / (1024**3), 1)
    try:
        import psutil
        mem = psutil.virtual_memory()
        mem_str = f"{mem.percent}% usat"
    except ImportError:
        mem_str = "N/A"
    text = (
        "📊 *Hort Osona Bot - Estadistiques*\n\n"
        f"*Sistema*\n"
        f"* Disc: {disk_used_gb} GB usat / {disk_free_gb} GB lliure\n"
        f"* RAM: {mem_str}\n\n"
        f"*Configuracio*\n"
        f"* Ollama: `{os.environ.get('OLLAMA_HOST', 'http://localhost:11434')}`\n"
        f"* Model: `{os.environ.get('OLLAMA_MODEL', 'gemma3:1b')}`\n\n"
        f"*Limits*\n"
        f"* Timeout Ollama: {os.environ.get('OLLAMA_TIMEOUT', '180')}s\n"
    )
    await update.message.reply_text(text, parse_mode='Markdown')


async def handle_message(update: Update, context: ContextTypes.DEFAULT_TYPE):
    """Handler per missatges normals (sense /)."""
    pregunta = update.message.text
    user = update.effective_user
    username = user.username if user else None
    first_name = user.first_name if user else None
    user_id = user.id if user else None
    logger.info(
        "MISSATGE de user_id=%s username=%s first_name=%s text=%r",
        user_id, username, first_name, pregunta
    )
    await respond_with_rag(update, pregunta)


async def respond_with_rag(update: Update, pregunta: str):
    """Fa la consulta al RAG i respon."""
    # Missatge d'espera (text pla per seguretat)
    wait_msg = await update.message.reply_text(
        f"🔎 Pensant...\n\n{pregunta}"
    )

    timeout_seconds = int(os.environ.get('OLLAMA_TIMEOUT', '180'))

    try:
        # Cridar el RAG (subprocess per simplificar)
        result = subprocess.run(
            ['python', str(RAG_SCRIPT), pregunta],
            capture_output=True,
            text=True,
            timeout=timeout_seconds,
            cwd=str(IOT_DIR)
        )

        if result.returncode != 0:
            error_text = result.stderr[:500] if result.stderr else "Error desconegut"
            await wait_msg.edit_text(
                f"❌ Error consultant el RAG:\n\n{error_text}\n\n"
                f"Assegura't que Ollama esta corrent amb {os.environ.get('OLLAMA_MODEL', 'gemma3:1b')}."
            )
            return

        # Extreure la resposta
        answer = result.stdout.strip()
        if not answer:
            await wait_msg.edit_text("❌ El RAG no ha retornat res.")
            return

        # Telegram te limit de 4096 caracters per missatge
        if len(answer) > 4000:
            answer = answer[:4000] + "\n\n(resposta tallada)"

        # Enviar com a text pla per evitar errors de Markdown
        await wait_msg.edit_text(f"🌱 Resposta:\n\n{answer}")

        # Netejar text per evitar problemes amb Telegram
        # (resposta ja enviada com a text pla mes amunt)

    except subprocess.TimeoutExpired:
        await wait_msg.edit_text(
            f"⏱ Timeout: el RAG ha trigat mes de {timeout_seconds} segons.\n"
            "Prova amb una pregunta mes curta o concreta.\n\n"
            "Si persisteix, escriu /stats per veure carrega del sistema."
        )
    except FileNotFoundError:
        await wait_msg.edit_text(
            "❌ No trobo `rag.py` al directori del projecte.\n"
            "Comprova que estas al directori correcte."
        )
    except Exception as e:
        logger.exception("Error inesperat")
        await wait_msg.edit_text(f"❌ Error inesperat:\n\n`{e}`")


def main():
    """Arrenca el bot."""
    print("=" * 70)
    print("� Hort Osona - Bot de Telegram")
    print("=" * 70)
    print()
    print(f"Directori: {IOT_DIR}")
    print(f"RAG script: {RAG_SCRIPT}")
    print(f"RAG existeix: {RAG_SCRIPT.exists()}")
    print(f"Token: {'OK (configurat)' if TELEGRAM_BOT_TOKEN else 'FALTA'}")
    print()
    print(f"Model Ollama: {os.environ.get('OLLAMA_MODEL', 'gemma3:1b')}")
    print(f"Host Ollama: {os.environ.get('OLLAMA_HOST', 'http://localhost:11434')}")
    print(f"Timeout: {os.environ.get('OLLAMA_TIMEOUT', '180')}s")
    print()
    print("Pre-escalfant Ollama (pot trigar 20-60s)...")
    try:
        result = subprocess.run(
            ['python', '-c', 'from rag import HortRAG; r = HortRAG(); print("OK" if r.warmup() else "FAIL")'],
            capture_output=True, text=True, timeout=180, cwd=str(IOT_DIR)
        )
        if result.returncode == 0:
            print(f"Ollama pre-escalfat: {result.stdout.strip()}")
        else:
            print(f"AVIS: pre-escalfament no completat: {result.stderr[:200]}")
    except Exception as e:
        print(f"AVIS: pre-escalfament fallit: {e}")
    print()
    print("Arrencant bot...")
    print()

    # Crear aplicacio
    app = Application.builder().token(TELEGRAM_BOT_TOKEN).build()

    # Handlers
    app.add_handler(CommandHandler('start', start))
    app.add_handler(CommandHandler('ajuda', ajuda))
    app.add_handler(CommandHandler('info', info))
    app.add_handler(CommandHandler('sensors', sensors))
    app.add_handler(CommandHandler('pregunta', pregunta_llarga))
    app.add_handler(CommandHandler('stats', stats))

    # Missatges normals (text que no es /comanda)
    app.add_handler(MessageHandler(
        filters.TEXT & ~filters.COMMAND,
        handle_message
    ))

    # Arrencar polling amb interval de 30s per estalviar dades
    poll_interval = int(os.environ.get('POLL_INTERVAL', '30'))
    print("Bot arrencat. Esperant missatges...")
    print(f"Interval de polling: {poll_interval}s (per estalviar dades)")
    print("Prem Ctrl+C per parar.")
    print()
    app.run_polling(allowed_updates=Update.ALL_TYPES, poll_interval=poll_interval)


if __name__ == '__main__':
    main()
