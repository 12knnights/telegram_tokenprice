import os
from telegram import Update, BotCommand
from telegram.ext import ApplicationBuilder, CommandHandler, ContextTypes, Application
from fastapi import FastAPI, Request


BotToken = "7369385672:AAEu8sYSzqUiMcHN9knHkIX7R_orLHbK8pk"

# AquariusOnSol
AQUARIUS = "C49Ut3om3QFTDrMZ5Cr8VcTKPpHDcQ2Fv8mmuJHHigDt"
# PiscesOnSol
PISCES = "3JsSsmGzjWDNe9XCw2L9vznC5JU9wSqQeB6ns5pAkPeE"
# AriesOnSol
ARIES = "GhFiFrExPY3proVF96oth1gESWA5QPQzdtb8cy8b1YZv"
# TaurusOnSol
TAURUS = "EjkkxYpfSwS6TAtKKuiJuNMMngYvumc1t1v9ZX1WJKMp"
# GeminiOnSol
GEMINI = "ARiZfq6dK19uNqxWyRudhbM2MswLyYhVUHdndGkffdGc"
# CancerOnSol
CANCER = "CmomKM8iPKRSMN7y1jqyW1QKj5bGoZmbvNZXWBJSUdnZ"
# LeoOnSol
LEO = "8Cd7wXoPb5Yt9cUGtmHNqAEmpMDrhfcVqnGbLC48b8Qm"
# VirgoOnSol
VIRGO = "Ez4bst5qu5uqX3AntYWUdafw9XvtFeJ3gugytKKbSJso"
# LibraOnSol
LIBRA = "7Zt2KUh5mkpEpPGcNcFy51aGkh9Ycb5ELcqRH1n2GmAe"
# ScorpioOnSol
SCORPIO = "J4fQTRN13MKpXhVE74t99msKJLbrjegjEgLBnzEv2YH1"
# SagittariusOnSol
SAGITTARIUS = "8x17zMmVjJxqswjX4hNpxVPc7Tr5UabVJF3kv8TKq8Y3"
# CapricornOnSol
CAPRICORN = "3C2SN1FjzE9MiLFFVRp7Jhkp8Gjwpk29S2TCSJ2jkHn2"

app = FastAPI()
bot_application = None

async def hello(update: Update, context: ContextTypes.DEFAULT_TYPE) -> None:
    await update.message.reply_text(f'Hello {update.effective_user.first_name}')

def get_token_price(token_address: str) -> float:
    url = f'https://api.dexscreener.com/latest/dex/tokens/{token_address}'
    response = requests.get(url)
    data = response.json()
    price = data['pairs'][0]['priceUsd']
    return price

async def handle_token_price(update: Update, context: ContextTypes.DEFAULT_TYPE, token_address: str) -> None:
    try:
        loop = asyncio.get_event_loop()
        price = await loop.run_in_executor(None, get_token_price, token_address)
        await update.message.reply_text(f'The price of the token is {price} USD')
    except Exception as e:
        await update.message.reply_text(f'Error: {e}')

async def set_commands(application: Application) -> None:
    commands = [
        BotCommand("hello", "Say hello"),
        BotCommand("aries", "Get Aries token price"),
        BotCommand("taurus", "Get Taurus token price"),
        BotCommand("gemini", "Get Gemini token price"),
        BotCommand("cancer", "Get Cancer token price"),
        BotCommand("leo", "Get Leo token price"),
        BotCommand("virgo", "Get Virgo token price"),
        BotCommand("libra", "Get Libra token price"),
        BotCommand("scorpio", "Get Scorpio token price"),
        BotCommand("sagittarius", "Get Sagittarius token price"),
        BotCommand("capricorn", "Get Capricorn token price"),
        BotCommand("aquarius", "Get Aquarius token price"),
        BotCommand("pisces", "Get Pisces token price")
    ]
    await application.bot.set_my_commands(commands)

async def setup_application():
    bot_token = os.environ.get("BOT_TOKEN")
    if not bot_token:
        raise ValueError("No BOT_TOKEN provided")
    
    application = ApplicationBuilder().token(bot_token).build()
    
    # 添加所有的命令处理器
    application.add_handler(CommandHandler("aquarius", lambda update, context: handle_token_price(update, context, AQUARIUS)))
    application.add_handler(CommandHandler("pisces", lambda update, context: asyncio.create_task(handle_token_price(update, context, PISCES))))
    application.add_handler(CommandHandler("aries", lambda update, context: asyncio.create_task(handle_token_price(update, context, ARIES))))
    application.add_handler(CommandHandler("taurus", lambda update, context: asyncio.create_task(handle_token_price(update, context, TAURUS))))
    application.add_handler(CommandHandler("gemini", lambda update, context: asyncio.create_task(handle_token_price(update, context, GEMINI))))
    application.add_handler(CommandHandler("cancer", lambda update, context: asyncio.create_task(handle_token_price(update, context, CANCER))))
    application.add_handler(CommandHandler("leo", lambda update, context: asyncio.create_task(handle_token_price(update, context, LEO))))
    application.add_handler(CommandHandler("virgo", lambda update, context: asyncio.create_task(handle_token_price(update, context, VIRGO))))
    application.add_handler(CommandHandler("libra", lambda update, context: asyncio.create_task(handle_token_price(update, context, LIBRA))))
    application.add_handler(CommandHandler("scorpio", lambda update, context: asyncio.create_task(handle_token_price(update, context, SCORPIO))))
    application.add_handler(CommandHandler("sagittarius", lambda update, context: asyncio.create_task(handle_token_price(update, context, SAGITTARIUS))))
    application.add_handler(CommandHandler("capricorn", lambda update, context: asyncio.create_task(handle_token_price(update, context, CAPRICORN))))
    application.add_handler(CommandHandler("hello", hello))
    
    # 设置命令列表
    await set_commands(application)
    
    return application

@app.on_event("startup")
async def startup_event():
    global bot_application
    try:
        bot_application = await setup_application()
        print("Bot application setup completed")
    except Exception as e:
        print(f"Error setting up bot application: {e}")
        raise

@app.post("/webhook")
async def webhook(request: Request):
    global bot_application
    if bot_application is None:
        print("Bot application is not initialized")
        return {"error": "Bot application not initialized"}
    try:
        update = Update.de_json(await request.json(), bot_application.bot)
        await bot_application.process_update(update)
        return {"ok": True}
    except Exception as e:
        print(f"Error processing update: {e}")
        return {"error": str(e)}

@app.get("/")
async def root():
    return {"message": "Bot is running", "bot_initialized": bot_application is not None}