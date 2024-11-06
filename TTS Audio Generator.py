from gtts import gTTS
import os
from pydub import AudioSegment

# Caminho da pasta para salvar os arquivos de áudio
output_folder = r"D:\Usp\Touch Display\Maquina Braille Touch\audios2"
os.makedirs(output_folder, exist_ok=True)  # Cria a pasta se não existir

# Mapeia caracteres para nomes de arquivo válidos e texto a ser falado
characters = {
    ' ': ('espaco', "espaço"),
    '\n': ('nova_linha', "nova linha"),
    'a': ('A', 'a'),
    'b': ('B', 'b'),
    'c': ('C', 'c'),
    'd': ('D', 'd'),
    'e': ('E', 'e'),
    'f': ('F', 'f'),
    'g': ('G', 'g'),
    'h': ('H', 'h'),
    'i': ('I', 'i'),
    'j': ('J', 'j'),
    'k': ('K', 'k'),
    'l': ('L', 'l'),
    'm': ('M', 'm'),
    'n': ('N', 'n'),
    'o': ('O', 'o'),
    'p': ('P', 'p'),
    'q': ('Q', 'q'),
    'r': ('R', 'r'),
    's': ('S', 's'),
    't': ('T', 't'),
    'u': ('U', 'u'),
    'v': ('V', 'v'),
    'w': ('W', 'w'),
    'x': ('X', 'x'),
    'y': ('Y', 'y'),
    'z': ('Z', 'z'),
    '0': ('0', 'zero'),
    '1': ('1', 'um'),
    '2': ('2', 'dois'),
    '3': ('3', 'três'),
    '4': ('4', 'quatro'),
    '5': ('5', 'cinco'),
    '6': ('6', 'seis'),
    '7': ('7', 'sete'),
    '8': ('8', 'oito'),
    '9': ('9', 'nove'),
    ',': ('virgula', 'vírgula'),
    '.': ('ponto', 'ponto'),
    '!': ('exclamacao', 'exclamação'),
    '?': ('interrogacao', 'interrogação'),
    '-': ('hifen', 'hífen'),
    '/': ('barra', 'barra'),
    '*': ('asterisco', 'asterisco'),
    '"': ('aspas', 'aspas'),
    '@': ('arroba', 'arroba'),
    '&': ('e_comercial', 'e comercial'),
}

# Função para gerar e salvar áudio de cada caractere em MP3
def generate_audio_files_mp3(characters, output_folder):
    for char, (filename, text_to_speak) in characters.items():
        audio = gTTS(text=text_to_speak, lang='pt', slow=False)  # Gera o áudio
        mp3_file = os.path.join(output_folder, f"{filename}.mp3")  # Define o nome do arquivo
        audio.save(mp3_file)  # Salva o arquivo
        print(f"Arquivo MP3 salvo para '{char}' como {mp3_file}")

# Função para converter MP3 para WAV
def convert_mp3_to_wav(output_folder):
    for file in os.listdir(output_folder):
        if file.endswith(".mp3"):
            mp3_file = os.path.join(output_folder, file)
            wav_file = os.path.join(output_folder, file[:-4] + ".wav")  # Remove .mp3 e adiciona .wav
            try:
                sound = AudioSegment.from_mp3(mp3_file)  # Carrega o MP3
                sound.export(wav_file, format="wav")  # Salva como WAV
                print(f"Arquivo WAV salvo como {wav_file}")
                os.remove(mp3_file)  # Remove o MP3 se não for mais necessário
            except Exception as e:
                print(f"Erro ao converter {mp3_file} para WAV: {e}")

# Gera os arquivos de áudio em MP3
generate_audio_files_mp3(characters, output_folder)

# Converte os arquivos MP3 gerados para WAV
convert_mp3_to_wav(output_folder)
