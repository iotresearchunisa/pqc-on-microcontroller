import matplotlib.pyplot as plt
import seaborn as sns

# Dati
words = [50, 100, 200, 400]

# Cicli di clock medi
avg_cycle_keypair = [17330, 17357, 17338, 17326]
avg_cycle_enc = [17342, 17389, 17383, 17346]
avg_cycle_dec = [17638, 17699, 17648, 17656]

# Tempi medi (in µs)
avg_time_keypair = [72, 73, 92, 72]
avg_time_enc = [73, 73, 73, 72]
avg_time_dec = [74, 74, 74, 74]

# Cicli di clock totali
total_cycle_keypair = [866503, 1735706, 3467760, 6930710]
total_cycle_enc = [867104, 1738999, 3476691, 6938620]
total_cycle_dec = [881903, 1769990, 3529622, 7062604]

# Tempi totali (in µs)
total_time_keypair = [3647, 7308, 18579, 29174]
total_time_enc = [3683, 7308, 14615, 29152]
total_time_dec = [3704, 7408, 14804, 29660]

# Imposta lo stile per i grafici
sns.set(style="whitegrid")

# 1. Cicli di clock medi per operazione
plt.figure(figsize=(10, 6))
plt.plot(words, avg_cycle_keypair, marker='o', label="Key Pair (avg)", color='blue')
plt.plot(words, avg_cycle_enc, marker='o', label="Encrypt (avg)", color='green')
plt.plot(words, avg_cycle_dec, marker='o', label="Decrypt (avg)", color='red')
plt.title("Average Cycle Count per Operation")
plt.xlabel("Number of Words")
plt.ylabel("Average Cycle Count")
plt.legend()
plt.grid(True)
plt.show()

# 2. Tempo medio per operazione
plt.figure(figsize=(10, 6))
plt.plot(words, avg_time_keypair, marker='o', label="Key Pair (avg)", color='blue')
plt.plot(words, avg_time_enc, marker='o', label="Encrypt (avg)", color='green')
plt.plot(words, avg_time_dec, marker='o', label="Decrypt (avg)", color='red')
plt.title("Average Time per Operation (µs)")
plt.xlabel("Number of Words")
plt.ylabel("Time (µs)")
plt.legend()
plt.grid(True)
plt.show()

# 3. Cicli di clock totali per operazione
plt.figure(figsize=(10, 6))
plt.plot(words, total_cycle_keypair, marker='o', label="Key Pair (total)", color='blue')
plt.plot(words, total_cycle_enc, marker='o', label="Encrypt (total)", color='green')
plt.plot(words, total_cycle_dec, marker='o', label="Decrypt (total)", color='red')
plt.title("Total Cycle Count per Operation")
plt.xlabel("Number of Words")
plt.ylabel("Total Cycle Count")
plt.legend()
plt.grid(True)
plt.show()

# 4. Tempo totale per operazione
plt.figure(figsize=(10, 6))
plt.plot(words, total_time_keypair, marker='o', label="Key Pair (total)", color='blue')
plt.plot(words, total_time_enc, marker='o', label="Encrypt (total)", color='green')
plt.plot(words, total_time_dec, marker='o', label="Decrypt (total)", color='red')
plt.title("Total Time per Operation (µs)")
plt.xlabel("Number of Words")
plt.ylabel("Time (µs)")
plt.legend()
plt.grid(True)
plt.show()
