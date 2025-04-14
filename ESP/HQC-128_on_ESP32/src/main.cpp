#include <Arduino.h>
#include <stdio.h>

#include "hqc-128/api.h"
#include "hqc-128/parameters.h"


unsigned char pk[PUBLIC_KEY_BYTES];
unsigned char sk[SECRET_KEY_BYTES];
unsigned char ct[CIPHERTEXT_BYTES];
unsigned char key1[SHARED_SECRET_BYTES];
unsigned char key2[SHARED_SECRET_BYTES];

// Variables for measuring cpu cycles
uint32_t CLOCK1, CLOCK2;
uint32_t CLOCK_kp, CLOCK_enc, CLOCK_dec;

// Dichiarazione delle code
QueueHandle_t keypairQueue;
QueueHandle_t encryptionQueue;

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
        crypto_kem_enc(ct, key1, pk);
        xQueueSend(encryptionQueue, ct, portMAX_DELAY);
        xQueueSend(encryptionQueue, key1, portMAX_DELAY);
        xQueueSend(encryptionQueue, pk, portMAX_DELAY);

    }
    vTaskDelete(NULL); // cancello il task chiamante
}

// Funzione del task per la decifratura
void taskDecrypt(void *pvParameters)
{
    if (xQueueReceive(encryptionQueue, ct, portMAX_DELAY) == pdTRUE)
    {
        xQueueReceive(keypairQueue, sk, portMAX_DELAY);
        crypto_kem_dec(key2, ct, sk);
    }
    vTaskDelete(NULL);
}

void setup() {

    Serial.begin(115200);

	keypairQueue = xQueueCreate(2, sizeof(uint8_t) * PUBLIC_KEY_BYTES);
    encryptionQueue = xQueueCreate(2, sizeof(uint8_t) * CIPHERTEXT_BYTES);

    Serial.println();
    Serial.println("*********************");
    Serial.printf("**** HQC-%d-%d ****\n", PARAM_SECURITY, PARAM_DFR_EXP);
    Serial.println("*********************");

    Serial.println();
    Serial.printf("N: %d   ", PARAM_N);
    Serial.printf("N1: %d   ", PARAM_N1);
    Serial.printf("N2: %d   ", PARAM_N2);
    Serial.printf("OMEGA: %d   ", PARAM_OMEGA);
    Serial.printf("OMEGA_R: %d   ", PARAM_OMEGA_R);
    Serial.printf("Failure rate: 2^-%d   ", PARAM_DFR_EXP);
    Serial.printf("Sec: %d bits", PARAM_SECURITY);
    Serial.println();


	 if (keypairQueue == NULL || encryptionQueue == NULL )
    {
        Serial.println("Failed to create queue");
        return;
    }

    CLOCK1 = ESP.getCycleCount();
	xTaskCreate(taskKeypair, "KeypairTask", 16000, NULL, 1, NULL);
    CLOCK2 = ESP.getCycleCount();

    CLOCK_kp = CLOCK2 - CLOCK1;

    CLOCK1 = ESP.getCycleCount();
	xTaskCreate(taskEncrypt, "EncryptTask", 30000, NULL, 1, NULL); //testare da 24000
    CLOCK2 = ESP.getCycleCount();

    CLOCK_enc = CLOCK2 - CLOCK1;

	CLOCK1 = ESP.getCycleCount();
	xTaskCreate(taskDecrypt, "DecryptTask", 38000, NULL, 1, NULL);
    CLOCK2 = ESP.getCycleCount();

    CLOCK_dec = CLOCK2 - CLOCK1;

    // Result
    Serial.println("");
    Serial.print("Cycle Count key_pair:");
    Serial.println(CLOCK_kp);
    Serial.print("Cycle Count enc:");
    Serial.println(CLOCK_enc);
    Serial.print("Cycle Count dec:");
    Serial.println(CLOCK_dec);

	}

void loop() {
  // put your main code here, to run repeatedly:
}
