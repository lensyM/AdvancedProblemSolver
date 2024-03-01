"""
Program główny wywołujący problem oraz wybrany algorytm filtracji
"""
from aControlers import MainController


if __name__ == "__main__":

    # Utworzenie instancji kontrolera
    controller = MainController()

    # Pierwsze zapytanie użytkownika o wprowadzenie akcji
    cmd = int(input("MENU:\n" + controller.menu))

    # Pętla główna
    while cmd != controller.STOP:

        # Wywołanie wybranej przez użytkownika operacji
        controller.evaluate_command(cmd)

        # Utworzenie plotów, w zależnośći od zmiennej  MainController.draw_plot.
        # zmienna setowana/resetowana na początku każdej wywołanej operacji
        controller.create_plots()

        # ponowne wywołanie pytania
        cmd = int(input("MENU:\n" + controller.menu))

