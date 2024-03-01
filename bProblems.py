import math
from INITIALIZAIONS import *
from StaticFunctions import *

'''
                    Problemy            
Program przechowujący zaimplementowane problemy. Jego głównym zadanienm jest generowanie danych pomiarowych, 
zwracanych i przekazywanych dalej przez moduł kontrolera.

KLASY: 
    SETTERY:
        - delta_t :                 Setter umożliwijaćy zapisywanie paranetru _delta_t i podczas jego zmiany aktualizację 
                                    parametru sample_amount
        - time :                    Setter umożliwijaćy zapisywanie paranetru time i podczas jego zmiany aktualizację 
                                    parametru sample_amount  
        
    PUBLIC: 
        - generate_measures :       Generowanie pomiarów z wykorzytsaniem poł chronionych
        - show_problem_params :     Wyseitlanie parametrów
        - problem_configure :       Konfiguracja paramterów. Wywołanie _new_problem_params do interkacji z użytkownikiem 
                                    oraz  _set_problem_params do zpaisania paremtrów do pol klasy
        
    PRIVATE: 
        - _sim_forward
        - _sim_curve_motion
        - _sim_line_change
        - _sim_acceleration
        - _sim_deceleration
        - _custom_ride
        - _new_problem_params :      Operacja interkacji z użytkownikiem i pobrania danych 
        - _set_problem_params :      Zapisanie parametrów  uzyskanych dzięki new_problem_params do pól klasy 
        

'''

