// Include le librerie necessarie per l'uso della scheda SD, gestione delle stringhe, comunicazione seriale e monitoraggio del consumo di corrente
#include <SD.h>
#include <string.h>
#include <SoftwareSerial.h>
#include <Adafruit_INA219.h>

// Definisce la dimensione del buffer per la lettura dei dati
#define BUFFER_SIZE 32
// Definisce il pin per il chip select dell'SD card
#define PIN_SPI_CS 4
// Pin per la comunicazione seriale software (RX e TX)
#define RX 2
#define TX 3
// Fattore di correzione della corrente misurata
#define CURRENT_CORRECTION 0.80
// Capacità della batteria in mAh (800 mAh considerando il 20% di perdita)
#define BATTERY_CAPACITY 800

// Enum per rappresentare gli stati del sistema
enum Status {
    INI,        // Inizializzazione
    LOADING,    // Caricamento dati
    RUNNING,    // Esecuzione
    ERROR       // Errore
};

// Array di stringhe per la rappresentazione testuale degli stati
const char *StatusToString[] = {"INITIALIZATION", "LOADING DATA", "RUNNING", "ERROR"};

// Variabili globali per la gestione dello stato, file e monitoraggio della corrente
Status s;
File fData, fLog;
Adafruit_INA219 eLog;
SoftwareSerial SerialBridge(RX, TX);
float simulatedBattery = BATTERY_CAPACITY; // Simulazione della batteria rimanente

// Prototipi delle funzioni
void read(char *msg);
float readNum();
void printTime(long time);
void printCurrent(float current, long time);

void setup() {
    // Imposta i pin RX e TX per la comunicazione seriale
    pinMode(RX, INPUT);
    pinMode(TX, OUTPUT);
    SerialBridge.begin(9600); // Avvia la comunicazione seriale su RX/TX
    Serial.begin(9600); // Avvia la comunicazione seriale per debug

    s = Status::INI; // Imposta lo stato iniziale

    // Inizializza il sensore INA219
    if (!eLog.begin()) {
        Serial.println(F("INA219 problem"));
        s = Status::ERROR;
    }

    // Inizializza la scheda SD e verifica l'esistenza del file "data.txt"
    if (!SD.begin(PIN_SPI_CS) || !SD.exists("data.txt")) {
        Serial.println(F("SD problem"));
        s = Status::ERROR;
    }

    // Apre il file "data.txt" per la lettura
    fData = SD.open("data.txt", FILE_READ);
    if (!fData) {
        Serial.println(F("Data problem"));
        s = Status::ERROR;
    }

    Serial.println("FINE SETUP"); // Messaggio di fine setup
}

void loop() {
    Serial.print(F("Status: "));
    Serial.println(StatusToString[s]); // Mostra lo stato corrente
    switch (s) {
        case Status::INI: { // Stato di inizializzazione
            Serial.println(F("Waiting for device startup"));
            read("INIT"); // Attende un segnale di inizializzazione
            s = Status::LOADING; // Passa allo stato di caricamento dati
            break;
        }
        case Status::LOADING: { // Stato di caricamento
            read("G"); // Legge un comando
            char buffer[BUFFER_SIZE];
            int ioNumber = (int) readNum(); // Numero di operazioni da eseguire
            int len = 0;
            char c;

            do {
                if (len > BUFFER_SIZE) {
                    s = Status::ERROR;
                    Serial.println("BufferOverflow");
                    break;
                }
                c = (char) fData.read(); // Legge caratteri dal file
                if (EOF == c) { // Se fine del file, riapre il file
                    fData.close();
                    fData = SD.open("data.txt", FILE_READ);
                    if (!fData) {
                        s = Status::ERROR;
                        Serial.println(F("Data problem"));
                        break;
                    }
                    continue;
                }
                buffer[len++] = c; // Memorizza il carattere nel buffer
                if (',' == c || '\n' == c || '\r' == c || ';' == c) { // Raggiunta la fine di un comando
                    buffer[--len] = '\0'; // Termina la stringa
                    if (len > 0) {
                        ioNumber--;
                        len = 0;
                        SerialBridge.println(buffer); // Invia il comando tramite la seriale
                        delay(10); // Ritardo per evitare sovrapposizioni
                    }
                }
            } while (ioNumber >= 0); // Continua fino a esaurimento comandi

            s = Status::RUNNING; // Passa allo stato di esecuzione
            break;
        }
        case Status::RUNNING: { // Stato di esecuzione
            read("R"); // Legge un comando
            int i = 0;
            float current = 0;
            long time = millis(); // Inizia il conteggio del tempo
            while (1) {
                i++;
                current += eLog.getCurrent_mA() - CURRENT_CORRECTION; // Accumula la corrente misurata
                if (SerialBridge.available() && 'E' == (char) SerialBridge.read()) { // Se riceve 'E', termina la misurazione
                    time = millis() - time; // Calcola il tempo trascorso
                    current = current / i; // Calcola la corrente media

                    printTime(time); // Stampa il tempo impiegato
                    printCurrent(current, time); // Stampa la corrente media e totale
                    break;
                }
            }
            // Simula il consumo della batteria in base alla corrente utilizzata
            simulatedBattery -= current * ((float) time / 3600);
            Serial.print(F("Totale mAh rimaneneti: "));
            Serial.println(simulatedBattery);
            SerialBridge.println(simulatedBattery); // Invia il dato della batteria rimanente
            s = Status::LOADING; // Torna allo stato di caricamento
            break;
        }
        default:
            delay(10000); // Se in stato non previsto, attende 10 secondi
    }
}

// Funzione per leggere un messaggio seriale
void rawRead(char *buffer) {
    for (int i = 0; i < BUFFER_SIZE; i++) {
        while (!SerialBridge.available()) {
            delay(10); // Attende la disponibilità di dati
        }

        buffer[i] = (char) SerialBridge.read(); // Legge il carattere
        if ('\n' == buffer[i] || -1 == buffer[i]) { // Se trova fine linea o -1 (mai raggiunto)
            buffer[i] = '\0'; // Termina la stringa
            break;
        }
    }
}

// Funzione per leggere un messaggio specifico dalla seriale
void read(char *msg) {
    char buffer[BUFFER_SIZE];
    while (true) {
        rawRead(buffer);
        if (strstr(buffer, msg) != nullptr) // Se trova il messaggio nel buffer, termina
            break;
    }
}

// Funzione per leggere un numero dalla seriale
float readNum() {
    char buffer[BUFFER_SIZE];
    rawRead(buffer); // Legge un numero come stringa
    return atof(buffer); // Converte la stringa in float
}

// Funzione per stampare il tempo trascorso
void printTime(long time) {
    uint32_t secs = time / 1000;
    uint32_t ms = time - (secs * 1000);

    Serial.print(F("TaskTime: "));
    Serial.print(secs);
    Serial.print(".");
    if (ms < 100) Serial.print(F("0"));
    if (ms < 10) Serial.print(F("0"));
    Serial.print(ms);
    Serial.println(F("s"));
}

// Funzione per stampare la corrente media e totale
void printCurrent(float current, long time) {
    Serial.print(F("Average Current: "));
    Serial.print(current);
    Serial.println(F("mA"));
    Serial.print(F("Total Current: "));
    Serial.print((current / ((float) time * 1000)) * 60);
    Serial.println(F("mA/min"));
}
