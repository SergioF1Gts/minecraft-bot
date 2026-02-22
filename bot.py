import os
from dotenv import load_dotenv
from telegram import Update, ReplyKeyboardMarkup, ReplyKeyboardRemove
from telegram.ext import (
    ApplicationBuilder, CommandHandler, MessageHandler,
    filters, ContextTypes, ConversationHandler
)
from excel_manager import (
    inicializar_excel, agregar_servidor, obtener_servidores,
    actualizar_estado, obtener_estadisticas
)

load_dotenv()
TOKEN = os.getenv("BOT_TOKEN")

# Estados
NOMBRE, IP, VERSION, TIPO = range(4)
ESTADO_ID, ESTADO_NUEVO = range(4, 6)

VERSIONES = [["1.8", "1.12.2"], ["1.16.5", "1.18.2"], ["1.19.4", "1.20.1"]]
TIPOS = [["Survival", "Creative"], ["Minigames", "SkyBlock"]]

async def start(update: Update, context: ContextTypes.DEFAULT_TYPE):
    await update.message.reply_text(
        "⛏️ *Bienvenido al Bot de Servidores Minecraft* ⛏️\n\n"
        "Gestiona tus servidores estilo Aternos desde Telegram.\n\n"
        "📌 *Comandos disponibles:*\n"
        "/agregar — Registrar un nuevo servidor\n"
        "/ver — Ver todos los servidores\n"
        "/estado — Cambiar estado de un servidor\n"
        "/stats — Ver estadísticas generales\n"
        "/cancelar — Cancelar operación actual",
        parse_mode="Markdown"
    )

async def agregar_inicio(update: Update, context: ContextTypes.DEFAULT_TYPE):
    await update.message.reply_text(
        "🟩 *Registrar nuevo servidor*\n\n¿Cuál es el nombre del servidor?",
        parse_mode="Markdown",
        reply_markup=ReplyKeyboardRemove()
    )
    return NOMBRE

async def recibir_nombre(update: Update, context: ContextTypes.DEFAULT_TYPE):
    context.user_data["nombre"] = update.message.text
    await update.message.reply_text("🌐 ¿Cuál es la IP? (ej: miservidor.aternos.me)")
    return IP

async def recibir_ip(update: Update, context: ContextTypes.DEFAULT_TYPE):
    context.user_data["ip"] = update.message.text
    await update.message.reply_text(
        "📦 ¿Qué versión de Minecraft usa?",
        reply_markup=ReplyKeyboardMarkup(VERSIONES, one_time_keyboard=True, resize_keyboard=True)
    )
    return VERSION

async def recibir_version(update: Update, context: ContextTypes.DEFAULT_TYPE):
    context.user_data["version"] = update.message.text
    await update.message.reply_text(
        "🎮 ¿Qué tipo de servidor es?",
        reply_markup=ReplyKeyboardMarkup(TIPOS, one_time_keyboard=True, resize_keyboard=True)
    )
    return TIPO

async def recibir_tipo(update: Update, context: ContextTypes.DEFAULT_TYPE):
    tipo = update.message.text
    nombre = context.user_data["nombre"]
    ip = context.user_data["ip"]
    version = context.user_data["version"]
    server_id = agregar_servidor(nombre, ip, version, tipo)
    await update.message.reply_text(
        f"✅ *¡Servidor registrado exitosamente!*\n\n"
        f"🆔 ID: `{server_id}`\n"
        f"🏷️ Nombre: {nombre}\n"
        f"🌐 IP: `{ip}`\n"
        f"📦 Versión: {version}\n"
        f"🎮 Tipo: {tipo}\n"
        f"🔴 Estado: Offline\n\n"
        f"Usa /estado para cambiar su estado cuando lo inicies.",
        parse_mode="Markdown",
        reply_markup=ReplyKeyboardRemove()
    )
    return ConversationHandler.END

async def ver_servidores(update: Update, context: ContextTypes.DEFAULT_TYPE):
    servidores = obtener_servidores()
    if not servidores:
        await update.message.reply_text("📭 No hay servidores registrados aún.\nUsa /agregar para añadir uno.")
        return
    texto = "🗺️ *Lista de Servidores:*\n\n"
    for s in servidores:
        sid, nombre, ip, version, tipo, estado, fecha = s
        texto += (
            f"{estado} *{nombre}*\n"
            f"   🆔 ID: `{sid}` | 📦 {version} | 🎮 {tipo}\n"
            f"   🌐 `{ip}`\n"
            f"   📅 Registrado: {fecha}\n\n"
        )
    await update.message.reply_text(texto, parse_mode="Markdown")

