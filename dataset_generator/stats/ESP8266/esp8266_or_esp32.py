import matplotlib.pyplot as plt

# Dati originali (in µs) per ESP8266 LIGHT-SABER
data_light_saber = {
    10: {
        'key_pair': 18180,
        'enc': 26562,
        'dec': 30225
    },
    15: {
        'key_pair': 27273,
        'enc': 39845,
        'dec': 45339
    },
    20: {
        'key_pair': 36361,
        'enc': 53170,
        'dec': 60459
    },
    25: {
        'key_pair': 45452,
        'enc': 66466,
        'dec': 75576
    }
}

# Dati originali (in µs) per SABER
data_saber = {
    10: {
        'key_pair': 738,
        'enc': 747,
        'dec': 756
    },
    15: {
        'key_pair': 1106,
        'enc': 1111,
        'dec': 1117
    },
    20: {
        'key_pair': 1475,
        'enc': 1480,
        'dec': 1488
    },
    25: {
        'key_pair': 1832,
        'enc': 1839,
        'dec': 1854
    }
}

# Conversione da µs a secondi per ESP8266 LIGHT-SABER
for w in data_light_saber:
    data_light_saber[w]['key_pair'] /= 1e6
    data_light_saber[w]['enc'] /= 1e6
    data_light_saber[w]['dec'] /= 1e6

# Conversione da µs a secondi per SABER
for w in data_saber:
    data_saber[w]['key_pair'] /= 1e6
    data_saber[w]['enc'] /= 1e6
    data_saber[w]['dec'] /= 1e6

# Estrazione delle informazioni da visualizzare per ESP8266 LIGHT-SABER
words_light_saber = list(data_light_saber.keys())
key_pair_times_light_saber = [data_light_saber[w]['key_pair'] for w in words_light_saber]
enc_times_light_saber = [data_light_saber[w]['enc'] for w in words_light_saber]
dec_times_light_saber = [data_light_saber[w]['dec'] for w in words_light_saber]

# Estrazione delle informazioni da visualizzare per SABER
words_saber = list(data_saber.keys())
key_pair_times_saber = [data_saber[w]['key_pair'] for w in words_saber]
enc_times_saber = [data_saber[w]['enc'] for w in words_saber]
dec_times_saber = [data_saber[w]['dec'] for w in words_saber]

# Creazione del grafico
plt.figure(figsize=(10, 6))

# Grafico per ESP8266 LIGHT-SABER
plt.plot(words_light_saber, key_pair_times_light_saber, label="Light-Saber Key Pair Time", marker='o', color='blue')
plt.plot(words_light_saber, enc_times_light_saber, label="Light-Saber Encryption Time", marker='o', color='green')
plt.plot(words_light_saber, dec_times_light_saber, label="Light-Saber Decryption Time", marker='o', color='red')

# Grafico per SABER
plt.plot(words_saber, key_pair_times_saber, label="SABER Key Pair Time", marker='o', color='cyan', linestyle='--')
plt.plot(words_saber, enc_times_saber, label="SABER Encryption Time", marker='o', color='lime', linestyle='--')
plt.plot(words_saber, dec_times_saber, label="SABER Decryption Time", marker='o', color='magenta', linestyle='--')

# Annotazioni per ogni punto (opzionali)
for i, txt in enumerate(key_pair_times_light_saber):
    plt.annotate(f'{txt:.6f} s', (words_light_saber[i], key_pair_times_light_saber[i]), textcoords="offset points", xytext=(0,10), ha='center')

for i, txt in enumerate(enc_times_light_saber):
    plt.annotate(f'{txt:.6f} s', (words_light_saber[i], enc_times_light_saber[i]), textcoords="offset points", xytext=(0,10), ha='center')

for i, txt in enumerate(dec_times_light_saber):
    plt.annotate(f'{txt:.6f} s', (words_light_saber[i], dec_times_light_saber[i]), textcoords="offset points", xytext=(0,10), ha='center')

# Aggiunta dei dettagli del grafico
plt.title("Comparison of Total Time per Operation (s)")
plt.xlabel('Number of Words (W)')
plt.ylabel('Time (s)')
plt.legend()
plt.grid(True)

# Visualizzazione del grafico
plt.show()
