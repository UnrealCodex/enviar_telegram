import time
import pyautogui
from PIL import Image
import imagehash
import asyncio
import telegram

# Configura tu bot de Telegram
bot_token = '7126831157:AAFEYlfqAmTEKYx5DK5IQqL_yLpX-tuKteA'
chat_id = '-4207303534'
bot = telegram.Bot(token=bot_token)

# Coordenadas y dimensiones del área de la pantalla que deseamos capturar
left = 1850
top = 79
width = 24
height = 24

# Ruta y nombre de archivo para la imagen de referencia predefinida
imagen_referencia_path = 'imagen_referencia.png'

# Estado del proceso de monitoreo
monitoring = False

# Función para tomar una captura de pantalla de la región especificada
def tomar_screenshot_region(left, top, width, height):
    screenshot = pyautogui.screenshot(region=(left, top, width, height))
    return screenshot

# Función para calcular el hash de la imagen
def calcular_hash_imagen(imagen):
    return imagehash.average_hash(imagen)

# Hash de la imagen de referencia
imagen_referencia = Image.open(imagen_referencia_path)
hash_imagen_referencia = calcular_hash_imagen(imagen_referencia)

# Función asíncrona para enviar mensaje de Telegram con la imagen capturada
async def enviar_mensaje_telegram(imagen, mensaje):
    imagen.save('captura.png')  # Guardar la imagen temporalmente
    with open('captura.png', 'rb') as f:
        await bot.send_photo(chat_id=chat_id, photo=f, caption=mensaje)
    print("Mensaje enviado a Telegram con la imagen capturada:", mensaje)

# Función para monitorear la pantalla
async def monitoreo():
    global hash_imagen_referencia
    while True:
        captura = tomar_screenshot_region(left, top, width, height)
        hash_captura = calcular_hash_imagen(captura)
        if hash_captura != hash_imagen_referencia:
            await enviar_mensaje_telegram(captura, "FOVISTATION")
            captura.save(imagen_referencia_path)
            hash_imagen_referencia = hash_captura
        print("Iteración de monitoreo...")
        await asyncio.sleep(10)

# Iniciar el monitoreo
async def iniciar_monitoreo():
    global monitoring
    monitoring = True
    await monitoreo()

# Iniciar el bucle de eventos asyncio
async def main():
    await iniciar_monitoreo()

# Ejecutar el bucle de eventos asyncio
asyncio.run(main())
