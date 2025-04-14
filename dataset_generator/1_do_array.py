def leggi_parole_da_file(nome_file):
    """
    Legge le parole da un file di testo.
    :param nome_file: Il nome del file da cui leggere le parole.
    :return: Lista di parole lette dal file.
    """
    with open(nome_file, 'r') as file:
        parole = [line.strip() for line in file.readlines()]
    return parole


def parola_in_byte(parola):
    """
    Converte una parola in un array di byte.
    :param parola: La parola da convertire.
    :return: Lista di byte (valori numerici corrispondenti ai caratteri ASCII della parola).
    """
    return [ord(c) for c in parola]


def genera_array_cpp(parole):
    """
    Genera una rappresentazione di un array C++ di tipo uint8_t dalle parole in byte.
    :param parole: Lista di parole.
    :return: Stringa che rappresenta l'array C++.
    """
    array_cpp = "uint8_t parole_in_byte[] = {\n"
    for parola in parole:
        byte_array = parola_in_byte(parola)
        byte_string = ", ".join(map(str, byte_array))
        array_cpp += "    " + byte_string + ", // " + parola + "\n"
    array_cpp += "};"
    return array_cpp


def scrivi_file_output(nome_file, contenuto):
    """
    Scrive il contenuto in un file di testo.
    :param nome_file: Nome del file di output.
    :param contenuto: Contenuto da scrivere nel file.
    """
    with open(nome_file, 'w') as file:
        file.write(contenuto)
    print(f"File '{nome_file}' generato con successo.")


if __name__ == "__main__":
    # Chiedi il nome del file di input
    nome_file_input = input("Inserisci il nome del file di input (esempio: parole.txt): ")

    # Leggi le parole dal file di input
    parole = leggi_parole_da_file(nome_file_input)

    # Genera l'array C++
    array_cpp = genera_array_cpp(parole)

    # Chiedi il nome del file di output
    nome_file_output = input("Inserisci il nome del file di output (esempio: parole_in_byte.cpp): ")

    # Scrivi l'array C++ nel file di output
    scrivi_file_output(nome_file_output, array_cpp)
