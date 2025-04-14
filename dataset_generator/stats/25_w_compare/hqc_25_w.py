import matplotlib.pyplot as plt

# Dati originali (in µs)
data = {
    10: {
        'key_pair': 923,
        'enc': 1181,
        'dec': 1020
    },
    15: {
        'key_pair': 1391,
        'enc': 1764,
        'dec': 1525
    },
    20: {
        'key_pair': 1844,
        'enc': 2344,
        'dec': 2047
    },
    25: {
        'key_pair': 2290,
        'enc': 2930,
        'dec': 2543
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

# Annotazioni per ogni punto
for i, txt in enumerate(key_pair_times):
    plt.annotate(f'{txt:.6f} s', (words[i], key_pair_times[i]), textcoords="offset points", xytext=(0,10), ha='center')
for i, txt in enumerate(enc_times):
    plt.annotate(f'{txt:.6f} s', (words[i], enc_times[i]), textcoords="offset points", xytext=(0,10), ha='center')
for i, txt in enumerate(dec_times):
    plt.annotate(f'{txt:.6f} s', (words[i], dec_times[i]), textcoords="offset points", xytext=(0,10), ha='center')

# Aggiunta dei dettagli del grafico
plt.title("HQC 128: Total Time per Operation (s)")
plt.xlabel('Number of Words')
plt.ylabel('Time (s)')
plt.legend()
plt.grid(True)

# Visualizzazione del grafico
plt.show()
