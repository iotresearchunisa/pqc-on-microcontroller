import re


def leggi_file(nome_file):
    """
    Legge il contenuto di un file di testo.
    :param nome_file: Nome del file da leggere.
    :return: Contenuto del file come stringa.
    """
    with open(nome_file, 'r') as file:
        return file.read()


def estrai_parole_da_byte(contenuto):
    """
    Estrae le parole dall'array di byte.
    :param contenuto: Contenuto dell'array di byte come stringa.
    :return: Lista di parole estratte.
    """
    # Trova le righe che contengono i byte e estrae i valori
    righe = contenuto.splitlines()
    parole = []
    byte_array = []

    for riga in righe:
        # Trova i byte nella riga
        byte_matches = re.findall(r'\d+', riga)
        if byte_matches:
            # Aggiunge i byte alla lista
            byte_array.extend(int(byte) for byte in byte_matches)
        # Se la riga termina con un commento, estrai la parola
        if '//' in riga:
            parola = riga.split('//')[-1].strip()
            if parola:
                parole.append((parola, byte_array))
                byte_array = []  # Resetta il byte_array per la prossima parola

    return parole


def genera_array_c_cpp(parole):
    """
    Genera una rappresentazione di un array C++ di array di uint8_t.
    :param parole: Lista di tuple contenenti parole e i loro byte corrispondenti.
    :return: Stringa formattata per l'array C++.
    """
    array_cpp = "const uint8_t parole_in_array[][ ] = {\n"

    for parola, byte_array in parole:
        byte_string = ", ".join(map(str, byte_array))
        array_cpp += f"    {{ {byte_string} }}, // {parola}\n"

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
    nome_file_input = input("Inserisci il nome del file di input (esempio: byte_array.txt): ")

    # Leggi il contenuto del file di input
    contenuto = leggi_file(nome_file_input)

    # Estrai le parole e i byte
    parole = estrai_parole_da_byte(contenuto)

    # Genera l'array C++
    array_cpp = genera_array_c_cpp(parole)

    # Chiedi il nome del file di output
    nome_file_output = input("Inserisci il nome del file di output (esempio: parole_in_array.cpp): ")

    # Scrivi l'array C++ nel file di output
    scrivi_file_output(nome_file_output, array_cpp)
