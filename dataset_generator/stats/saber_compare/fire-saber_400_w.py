import matplotlib.pyplot as plt

# Dati originali Fire-Saber (in µs)
fire_saber_data = {
    50: {
        'key_pair': 4235,
        'enc': 4235,
        'dec': 4576
    },
    100: {
        'key_pair': 8464,
        'enc': 8488,
        'dec': 9131
    },
    200: {
        'key_pair': 17937,
        'enc': 16982,
        'dec': 18268
    },
    400: {
        'key_pair': 35865,
        'enc': 33969,
        'dec': 36560
    }
}

# Conversione da µs a secondi
for w in fire_saber_data:
    fire_saber_data[w]['key_pair'] /= 1e6
    fire_saber_data[w]['enc'] /= 1e6
    fire_saber_data[w]['dec'] /= 1e6

# Estrazione delle informazioni da visualizzare
words = list(fire_saber_data.keys())
fire_saber_key_pair_times = [fire_saber_data[w]['key_pair'] for w in words]
fire_saber_enc_times = [fire_saber_data[w]['enc'] for w in words]
fire_saber_dec_times = [fire_saber_data[w]['dec'] for w in words]

# Creazione del grafico
plt.figure(figsize=(10, 6))

# Plot per Fire-Saber
plt.plot(words, fire_saber_key_pair_times, label="Fire-Saber Key Pair Time", marker='o', color='blue')
plt.plot(words, fire_saber_enc_times, label="Fire-Saber Encryption Time", marker='o', color='green')
plt.plot(words, fire_saber_dec_times, label="Fire-Saber Decryption Time", marker='o', color='red')



# Aggiunta dei dettagli del grafico
plt.title("Fire-Saber: Total Time per Operation (s)")
plt.xlabel('Number of Words')
plt.ylabel('Time (s)')
plt.legend()
plt.grid(True)

# Visualizzazione del grafico
plt.show()
