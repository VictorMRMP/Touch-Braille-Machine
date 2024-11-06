import customtkinter
import serial
import os
import pygame

# Inicializa o mixer do Pygame
pygame.mixer.init()

# Função para tocar um arquivo de áudio
def play_audio(file_path):
    if os.path.exists(file_path):
        pygame.mixer.music.load(file_path)
        pygame.mixer.music.play()
    else:
        print(f"Arquivo não encontrado: {file_path}")

# Função para ler dados da porta serial
def read_serial_data(serial_connection):
    if serial_connection.in_waiting > 0:
        try:
            data = serial_connection.readline().decode('utf-8').strip()
            return data
        except Exception as e:
            print(f"Erro de leitura serial: {e}")
    return None

# Função para processar letras e comandos recebidos via serial
def process_serial_input(serial_connection, message_textbox):
    data = read_serial_data(serial_connection)
    if data:
        if data == "ultimap":
            speak_last_word(message_textbox)
        elif data == "ultimaf":
            speak_all_text(message_textbox)
        elif data == "apagarl":
            delete_last_letter(message_textbox)
        elif data == "espaco":
            message_textbox.insert("end", " ")  # Adiciona um espaço
            play_audio(os.path.join("D:\\Usp\\Touch Display\\Maquina Braille Touch\\audios", "apostrofo.mp3"))  # Toca o áudio para espaço
        elif data == "linhab":
            message_textbox.insert("end", "\n")  # Pula para a linha de baixo
            play_audio(os.path.join("D:\\Usp\\Touch Display\\Maquina Braille Touch\\audios", "virgula.mp3"))  # Toca o áudio para linha abaixo
        elif data == "linhac":
            move_cursor_up(message_textbox)  # Volta para a linha de cima
        else:
            message_textbox.insert("end", data)  # Insere a letra ou comando no editor de texto
            
            # Toca o áudio correspondente à letra recebida
            if data.isalpha() and len(data) == 1:  # Se for uma letra
                audio_file = f"{data.upper()}.mp3"  # Nome do arquivo em maiúsculas
            elif data == ",":
                audio_file = "virgula.mp3"
            elif data == ".":
                audio_file = "ponto.mp3"
            elif data == "!":
                audio_file = "exclamacao.mp3"
            elif data == "?":
                audio_file = "interrogacao.mp3"
            elif data == "-":
                audio_file = "hifen.mp3"
            elif data == "/":
                audio_file = "barra.mp3"
            elif data == "*":
                audio_file = "asterisco.mp3"
            elif data == '"':
                audio_file = "aspas.mp3"
            elif data == "@":
                audio_file = "arroba.mp3"
            elif data == "&":
                audio_file = "e_comercial.mp3"
            else:
                audio_file = None  # Nenhum arquivo correspondente

            # Toca o arquivo de áudio, se existir
            if audio_file:
                play_audio(os.path.join("D:\\Usp\\Touch Display\\Maquina Braille Touch\\audios", audio_file))

# Função para falar a última palavra escrita
def speak_last_word(message_textbox):
    text = message_textbox.get("1.0", "end-1c")
    words = text.split()
    if words:
        play_audio(os.path.join("D:\\Usp\\Touch Display\\Maquina Braille Touch\\audios", f"{words[-1].upper()}.mp3"))
    else:
        play_audio(os.path.join("D:\\Usp\\Touch Display\\Maquina Braille Touch\\audios", "nenhuma_palavra.mp3"))

# Função para falar todo o texto escrito
def speak_all_text(message_textbox):
    text = message_textbox.get("1.0", "end-1c")
    if text:
        play_audio(os.path.join("D:\\Usp\\Touch Display\\Maquina Braille Touch\\audios", "texto_completo.mp3"))
    else:
        play_audio(os.path.join("D:\\Usp\\Touch Display\\Maquina Braille Touch\\audios", "nenhum_texto.mp3"))

# Função para apagar a última letra escrita
def delete_last_letter(message_textbox):
    text = message_textbox.get("1.0", "end-1c")
    if text:
        message_textbox.delete("end-2c", "end-1c")  # Remove a última letra
        play_audio(os.path.join("D:\\Usp\\Touch Display\\Maquina Braille Touch\\audios", "ultima_letra_apagada.mp3"))
    else:
        play_audio(os.path.join("D:\\Usp\\Touch Display\\Maquina Braille Touch\\audios", "nenhuma_letra.mp3"))

# Função para voltar para a linha de cima
def move_cursor_up(message_textbox):
    try:
        current_index = message_textbox.index("insert")
        line, column = map(int, current_index.split('.'))
        if line > 1:
            new_index = f"{line - 1}.{column}"
            message_textbox.mark_set("insert", new_index)
            play_audio(os.path.join("D:\\Usp\\Touch Display\\Maquina Braille Touch\\audios", "voltando_linha.mp3"))
        else:
            play_audio(os.path.join("D:\\Usp\\Touch Display\\Maquina Braille Touch\\audios", "nao_hay_linha_acima.mp3"))
    except Exception as e:
        print(f"Erro ao mover cursor para cima: {e}")
        play_audio(os.path.join("D:\\Usp\\Touch Display\\Maquina Braille Touch\\audios", "erro_voltar_linha.mp3"))

# Função para configurar a interface gráfica
def setup_gui(serial_connection):
    root = customtkinter.CTk()
    root.geometry("800x600")
    root.title("Editor de Texto Serial")

    # Frame principal para o editor de texto
    frame = customtkinter.CTkFrame(master=root)
    frame.pack(padx=20, pady=20, fill="both", expand=True)

    # Caixa de texto onde as letras recebidas aparecerão
    message_textbox = customtkinter.CTkTextbox(master=frame, height=300, width=400)
    message_textbox.pack(pady=12, padx=10)

    # Função para atualizar as letras recebidas via serial
    def update_serial_data():
        process_serial_input(serial_connection, message_textbox)
        root.after(100, update_serial_data)  # Atualiza a cada 100 ms

    root.after(100, update_serial_data)  # Inicia o loop de verificação da porta serial

    return root

# Função principal
def main():
    # Inicialização da porta serial (ajuste a porta e baudrate conforme necessário)
    serial_port = 'COM19'  # Exemplo de porta (ajustar para o seu sistema)
    baud_rate = 9600
    try:
        serial_connection = serial.Serial(serial_port, baud_rate, timeout=1)
        print(f"Conectado à porta {serial_port}")
    except Exception as e:
        print(f"Erro ao conectar na porta serial: {e}")
        return

    root = setup_gui(serial_connection)
    root.mainloop()

if __name__ == "__main__":
    main()
