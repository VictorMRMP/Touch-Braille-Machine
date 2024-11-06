#include <map>
#include <BleKeyboard.h>

BleKeyboard bleKeyboard("ESP32 Keyboard", "Espressif", 100);

// Definir os pinos que serão usados para as células touch
const int touchPins[] = {14, 33, 35, 18, 21, 34};  // Pinos das células touch para Braille
const int pinEspaco = 23;  // Pino para comando de espaço
const int auxPins[] = {16, 4};  // Pino para comandos auxiliares

// Mapeamento de Braille para letras, sinais de pontuação e números
std::map<int, uint8_t> braille_map = {
    {0b100000, 0x61},  // 'a' ASCII
    {0b101000, 0x62},  // 'b' ASCII
    {0b110000, 0x63},  // 'c' ASCII
    {0b110100, 0x64},  // 'd' ASCII
    {0b100100, 0x65},  // 'e' ASCII
    {0b111000, 0x66},  // 'f' ASCII
    {0b111100, 0x67},  // 'g' ASCII
    {0b101100, 0x68},  // 'h' ASCII
    {0b011000, 0x69},  // 'i' ASCII
    {0b011100, 0x6A},  // 'j' ASCII
    {0b100010, 0x6B},  // 'k' ASCII
    {0b101010, 0x6C},  // 'l' ASCII
    {0b110010, 0x6D},  // 'm' ASCII
    {0b110110, 0x6E},  // 'n' ASCII
    {0b100110, 0x6F},  // 'o' ASCII
    {0b111010, 0x70},  // 'p' ASCII
    {0b111110, 0x71},  // 'q' ASCII
    {0b101110, 0x72},  // 'r' ASCII
    {0b011010, 0x73},  // 's' ASCII
    {0b011110, 0x74},  // 't' ASCII
    {0b100011, 0x75},  // 'u' ASCII
    {0b101011, 0x76},  // 'v' ASCII
    {0b011101, 0x77},  // 'w' ASCII
    {0b110011, 0x78},  // 'x' ASCII
    {0b110111, 0x79},  // 'y' ASCII
    {0b100111, 0x7A},  // 'z' ASCII
    {0b000001, 0x27},  // '\'' ASCII
    {0b001010, 0x2C},  // ',' ASCII
    {0b001011, 0x3B},  // ';' ASCII
    {0b001110, 0x3A},  // ':' ASCII
    {0b001100, 0x2E},  // '.' ASCII
    {0b001101, 0x21},  // '!' ASCII
    {0b001001, 0x3F},  // '?' ASCII
    {0b010011, 0x2D},  // '-' ASCII
    {0b011011, 0x2F},  // '/' ASCII
    {0b010111, 0x2A},  // '*' ASCII
    {0b010101, 0x22},  // '"' ASCII
    {0b010010, 0x40},  // '@' ASCII
    {0b001101, 0x26},  // '&' ASCII
    {0b000011, 0xE1},  // Prefixo de letra maiúscula (Shift)
    {0b000010, 0},     // Prefixo de número
};

std::map<int, int> aux_map = {
    {0b01, KEY_DOWN_ARROW},
    {0b10, KEY_UP_ARROW},
    {0b11, KEY_BACKSPACE},
};

// Controle de estado
bool useShift = false;
bool useNumber = false;
unsigned long lastReadingTime = 0;
const unsigned long readingDelay = 500;

uint8_t braille_to_letter(int braille_code) {
    auto it = braille_map.find(braille_code);
    return (it != braille_map.end()) ? it->second : 0;
}

uint8_t braille_to_number(int braille_code) {
    return (braille_code >= 0b100000 && braille_code <= 0b100111) ? (braille_code - 0b100000 + 0x31) : 0; // '1' a '9'
}

void setup() {
    Serial.begin(9600);
    for (int pin : touchPins) {
        pinMode(pin, INPUT_PULLDOWN);
    }
    pinMode(pinEspaco, INPUT_PULLDOWN);
    for (int pin : auxPins) {
        pinMode(pin, INPUT_PULLDOWN);
    }
    bleKeyboard.begin();
}

void send_data(uint8_t output) {
    if (bleKeyboard.isConnected()) {
        bleKeyboard.write(output); // Envia via Bluetooth
    } else {
        Serial.write(output);      // Envia via Serial
    }
}

void loop() {
    int braille = 0;
    int aux = 0;

    // Verificar as 6 células para Braille
    for (int i = 0; i < 6; i++) {
        if (digitalRead(touchPins[i]) == HIGH) {
            delay(10);
            braille |= (1 << i);
        }
    }

    // Verificar os comandos auxiliares
    for (int i = 0; i < 2; i++) {
        if (digitalRead(auxPins[i]) == HIGH) {
            delay(10);
            aux |= (1 << i);
        }
    }

    // Processar entrada Braille
    if (braille > 0 && millis() - lastReadingTime > readingDelay) {
        lastReadingTime = millis();
        if (braille == 0b000011) {
            useShift = true;  // Shift para maiúscula
        } else if (braille == 0b000010) {
            useNumber = true; // Prefixo de número
        } else {
            uint8_t output;
            if (useNumber) {
                output = braille_to_number(braille);
                useNumber = false; // Desativa após leitura
            } else {
                output = braille_to_letter(braille);
                if (useShift) {
                    output -= 32; // Converte para maiúscula
                    useShift = false; // Desativa após leitura
                }
            }
            if (output) {
                send_data(output); // Envia o dado via Bluetooth ou Serial
            }
        }
    }

    // Comando auxiliar
    if (aux > 0) {
        int command = aux_map[aux];
        if (command) {
            send_data(command); // Envia o comando via Bluetooth ou Serial
            delay(200);
        }
    }

    // Espaço
    if (digitalRead(pinEspaco) == HIGH) {
        send_data(' '); // Envia espaço via Bluetooth ou Serial
        delay(200);
    }

    delay(200); // Pequeno delay para evitar múltiplas leituras
}
