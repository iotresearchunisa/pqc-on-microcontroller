import matplotlib.pyplot as plt

# Dati originali SABER (in µs)
saber_data = {
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
for w in saber_data:
    saber_data[w]['key_pair'] /= 1e6
    saber_data[w]['enc'] /= 1e6
    saber_data[w]['dec'] /= 1e6

for w in light_saber_data:
    light_saber_data[w]['key_pair'] /= 1e6
    light_saber_data[w]['enc'] /= 1e6
    light_saber_data[w]['dec'] /= 1e6

for w in fire_saber_data:
    fire_saber_data[w]['key_pair'] /= 1e6
    fire_saber_data[w]['enc'] /= 1e6
    fire_saber_data[w]['dec'] /= 1e6

# Estrazione delle informazioni da visualizzare
words = list(saber_data.keys())

saber_key_pair_times = [saber_data[w]['key_pair'] for w in words]
saber_enc_times = [saber_data[w]['enc'] for w in words]
saber_dec_times = [saber_data[w]['dec'] for w in words]

light_saber_key_pair_times = [light_saber_data[w]['key_pair'] for w in words]
light_saber_enc_times = [light_saber_data[w]['enc'] for w in words]
light_saber_dec_times = [light_saber_data[w]['dec'] for w in words]

fire_saber_key_pair_times = [fire_saber_data[w]['key_pair'] for w in words]
fire_saber_enc_times = [fire_saber_data[w]['enc'] for w in words]
fire_saber_dec_times = [fire_saber_data[w]['dec'] for w in words]

# Creazione del grafico
plt.figure(figsize=(12, 8))

# Plot per SABER
plt.plot(words, saber_key_pair_times, label="SABER Key Pair Time", marker='o', color='blue')
plt.plot(words, saber_enc_times, label="SABER Encryption Time", marker='o', color='green')
plt.plot(words, saber_dec_times, label="SABER Decryption Time", marker='o', color='red')

# Plot per LIGHT-SABER
plt.plot(words, light_saber_key_pair_times, label="LIGHT-SABER Key Pair Time", marker='x', color='cyan')
plt.plot(words, light_saber_enc_times, label="LIGHT-SABER Encryption Time", marker='x', color='lime')
plt.plot(words, light_saber_dec_times, label="LIGHT-SABER Decryption Time", marker='x', color='magenta')

# Plot per Fire-Saber
plt.plot(words, fire_saber_key_pair_times, label="Fire-SABER Key Pair Time", marker='s', color='orange')
plt.plot(words, fire_saber_enc_times, label="Fire-SABER Encryption Time", marker='s', color='purple')
plt.plot(words, fire_saber_dec_times, label="Fire-SABER Decryption Time", marker='s', color='brown')


# Aggiunta dei dettagli del grafico
plt.title("SABER vs LIGHT-SABER vs Fire-SABER: Total Time per Operation (s)")
plt.xlabel('Number of Words')
plt.ylabel('Time (s)')
plt.legend()
plt.grid(True)

# Visualizzazione del grafico
plt.show()
