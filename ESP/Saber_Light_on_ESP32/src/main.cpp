#include <Arduino.h>
#include <esp_random.h>

#include "Saber/api.h"
#include "Saber/poly.h"
#include "Saber/rng.h"
#include "Saber/SABER_indcpa.h"
#include "Saber/verify.h"
#include "Saber/SABER_params.h"

uint8_t pk[SABER_PUBLICKEYBYTES];
uint8_t sk[SABER_SECRETKEYBYTES];
uint8_t c[SABER_BYTES_CCA_DEC];
uint8_t k_a[SABER_KEYBYTES];
uint8_t k_b[SABER_KEYBYTES];

// Variables for measuring cpu cycles
uint32_t CLOCK1, CLOCK2;
uint32_t CLOCK_kp, CLOCK_enc, CLOCK_dec;

// Random Generator
unsigned char entropy_input[48];

// Dichiarazione delle code
QueueHandle_t keypairQueue;
QueueHandle_t encryptionQueue;
QueueHandle_t decryptionQueue;

// Funzione del task per la generazione delle chiavi
void taskKeypair(void *pvParameters)
{
    crypto_kem_keypair(pk, sk);
    xQueueSend(keypairQueue, pk, portMAX_DELAY);
    xQueueSend(keypairQueue, sk, portMAX_DELAY);
    vTaskDelete(NULL);
}

// Funzione del task per la cifratura
void taskEncrypt(void *pvParameters)
{
    if (xQueueReceive(keypairQueue, pk, portMAX_DELAY) == pdTRUE)
    {
        crypto_kem_enc(c, k_a, pk);
        xQueueSend(encryptionQueue, c, portMAX_DELAY);
        xQueueSend(encryptionQueue, k_a, portMAX_DELAY);
    }
    vTaskDelete(NULL); // cancello il task chiamante
}

// Funzione del task per la decifratura
void taskDecrypt(void *pvParameters)
{
    if (xQueueReceive(encryptionQueue, c, portMAX_DELAY) == pdTRUE)
    {
        xQueueReceive(keypairQueue, sk, portMAX_DELAY);
        crypto_kem_dec(k_b, c, sk);
        xQueueSend(decryptionQueue, k_b, portMAX_DELAY);
    }
    vTaskDelete(NULL);
}

// Funzione del task per la verifica
void taskVerify(void *pvParameters)
{
    if (xQueueReceive(decryptionQueue, k_b, portMAX_DELAY) == pdTRUE)
    {
        // Functional verification: check if k_a == k_b
        for (int j = 0; j < SABER_KEYBYTES; j++)
        {
            if (k_a[j] != k_b[j])
            {
                Serial.println("----- ERR CCA KEM ------");
                break;
            }
        }

        Serial.println("----- END KEM SABER ------");
    }
    vTaskDelete(NULL);
}

void setup()
{
    Serial.begin(115200);

    // Creazione delle code
    keypairQueue = xQueueCreate(2, sizeof(uint8_t) * SABER_PUBLICKEYBYTES);
    encryptionQueue = xQueueCreate(2, sizeof(uint8_t) * SABER_BYTES_CCA_DEC);
    decryptionQueue = xQueueCreate(2, sizeof(uint8_t) * SABER_KEYBYTES);

    if (keypairQueue == NULL || encryptionQueue == NULL || decryptionQueue == NULL)
    {
        Serial.println("Failed to create queue");
        return;
    }

    for (int i = 0; i < 48; i++)
    {
        // entropy_input[i] = i;
        entropy_input[i] = (esp_random()) % 256;
    }
    randombytes_init(entropy_input, NULL, 256);

    Serial.println("");
    Serial.print("SABER_INDCPA_PUBLICKEYBYTES=");
    Serial.println(SABER_INDCPA_PUBLICKEYBYTES);
    Serial.print("SABER_INDCPA_SECRETKEYBYTES=");
    Serial.println(SABER_INDCPA_SECRETKEYBYTES);
    Serial.print("SABER_PUBLICKEYBYTES=");
    Serial.println(SABER_PUBLICKEYBYTES);
    Serial.print("SABER_SECRETKEYBYTES");
    Serial.println(SABER_SECRETKEYBYTES);
    Serial.print("SABER_KEYBYTES=");
    Serial.println(SABER_KEYBYTES);
    Serial.print("SABER_HASHBYTES=");
    Serial.println(SABER_HASHBYTES);
    Serial.print("SABER_BYTES_CCA_DEC=");
    Serial.print(SABER_BYTES_CCA_DEC);
    Serial.println("");

    // Creazione dei task

    CLOCK1 = ESP.getCycleCount();
    xTaskCreate(taskKeypair, "KeypairTask", 10000, NULL, 1, NULL);
    CLOCK2 = ESP.getCycleCount();

    CLOCK_kp = CLOCK2 - CLOCK1;

    CLOCK1 = ESP.getCycleCount();
    xTaskCreate(taskEncrypt, "EncryptTask", 12000, NULL, 1, NULL);
    CLOCK2 = ESP.getCycleCount();

    CLOCK_enc = CLOCK2 - CLOCK1;

    CLOCK1 = ESP.getCycleCount();
    xTaskCreate(taskDecrypt, "DecryptTask", 13000, NULL, 1, NULL);
    CLOCK2 = ESP.getCycleCount();

    CLOCK_dec = CLOCK2 - CLOCK1;

    //xTaskCreate(taskVerify, "VerifyTask", 8192, NULL, 1, NULL);
    xTaskCreate(taskVerify, "VerifyTask", 4192, NULL, 1, NULL);


    // Result
    Serial.println("");
    Serial.print("Cycle Count key_pair:");
    Serial.println(CLOCK_kp);
    Serial.print("Cycle Count enc:");
    Serial.println(CLOCK_enc);
    Serial.print("Cycle Count dec:");
    Serial.println(CLOCK_dec);
}

void loop()
{
    // Il loop principale può rimanere vuoto o gestire altre operazioni
}
