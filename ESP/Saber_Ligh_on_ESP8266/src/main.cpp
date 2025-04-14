#include <Arduino.h>
#include <ESP8266WiFi.h>
#include <ESP8266TrueRandom.h>

#include "Saber/api.h"
#include "Saber/poly.h"         /*  Include definizioni per lavorare con polinomi usati nell'algoritmo.*/
#include "Saber/rng.h"          /*  Include definizioni per il generatore di numeri casuali usato da SABER.*/
#include "Saber/SABER_indcpa.h" /*  Include definizioni per lo schema crittografico a chiave pubblica IND-CPA di SABER.*/
#include "Saber/verify.h"       /*  Include funzioni per la verifica delle operazioni crittografiche.*/

void setup()
{
  Serial.begin(115200); // Initialize serial communication (115200 baund standard for esp8266)
  WiFi.forceSleepBegin();

  uint8_t pk[SABER_PUBLICKEYBYTES];
  uint8_t sk[SABER_SECRETKEYBYTES];

  uint8_t c[SABER_BYTES_CCA_DEC];
  uint8_t k_a[SABER_KEYBYTES], k_b[SABER_KEYBYTES];

  uint64_t i, j;

  // Variables for measuring cpu cycles
  uint32_t CLOCK1, CLOCK2;
  uint32_t CLOCK_kp, CLOCK_enc, CLOCK_dec;

  unsigned char entropy_input[48];

  // Random Generator
  // Inizializza la libreria ESP8266TrueRandom
  randomSeed(analogRead(A0));

  for (i = 0; i < 48; i++)
  {
    entropy_input[i] = ESP8266TrueRandom.random(0, 256); // random number 0/255
  }

  randombytes_init(entropy_input, NULL, 256);

  Serial.println(F(""));
  Serial.print(F("SABER_INDCPA_PUBLICKEYBYTES="));
  Serial.println(SABER_INDCPA_PUBLICKEYBYTES);
  Serial.print(F("SABER_INDCPA_SECRETKEYBYTES="));
  Serial.println(SABER_INDCPA_SECRETKEYBYTES);
  Serial.print(F("SABER_PUBLICKEYBYTES="));
  Serial.println(SABER_PUBLICKEYBYTES);
  Serial.print(F("SABER_SECRETKEYBYTES"));
  Serial.println(SABER_SECRETKEYBYTES);
  Serial.print(F("SABER_KEYBYTES="));
  Serial.println(SABER_KEYBYTES);
  Serial.print(F("SABER_HASHBYTES="));
  Serial.println(SABER_HASHBYTES);
  Serial.print(F("SABER_BYTES_CCA_DEC="));
  Serial.print(SABER_BYTES_CCA_DEC);
  Serial.println(F(""));

  CLOCK1 = ESP.getCycleCount();
  crypto_kem_keypair(pk, sk);
  CLOCK2 = ESP.getCycleCount();
  CLOCK_kp = CLOCK2 - CLOCK1;

  delay(0);

  CLOCK1 = ESP.getCycleCount();
  crypto_kem_enc(c, k_a, pk);
  CLOCK2 = ESP.getCycleCount();

  CLOCK_enc = CLOCK2 - CLOCK1;

  CLOCK1 = ESP.getCycleCount();
  crypto_kem_dec(k_b, c, sk);
  CLOCK2 = ESP.getCycleCount();

  CLOCK_dec = CLOCK2 - CLOCK1;

  // Functional verification: check if k_a == k_b?
  for (j = 0; j < SABER_KEYBYTES; j++)
  {
    if (k_a[j] != k_b[j])
    {
      Serial.println(F("----- ERR CCA KEM ------"));
      break;
    }
  }

  delay(0);

  // Result
  Serial.println(F(""));
  Serial.print(F("Time key_pair:"));
  Serial.println(CLOCK_kp);
  Serial.print(F("Time enc:"));
  Serial.println(CLOCK_enc);
  Serial.print(F("Time dec:"));
  Serial.println(CLOCK_dec);
  
  Serial.println(F("----- END KEM SABER ------"));
}

void loop()
{
  delay(0);
}