async def estado_inicio(update: Update, context: ContextTypes.DEFAULT_TYPE):
    servidores = obtener_servidores()
    if not servidores:
        await update.message.reply_text("📭 No hay servidores registrados. Usa /agregar primero.")
        return ConversationHandler.END
    texto = "🔧 *¿Qué servidor quieres actualizar?*\n\nEscribe el ID:\n\n"
    for s in servidores:
        texto += f"  {s[5]} ID `{s[0]}` — {s[1]}\n"
    await update.message.reply_text(texto, parse_mode="Markdown")
    return ESTADO_ID

async def recibir_estado_id(update: Update, context: ContextTypes.DEFAULT_TYPE):
    try:
        context.user_data["estado_id"] = int(update.message.text)
        await update.message.reply_text(
            "¿Cuál es el nuevo estado?",
            reply_markup=ReplyKeyboardMarkup(
                [["🟢 Online", "🔴 Offline"], ["🟡 Mantenimiento"]],
                one_time_keyboard=True, resize_keyboard=True
            )
        )
        return ESTADO_NUEVO
    except ValueError:
        await update.message.reply_text("❌ Eso no es un ID válido. Escribe solo el número.")
        return ESTADO_ID

async def recibir_estado_nuevo(update: Update, context: ContextTypes.DEFAULT_TYPE):
    nuevo_estado = update.message.text
    server_id = context.user_data["estado_id"]
    exito = actualizar_estado(server_id, nuevo_estado)
    if exito:
        await update.message.reply_text(
            f" Servidor ID `{server_id}` actualizado a {nuevo_estado}",
            parse_mode="Markdown",
            reply_markup=ReplyKeyboardRemove()
        )
    else:
        await update.message.reply_text(
            f" No se encontró un servidor con ID `{server_id}`.",
            parse_mode="Markdown",
            reply_markup=ReplyKeyboardRemove()
        )
    return ConversationHandler.END

async def ver_stats(update: Update, context: ContextTypes.DEFAULT_TYPE):
    total, online, offline, versiones = obtener_estadisticas()
    if total == 0:
        await update.message.reply_text("📭 No hay servidores registrados aún.")
        return
    texto = (
        " *Estadísticas Generales*\n\n"
        f" Total de servidores: *{total}*\n"
        f" Online: *{online}*\n"
        f" Offline: *{offline}*\n\n"
        " *Por versión:*\n"
    )
    for version, cantidad in versiones.items():
        texto += f"  • {version}: {cantidad} servidor(es)\n"
    await update.message.reply_text(texto, parse_mode="Markdown")

async def cancelar(update: Update, context: ContextTypes.DEFAULT_TYPE):
    await update.message.reply_text("❌ Operación cancelada.", reply_markup=ReplyKeyboardRemove())
    return ConversationHandler.END

if __name__ == "__main__":
    inicializar_excel()
    app = ApplicationBuilder().token(TOKEN).build()

    conv_agregar = ConversationHandler(
        entry_points=[CommandHandler("agregar", agregar_inicio)],
        states={
            NOMBRE: [MessageHandler(filters.TEXT & ~filters.COMMAND, recibir_nombre)],
            IP: [MessageHandler(filters.TEXT & ~filters.COMMAND, recibir_ip)],
            VERSION: [MessageHandler(filters.TEXT & ~filters.COMMAND, recibir_version)],
            TIPO: [MessageHandler(filters.TEXT & ~filters.COMMAND, recibir_tipo)],
        },
        fallbacks=[CommandHandler("cancelar", cancelar)],
    )

    conv_estado = ConversationHandler(
        entry_points=[CommandHandler("estado", estado_inicio)],
        states={
            ESTADO_ID: [MessageHandler(filters.TEXT & ~filters.COMMAND, recibir_estado_id)],
            ESTADO_NUEVO: [MessageHandler(filters.TEXT & ~filters.COMMAND, recibir_estado_nuevo)],
        },
        fallbacks=[CommandHandler("cancelar", cancelar)],
    )

    app.add_handler(CommandHandler("start", start))
    app.add_handler(conv_agregar)
    app.add_handler(conv_estado)
    app.add_handler(CommandHandler("ver", ver_servidores))
    app.add_handler(CommandHandler("stats", ver_stats))

    print("⛏️ Bot de Minecraft corriendo...")
    app.run_polling()