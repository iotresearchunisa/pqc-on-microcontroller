import random
import string


def genera_parola(lunghezza):
    """
    Genera una parola casuale di una certa lunghezza.
    """
    lettere = string.ascii_lowercase
    return ''.join(random.choice(lettere) for _ in range(lunghezza))


def genera_dataset_parole(num_parole, lunghezza_min=3, lunghezza_max=10):
    """
    Genera un dataset di parole casuali.
    :param num_parole: Numero di parole da generare.
    :param lunghezza_min: Lunghezza minima delle parole.
    :param lunghezza_max: Lunghezza massima delle parole.
    :return: Lista di parole generate.
    """
    dataset = []
    for _ in range(num_parole):
        lunghezza_parola = random.randint(lunghezza_min, lunghezza_max)
        parola = genera_parola(lunghezza_parola)
        dataset.append(parola)
    return dataset


def salva_dataset_in_file(dataset, nome_file):
    """
    Salva il dataset di parole in un file di testo.
    :param dataset: Lista di parole da salvare.
    :param nome_file: Nome del file in cui salvare il dataset.
    """
    with open(nome_file, 'w') as file:
        for parola in dataset:
            file.write(parola + '\n')
    print(f"Dataset salvato con successo in '{nome_file}'.")


if __name__ == "__main__":
    # Chiediamo all'utente quante parole generare
    num_parole = int(input("Inserisci il numero di parole da generare: "))

    # Generiamo il dataset
    dataset = genera_dataset_parole(num_parole)

    # Chiediamo il nome del file
    nome_file = input("Inserisci il nome del file dove salvare il dataset (esempio: dataset.txt): ")

    # Salviamo il dataset nel file
    salva_dataset_in_file(dataset, nome_file)