class DynamicReasoning:
    def __init__(self, algorithm):
        self.with_noise = NOISE
        self.noise_level = NOISE_LEVEL        # maksymalne wychylenie od podstawowej wartości
        self.algorithm = algorithm

        self.sample_amount = 0
        self._delta_t = DT
        self._time = TIME
        self.sigma_measure = [0.1,0.2,0.002,0.0030,0.1]

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
        return self._time

    @time.setter
    def time(self, val):
        if self._delta_t is not None:
            self.sample_amount = int(val / self.delta_t)
        self._time = val

    def generate_measures(self, operation):
        measures = 0
        print(f"opeartion={operation}")
        if operation == 0: measures = self._sim_forward()
        elif operation == 1: measures = self._sim_curve_motion()
        elif operation == 2: measures = self._sim_line_change()
        elif operation == 3: measures = self._sim_acceleration()
        elif operation == 4: measures = self._sim_deceleration()
        elif operation == 5: measures = self._custom_ride()

        print(measures[0])
        if self.with_noise:
            measures = self.generate_noises2(measures, self.algorithm.sigma_x)
        print(measures[0])

        return measures

    def show_problem_params(self):
        print_info(title="Dynamiczne wnioskowanie",
                   data=(self.with_noise,self.noise_level,self.sample_amount,),
                   data_title=("Czy dodać szum?", "Maksymalnie wychylone zaszumienie","Ilość próbek",))

    def problem_configure(self):
        with_noise,noise_level,sample_amount = self._new_problem_params()
        self._set_problem_params(with_noise,noise_level,sample_amount)

    def _sim_forward(self):
        num_steps = self.sample_amount
        states = np.zeros((STATES, num_steps))
        deltas = np.zeros(num_steps)

        for i in range(num_steps):
            # Aktualizacja stanu
            kappa = np.random.uniform(0, 0.1)
            X = np.random.uniform(0, 0.1)#V * dt * V * dt * np.sin(alpha) - np.sin(kappa)  # Przesunięcie wzdłuż osi X
            alpha = np.random.uniform(0, 0.1)#delta * dt
            V = np.random.uniform(0, 0.1)#V_meas
            delta = np.random.uniform(-0.1, 0.1)

            # Zapisanie stanu i pomiaru
            states[0, i] = X
            states[1, i] = alpha
            states[2, i] = V
            deltas[i] = delta

        return states

    def _sim_curve_motion(self):
        duration = self.time
        dt = self.delta_t
        V = 70
        R = 75
        steer_angle = 0
        curvature = 0

        num_steps = self.sample_amount
        t = np.arange(0, duration, dt)

        states = np.zeros((STATES, num_steps))
        first_steer_flag = False

        for i in range(0,num_steps):
            if i > 50 and steer_angle <= R and not first_steer_flag:
                steer_angle += 0.1
                if steer_angle == R:
                    first_steer_flag = True

            alpha = steer_angle * 0.99

            if curvature < R:
                curvature += 0.01  # Krzywizna drogi zależna od x i wychylenia kątowego kierownicy

            pos = ((self.delta_t * i * V / 3600) * np.tan(math.radians(curvature)) - (self.delta_t * i * V / 3600) * np.tan(math.radians(alpha)))
            states[0, i] = pos
            states[1, i] = alpha
            states[2, i] = V

        return states

    def _sim_acceleration(self):
        V = 40

        num_steps = self.sample_amount

        states = np.zeros((STATES, num_steps))
        deltas = np.zeros(num_steps)

        for i in range(0,num_steps):
            # Aktualizacja stanu
            X = np.random.uniform(-0.01,0.01)
            alpha = np.random.uniform(0, 0.1)
            delta = np.random.uniform(-0.1, 0.1)
            if i > 10 and V < 100:
                V += np.random.uniform(0, 1)

            states[0, i] = X
            states[1, i] = alpha
            states[2, i] = V
            deltas[i] = delta

        return states

    def _sim_deceleration(self):
        V = 100

        num_steps = self.sample_amount

        states = np.zeros((STATES, num_steps))
        deltas = np.zeros(num_steps)

        for i in range(0,num_steps):
            # Aktualizacja stanu
            X = np.random.uniform(0, 0.1)
            alpha = np.random.uniform(0, 0.1)
            delta = np.random.uniform(-0.1, 0.1)
            if i > 100 and V > 20:
                V -= np.random.uniform(0, 0.1)

                # Zapisanie stanu i pomiaru
            states[0, i] = X
            states[1, i] = alpha
            states[2, i] = V
            deltas[i] = delta

        return states

    def _sim_line_change(self):
        # Ustawienie początkowych wartości zmiennych
        alpha = 0  # Kąt kierownicy w stopniach (w lewo < 0)
        v = 40  # Stała prędkość pojazdu w m/s
        x = 2  # Położenie pojazdu od środka drogi w m
        dt = self.delta_t  # Krok czasowy symulacji w s - może 0.5
        V = 50

        num_steps = self.sample_amount
        # Ustawienie początkowe dla regulatora
        destination = -2

        # Stałe dla regulatora
        HIGH_ANGLE = 40
        MEDIUM_ANGLE = 25
        LOW_ANGLE = 10
        MEDIUM_ANGLE_LEVEL = 0.8
        LOW_ANGLE_LEVEL = 0.2
        VEHICLE_IN_POS = 0.02
        CONST_ALPHA_DT = 180  # stopień na s
        CONST_RETURN_ALPHA_DT = 50  # stopień na s

        n = self.sample_amount  # Liczba kroków symulacji
        states = np.zeros((STATES, num_steps))
        calc_dist = x - destination


        for i in range(0, n):
            print(f"{'#'*100}")
            act_diff = x - destination
            print(f"act_diff=  {act_diff}")
            if x >= destination - 0.1 and x <= destination + 0.1:
                calc_dist = 0
                desired_angle = 0
                if alpha > 0.01:
                    alpha -= alpha_per_sec * dt / 100
                else:
                    alpha += alpha_per_sec * dt / 100
            else:
                if abs(act_diff / calc_dist) > MEDIUM_ANGLE_LEVEL:
                    alpha_per_sec = CONST_ALPHA_DT
                    desired_angle = HIGH_ANGLE

                elif abs(act_diff / calc_dist) > LOW_ANGLE_LEVEL and abs(act_diff / calc_dist) < MEDIUM_ANGLE_LEVEL:
                    alpha_per_sec = CONST_RETURN_ALPHA_DT
                    desired_angle = MEDIUM_ANGLE
                elif abs(act_diff / calc_dist) > VEHICLE_IN_POS and abs(act_diff / calc_dist) < LOW_ANGLE_LEVEL:
                    alpha_per_sec = CONST_ALPHA_DT
                    desired_angle = LOW_ANGLE
                if x > destination:
                    if alpha > desired_angle:
                        alpha -= alpha_per_sec * dt / 100
                    else:
                        alpha += alpha_per_sec * dt / 100
                    x -= v * np.sin(np.radians(alpha)) * dt /1000

            # Zapisanie stanu, pomiaru i krzywizny drogi
            states[0, i] = x #- center_offset
            states[1, i] = alpha
            states[2, i] = V

        return states

    def _custom_ride(self):
        states = []
        return np.array(states)

    def simulate_measurement(self,X,angle,V,delta,kappa):
        X_meas = X + np.random.normal(0, self.sigma_measure[0])  # Pomiar położenia
        alpha_meas = angle + np.random.normal(0, self.sigma_measure[1])  # Pomiar położenia
        V_meas = V + np.random.normal(0, self.sigma_measure[2])  # Pomiar położenia
        delta_meas = delta + np.random.normal(0, self.sigma_measure[3])  # Pomiar położenia
        kappa_meas = kappa + np.random.normal(0, self.sigma_measure[4])  # Pomiar położenia

        return np.array([X_meas, alpha_meas, V_meas, delta_meas, kappa_meas])

    def generate_noises2(self, measurement, sigma_z):
        noise = np.random.normal(0, 0.2, size=measurement.shape)
        noisy_measurement = measurement + noise
        return noisy_measurement

    def _new_problem_params(self):
        print(f"{'-' * 80}")
        with_noise = True if input("Szum:\n1.Tak\n2.Nie\n") == "1" else False
        if with_noise:
            print(f"{'-' * 80}")
            noise_level = float(input("Podaj maksymalną wartość jaką może uzyskać zaszumienie:   \n"))
        print(f"{'-' * 80}")
        sample_amount = int(input(f"Ile próbek? (Aktualnie - [{self.sample_amount}])\n"))
        print(f"{'-' * 80}")
        return with_noise,noise_level,sample_amount

    def _set_problem_params(self, with_noise,noise_level,sample_amount):
        self.with_noise = with_noise
        if self.with_noise:
            self.noise_level = noise_level
        self.sample_amount = sample_amount
