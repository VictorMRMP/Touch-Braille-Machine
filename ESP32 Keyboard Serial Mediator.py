import serial
from pynput.keyboard import Controller, Key
import time
import os
import pygame

# Configuração da porta serial
SERIAL_PORT = 'COM19'  # Ajuste para sua porta
BAUD_RATE = 9600
keyboard = Controller()  # Controlador de teclado

# Caminho dos arquivos de áudio
AUDIO_FOLDER = r"D:\Usp\Touch Display\Maquina Braille Touch\audios"  # Altere para o diretório correto dos arquivos WAV

# Inicializa o mixer do Pygame para reprodução de áudio
pygame.mixer.init()

# Função para tocar um arquivo de áudio
def play_audio(file_path):
    if os.path.exists(file_path):
        pygame.mixer.music.load(file_path)
        pygame.mixer.music.play()
    else:
        print(f"Arquivo não encontrado: {file_path}")

# Conectando à porta serial
try:
    serial_connection = serial.Serial(SERIAL_PORT, BAUD_RATE, timeout=1)
    print(f"Conectado à porta {SERIAL_PORT}")
except Exception as e:
    print(f"Erro ao conectar na porta serial: {e}")
    exit()

# Função para transformar entrada serial em teclas e tocar o áudio correspondente
def serial_to_keyboard(data):
    # Mapear as entradas específicas da serial para teclas do teclado
    audio_file = None
    if data == "32":  # Código ASCII para espaço
        keyboard.press(Key.space)
        keyboard.release(Key.space)
        audio_file = "espaco.wav"  # Nome do arquivo WAV correspondente
    elif data == "10":  # Código ASCII para Enter
        keyboard.press(Key.enter)
        keyboard.release(Key.enter)
        audio_file = "nova_linha.wav"  # Nome do arquivo WAV correspondente
    elif data == "127":  # Código ASCII para Delete
        keyboard.press(Key.backspace)
        keyboard.release(Key.backspace)
    elif data == "25":  # Exemplo de Ctrl+Y para mover para cima
        keyboard.press(Key.up)
        keyboard.release(Key.up)
    elif data == "26":  # Exemplo de Ctrl+Z para mover para baixo
        keyboard.press(Key.down)
        keyboard.release(Key.down)
    elif data.isalpha() or data.isdigit():  # Letras e números
        keyboard.press(data)
        keyboard.release(data)
        audio_file = f"{data.upper()}.wav" if data.isalpha() else f"{data}.wav"
    else:
        print(f"Comando não mapeado: {data}")
    
    # Reproduz o áudio correspondente ao caractere
    if audio_file:
        play_audio(os.path.join(AUDIO_FOLDER, audio_file))

# Loop principal para ler da serial e enviar para o teclado
try:
    while True:
        if serial_connection.in_waiting > 0:
            # Leitura do dado serial
            data = serial_connection.readline().decode('utf-8').strip()
            print(f"Dado recebido: {data}")
            serial_to_keyboard(data)  # Envia o dado como teclado e toca o som correspondente
        time.sleep(0.1)
except KeyboardInterrupt:
    print("Encerrando o programa.")
finally:
    serial_connection.close()
