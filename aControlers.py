import matplotlib.pyplot as plt
from cAlgorithms import KalmanFilter
from bProblems import DynamicReasoning
from INITIALIZAIONS import *
from StaticFunctions import *

''' 
                                    MENU
Menu użytkownika - defniownane w tym miejscu z automatu aktualizuje się poprzez wywołąnie
StaticFunctions.menu_converter w pliku _main 
 '''
MENU = ["Test 1 - jazda prosto",
        "Test 2 - jazda po łuku",
        "Test 3 - zmiana pasa",
        "Test 4 - przyspieszenie",
        "Test 5 - hamoanie",
        "Test 6 - custom_ride",
        "Konfiguj parametry",
        "Wyświetl aktulane ustawienia",
        "Koniec"]

'''
                KOMENDY
Komendy podzielone są w trzy grupy :
    - Testy 
    - konfiguracja
    - okaż konfigurację 
Wybór w self.evaluate_command
'''
# Lista komend do wyboru testów
TEST_CMDS = list(range(len(MENU) - 3))
# Index komendy konfiguracji
CONFIG_CMD = len(TEST_CMDS) + 1
# Index komendy pokaż aktualną konfigurację
SHOW_CMD = CONFIG_CMD + 1

'''
            PLOTY 
            
Jeśli wykorzystane byłoby więcej niż 3 ploty do zobrazowania wyników w tyn miejscu można dodać label

'''
PLOT_TITLES = ["Wartości x","Wartości alpha","Wartości v"]

'''
                KONTROLER
        
Klasa main kontroler, podział uwzględnia ewentualną wymainę kontrolera np.dla różnych systemów. Można zadeklarować 
prblem i algorytm jako arumenty przy inicjalizacji klasy, defaultowo tworzy pole będące instancją problemu - 
DynamicReasoning oraz filtru Kalmana.
 

KLASY :
    PUBLIC:
        - evalute_command :     Wywołanie komendy użytkkownika
        - create_plots :        Rysowannie uzyskanych wyników dla zadanego problemu 
    
    PROTECTED:
        - _configure_parameters :      Po wybraniu przez użytkownika opcji konfiguracji w tym miejscu wywołuje 
                                       metody konfiguracji pola problemu oraz pola algorytmu.
        - _show_config :               Po wybraniu przez użytkownika wyświetlenia danych w tym miejscu wywołuje
                                       metody pól roblemu oraz algorytmu wyświetlające parametry dla poszczególnych
                                       instancji. 
        - _test :                      Wywołanie jednej z opcji testów. Wybrany numer z indexem -1 wysyłany jest do 
                                       metody klasy problemu gdzie wybrana jest symulacja. Zwrócona wartość parametru 
                                       jest argumentem metody optymalizacji algorytmu filtru Kalmana. Po wyliczneiu 
                                       estymat zmienne : wygenerowane sygnały - measurements oraz estymwoane wartości
                                       estimates nadpisywane są w polach klasy KONTROLER. Ten zabieg umożliwia 
                                       wywołanie metody rysującej ploty  
        -  _set_test_params :          Metoda wywołana tuż przed wyznaczeniem parametrów pomiaru, pyta czy nadpisać 
                                       macierze stanu i obserwacji
        -  _set_time_stamps :          Ustaiwa czas próbkowania oraz trwania symulacji dla danego testu. W zależności od
                                       testu, pomiary łatwiej było przeglądać na odpowiednich pramaterach.
        -  _set_model_params :         Umożliwia ustawienie konkretnych macierzy tranzycji i obserwacji dla konkretnego 
                                       testu                            
                
    CONSTS: 
        - STOP :                        Na podstaiwe listy MENU przypisana jest długośćlisty. Dzięki temu użytkownik 
                                        po wybraniu osttaniej pozycji ma możliwość zakończenia prograu - pętli while 
                                        w _main  
'''
class MainController:
    STOP = len(MENU)

    def __init__(self, problem=None, algorithm=None):
        # inicjalizacja wybranego problemu i algorytmu
        self.algorithm = algorithm if algorithm is not None else KalmanFilter()
        self.problem = problem if problem is not None else DynamicReasoning(self.algorithm)

        # inicjalizacja pomiaru oraz wyznaczonej estymaty
        self.measurements = 0
        self.estimations = 0

        # parametry kontroli nad blokiem
        self.draw_plot = True

        # pole przechowujące dostępne opcja dla użytkownika
        self.menu = menu_converter(MENU)

    """
    Metody publiczne
    """
    def evaluate_command(self, cmd):
        print(f"cmd = {CONFIG_CMD}")
        if cmd-1 in TEST_CMDS: self._test(cmd)
        elif cmd == CONFIG_CMD: self._configure_parameters()
        elif cmd == SHOW_CMD: self._show_config()
        else: pass

    def create_plots(self):
        if self.draw_plot:
            n = len(self.algorithm.measurements[0])
            t = np.arange(n)

            # Wyświetlanie wyników
            plt.figure(figsize=(10, 9))

            for x, title in enumerate(PLOT_TITLES[:len(PLOT_TITLES)]):  # Ograniczenie do 3 wykresów
                # Porównanie estymaty z prawdziwymi wartościami dla prędkości
                plt.subplot(3, 1, x + 1)
                plt.plot(t, self.measurements[x], 'r-', label='Pomiar')
                plt.plot(t, self.estimations[x], 'b-', label='Estymacja')
                plt.xlabel('Czas')
                plt.ylabel(title)
                plt.legend()

            plt.tight_layout()
            plt.show()

    """
    Metody chronione
    """
    def _configure_parameters(self):
        self.draw_plot = False
        config = True if input("Skonfigurować parametry problemu ?\n y/n ? \n") == "y" else False
        if config:
            self.problem.problem_configure()
        config = True if input("Skonfigurować parametry algorytmu ?\n y/n ? \n") == "y" else False
        if config:
            self.algorithm.algorithm_configure()
        input("Wciśnij enter, aby przejść dalej...")

    def _show_config(self):
        self.draw_plot = False
        self.problem.show_problem_params()
        self.algorithm.show_algorithm_params()

    def _test(self, cmd):
        self.draw_plot = True
        self._set_test_params(cmd)
        command = cmd - 1
        measures = self.problem.generate_measures(command)
        estimations = self.algorithm.estimate_states(measures=measures)

        self.measurements = measures
        self.estimations = estimations
        zapisz_do_pliku(measures,estimations)

    def _set_test_params(self,cmd):
        self._set_time_stamps(cmd)
        if input("Nadpisać macierze przejść?\ny/n\n") == 'y':
            self._set_model_params(cmd)

    def _set_time_stamps(self, cmd):
        command=cmd

        # set dt
        if command in [1]:
            dt = 1
        elif command in [2,4,5]:
            dt = 0.1
        elif command in [3]:
            dt = 0.01

        # set time
        if command in [1,4]:
            time = 100
        elif command in [2,5]:
            time = 1000
        elif command in [3]:
            time = 300


        self.algorithm.delta_t = dt
        self.problem.delta_t = dt
        print(f"Algo sample = {self.algorithm.sample_amount}")
        self.algorithm.time = time
        self.problem.time = time
        print(f"Problem sample = {self.problem.sample_amount}")

        print(command)

    def _set_model_params(self,cmd):
        if cmd in [3,4,5]:
            self.algorithm.transition_model = update_transition_model(0.2)
            self.algorithm.observation_model = update_observation_model(0.1)

