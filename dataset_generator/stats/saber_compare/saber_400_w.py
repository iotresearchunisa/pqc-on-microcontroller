import matplotlib.pyplot as plt

# Dati originali (in µs)
data = {
    50: {
        'key_pair': 3640,
        'enc': 3661,
        'dec': 3714
    },
    100: {
        'key_pair': 7299,
        'enc': 7306,
        'dec': 7416
    },
    200: {
        'key_pair': 14567,
        'enc': 14565,
        'dec': 14803
    },
    400: {
        'key_pair': 29129,
        'enc': 29130,
        'dec': 29614
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



# Aggiunta dei dettagli del grafico
plt.title("SABER: Total Time per Operation (s)")
plt.xlabel('Number of Words')
plt.ylabel('Time (s)')
plt.legend()
plt.grid(True)

# Visualizzazione del grafico
plt.show()
