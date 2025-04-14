import matplotlib.pyplot as plt

# Dati originali LIGHT-SABER (in µs)
light_saber_data = {
    50: {
        'key_pair': 2621,
        'enc': 2750,
        'dec': 2826
    },
    100: {
        'key_pair': 5248,
        'enc': 5513,
        'dec': 5627
    },
    200: {
        'key_pair': 10463,
        'enc': 10997,
        'dec': 11241
    },
    400: {
        'key_pair': 21908,
        'enc': 21924,
        'dec': 22498
    }
}

# Conversione da µs a secondi
for w in light_saber_data:
    light_saber_data[w]['key_pair'] /= 1e6
    light_saber_data[w]['enc'] /= 1e6
    light_saber_data[w]['dec'] /= 1e6

# Estrazione delle informazioni da visualizzare
words = list(light_saber_data.keys())
light_saber_key_pair_times = [light_saber_data[w]['key_pair'] for w in words]
light_saber_enc_times = [light_saber_data[w]['enc'] for w in words]
light_saber_dec_times = [light_saber_data[w]['dec'] for w in words]

# Creazione del grafico
plt.figure(figsize=(10, 6))

# Plot per LIGHT-SABER
plt.plot(words, light_saber_key_pair_times, label="LIGHT-SABER Key Pair Time", marker='o', color='blue')
plt.plot(words, light_saber_enc_times, label="LIGHT-SABER Encryption Time", marker='o', color='green')
plt.plot(words, light_saber_dec_times, label="LIGHT-SABER Decryption Time", marker='o', color='red')



# Aggiunta dei dettagli del grafico
plt.title("LIGHT-SABER: Total Time per Operation (s)")
plt.xlabel('Number of Words')
plt.ylabel('Time (s)')
plt.legend()
plt.grid(True)

# Visualizzazione del grafico
plt.show()
