import numpy as np
import datetime

# W _menu na podstawie listy generuje tekst dla użytkownika jakie są dostępne opcje
def menu_converter(my_menu)->str:
    menu = ""
    for i, item in enumerate(my_menu, start=1):
        menu += f"{i}. {item}\n"
    return menu

# Wyświetlanie wszytskichh informacji o stanie danego modułu
def print_info(title, data_title, data):
    frame_length = 80
    size = len(data_title)
    print('+' + '-' * (frame_length - 2) + '+')
    print(f"|{title:^{frame_length-2}}|")
    print('+' + '-' * (frame_length - 2) + '+')
    for i in range(size):
        data_value = np.array(data[i]).tolist()
        print(f"| {data_title[i]} = {str(data_value):<{frame_length-4}}")
    print('+' + '-' * (frame_length - 2) + '+')


# Zapsiywanie do pliku
def zapisz_do_pliku(zmienna1, zmienna2):
    format_daty = "%d%m%Y"
    format_godziny = "%H%M%S"
    obecny_czas = datetime.datetime.now()

    nazwa_pliku = "KF_Measure_" + obecny_czas.strftime(format_daty) + "_" + obecny_czas.strftime(
        format_godziny) + ".txt"

    try:
        with open(nazwa_pliku, "a") as plik:
            plik.write(f"Measured: {zmienna1}\n")
            plik.write(f"Estimated: {zmienna2}\n")
            plik.write("-" * 30 + "\n")
        print("Dane zapisano do pliku.")
    except IOError:
        with open(nazwa_pliku, "w") as plik:
            plik.write(f"Measured: {zmienna1}\n")
            plik.write(f"Estimated: {zmienna2}\n")
            plik.write("-" * 30 + "\n")
        print("Utworzono nowy plik i zapisano dane.")




