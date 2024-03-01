from INITIALIZAIONS import *
from StaticFunctions import *


'''
                    AGORYTMMY 
W tyn probgrami mogą być przechowywane rózne algorytmy. Umieszczony filtr Kalmana składa się z metod obliczających oraz
służących do bezpośredniej interakcji (interakkcja również jest zamieszczona w tym miejscu ponieważ rózne algorytmy mogą 
potrzebować różnych parametrów, stąd taki podział)   

KLASY: 
    SETTERY:
        - delta_t :                 Setter umożliwijaćy zapisywanie paranetru _delta_t i podczas jego zmiany aktualizację 
                                    parametru sample_amount
        - time :                    Setter umożliwijaćy zapisywanie paranetru time i podczas jego zmiany aktualizację 
                                    parametru sample_amount  
        
    PUBLIC: 
        - generate_measures :       Generowanie pomiarów z wykorzytsaniem poł chronionych
        - show_algorithm_params :   Wyseitlanie parametrów
        - algorithm_configure :     Konfiguracja paramterów. Wywołanie _set_transition_model do ustawienia macierzy F
                                    oraz  _set_observation_model do ustawienia macierzy H
        
    PRIVATE: 
        - _set_transition_model
        - _set_observation_model
        
    STATIC :
        - _new_matrix_question :    Dodanie nowegj macierzyy 

'''


class KalmanFilter:
    def __init__(self):
        self.sample_amount = 0
        self._time = TIME
        self.delta_t = DT
        # ilość parametrów
        states_num = INIT_X0.shape[0]

        # inicjalizacja zmiennych estymownaych, początkowych filtru Kalmana
        self.mi_est = np.zeros((states_num, 1))
        self.sigma_t_est = np.zeros((states_num, states_num, 1))

        # inicjalizacja zmiennych wyzerowanych w pierwszym kroku
        self.mi_pred = np.zeros((states_num, 0))
        self.sigma_t_pred = np.zeros((states_num, 0))
        self.measurements = np.zeros((states_num, 0))

        # przypisanie wartości w stanie 0
        self.mi_est[:, 0] = INIT_X0
        self.sigma_t_est[:, :, 0] = INIT_COV

        self.init_XO = INIT_X0
        self.init_cov = INIT_COV
        # przypisanie stałych parametrów
        self.F = INIT_F
        self.B = INIT_B
        self.H = INIT_H
        self.sigma_x = INIT_SIGMA_X
        self.sigma_z = INIT_SIGMA_Z

        self.update_matrix_online = UPDATE_TRANSITION_ONLINE

        self.err_cov_matrix_params = [0,0,0,0]

    @property
    def delta_t(self):
        print(self._delta_t)
        return self._delta_t

    @delta_t.setter
    def delta_t(self, val):
        if self.time is not None:
            self.sample_amount = int(self.time / val)
        print(val)
        self._delta_t = val

    @property
    def time(self):
        print(f"TUTAJ ----   1")
        return self._time

    @time.setter
    def time(self, val):
        if self._delta_t is not None:
            self.sample_amount = int(val / self.delta_t)
        self._time = val

    def show_algorithm_params(self):
        print_info(title="Filtr Kalmana",
                   data=(self.init_XO, self.init_cov, self.sigma_z,self.sigma_x,self.F,self.B,self.H,),
                   data_title=("Początkowa wartość x0", "Początkowa wartość macierzy kowariancji",
                               "Wartość macierzy błędu kowariancji obserwacji R", "Wartość macierzy błędu kowariancji szumu Q",
                               "F", "B",
                               "H", ))

    def algorithm_configure(self):
        n = self.mi_est.shape[0]
        is_models_to_define = input("Zdefiniować model przejść?:\n1.Tak\n2.Nie\n")
        if is_models_to_define == '1':
            self.set_transition_model(n)
            self.set_observation_model(n)

    def estimate_states(self, measures):
        measurement = measures
        n = measures.shape[1]
        num_of_states = measures.shape[0]
        h_size = self.sigma_z.shape[1]

        mi_pred = np.zeros((num_of_states, n))
        mi_est = np.zeros((num_of_states, n))
        sigma_t_est = np.zeros((num_of_states, num_of_states, n))
        sigma_t_pred = np.zeros((num_of_states, num_of_states, n))
        K = np.zeros((num_of_states, h_size, n))

        mi_est[:, 0] = self.init_XO
        print(f"mi_est[:, 0] = {mi_est[:, 0]}")
        sigma_t_est[:, :,0 ] = self.init_cov

        for k in range(n - 1):

            # predykcja
            mi_pred[:, k + 1] = self.F @ mi_est[:, k]
            sigma_t_pred[:, :, k + 1] = self.F @ sigma_t_est[:, :, k] @ self.F.T + self.sigma_x

            # aktualizacja
            K[:, :, k + 1] = sigma_t_pred[:, :, k + 1] \
                             @ self.H.T @ \
                             np.linalg.inv(self.H @ sigma_t_pred[:, :, k + 1] @ self.H.T + self.sigma_z)
            mi_est[:, k + 1] = mi_pred[:, k + 1] + K[:, :, k + 1] @ (measurement[:, k] - self.H @ mi_pred[:, k + 1])
            sigma_t_est[:, :, k + 1] = (np.eye(num_of_states) - K[:, :, k + 1] @ self.H) @ sigma_t_pred[:, :, k + 1]

        self.measurements = measurement
        self.mi_est = mi_est
        return mi_est

    def _set_transition_model(self, n):
        is_transition_to_change = input("Chcesz zmienić model przejsć ? \n1.Tak\n2.Nie\n")
        if is_transition_to_change == '1':
            is_adv_param_to_define = input("1.Zmiana parametrów macierzy kowarianacji?\n2. Macerz przejść.\n")
            if is_adv_param_to_define == "1":
                params = [input(f"Podaj Ex_{i}") for i in range(self.F.shape[0])]
                self.sigma_x = create_measure_err_cov_matrix(params)
            else:
                transition_model = KalmanFilter._new_matrix_question(n, n, "Wprowadź wartość macierzy, F:\n")
                self.transition_model = transition_model

    def _set_observation_model(self, n):
        is_observation_to_change = input("Chcesz zmienić model obserwacji ? \n1.Tak\n2.Nie\n")
        if is_observation_to_change == '1':
            is_adv_param_to_define = input("1.Zmiana parametrów macierzy kowarianacji?\n2. Macierz obserwacji.\n")
            if is_adv_param_to_define == "1":
                est_matrix_multiplier = [input(f"Podaj I_{i}") for i in range(self.F.shape[0])]
                params = [input(f"Podaj param_{i}") for i in range(len(self.err_cov_matrix_params))]
                self.sigma_z = create_est_err_cov_matrix(self.F.shape[0], est_matrix_multiplier, params)
            else:
                observation_model = KalmanFilter._new_matrix_question(n, n, "Wprowadź wartość macierzy, H:\n")
                self.observation_model = observation_model

    @staticmethod
    def _new_matrix_question(n=0, m=0):
        val = []
        for i in range(m):
            row = []
            for j in range(n):
                elem = input('#')
                elem = float(elem) if elem != '' else 0
                if m > 0:
                    row.append(elem)
                else:
                    val.append(row)
            if m > 0:
                val.append(row)

        val = np.array(val)
        return val