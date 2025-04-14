import matplotlib.pyplot as plt

# Dati originali (in µs)
data = {
    10: {
        'key_pair': 10423155,
        'enc': 4725,
        'sign': 2852552
    },
    15: {
        'key_pair': 14795455,
        'enc': 7101,
        'sign': 4280055
    },
    20: {
        'key_pair': 19167724,
        'enc': 9480,
        'sign': 5707554
    },
    25: {
        'key_pair': 23540004,
        'enc': 11869,
        'sign': 7135058
    }
}

# Conversione da µs a secondi
for w in data:
    data[w]['key_pair'] /= 1e6
    data[w]['enc'] /= 1e6
    data[w]['sign'] /= 1e6

# Estrazione delle informazioni da visualizzare
words = list(data.keys())
key_pair_times = [data[w]['key_pair'] for w in words]
enc_times = [data[w]['enc'] for w in words]
sign_times = [data[w]['sign'] for w in words]

# Creazione del grafico
plt.figure(figsize=(10, 6))

plt.plot(words, key_pair_times, label="Key Pair Time", marker='o', color='blue')
plt.plot(words, enc_times, label="Encryption Time", marker='o', color='green')
plt.plot(words, sign_times, label="Signing Time", marker='o', color='red')

# Annotazioni per ogni punto
for i, txt in enumerate(key_pair_times):
    plt.annotate(f'{txt:.6f} s', (words[i], key_pair_times[i]), textcoords="offset points", xytext=(0,10), ha='center')
for i, txt in enumerate(enc_times):
    plt.annotate(f'{txt:.6f} s', (words[i], enc_times[i]), textcoords="offset points", xytext=(0,10), ha='center')
for i, txt in enumerate(sign_times):
    plt.annotate(f'{txt:.6f} s', (words[i], sign_times[i]), textcoords="offset points", xytext=(0,10), ha='center')

# Aggiunta dei dettagli del grafico
plt.title("Falcon 512: Total Time per Operation (s)")
plt.xlabel('Number of Words')
plt.ylabel('Time (s)')
plt.legend()
plt.grid(True)

# Visualizzazione del grafico
plt.show()
