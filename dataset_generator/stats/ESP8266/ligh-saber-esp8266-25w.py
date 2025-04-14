import matplotlib.pyplot as plt

# Dati originali (in µs)
data = {
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



# Conversione da µs a secondi
for w in data:
    data[w]['key_pair'] /= 1e6
    data[w]['enc'] /= 1e6
    data[w]['dec'] /= 1e6

# Estrazione delle informazioni da visualizzare
words = list(data.keys())
key_pair_times = [data[w]['key_pair'] for w in words]
enc_times = [data[w]['enc'] for w in words]
dec_times = [data[w]['dec'] for w in words]

# Creazione del grafico
plt.figure(figsize=(10, 6))

plt.plot(words, key_pair_times, label="Key Pair Time", marker='o', color='blue')
plt.plot(words, enc_times, label="Encryption Time", marker='o', color='green')
plt.plot(words, dec_times, label="Decryption Time", marker='o', color='red')

# Annotazioni per ogni punto (opzionali)
for i, txt in enumerate(key_pair_times):
    plt.annotate(f'{txt:.6f} s', (words[i], key_pair_times[i]), textcoords="offset points", xytext=(0,10), ha='center')
for i, txt in enumerate(enc_times):
    plt.annotate(f'{txt:.6f} s', (words[i], enc_times[i]), textcoords="offset points", xytext=(0,10), ha='center')
for i, txt in enumerate(dec_times):
   plt.annotate(f'{txt:.6f} s', (words[i], dec_times[i]), textcoords="offset points", xytext=(0,10), ha='center')

# Aggiunta dei dettagli del grafico
plt.title("ESP8266 LIGHT-SABER: Total Time per Operation (s)")
plt.xlabel('Number of Words (W)')
plt.ylabel('Time (s)')
plt.legend()
plt.grid(True)

# Visualizzazione del grafico
plt.show()
