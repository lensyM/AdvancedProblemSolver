import numpy as np
from math import *
'''
Program predefinujący poszczrgólne parametry. Są one możliwe do zmiany w programie w późniejszym czasie przez 
użytkownika

'''
# Parametry Czasu
DT = 0.1
TIME = 100

# Paranetry obecności szumu
NOISE = True    # Czy mabyć
NOISE_LEVEL = 1 # Maksymalne  wychylenie
alpha = 20      # parametr możliwy do wykorzystaua dla macierzy przejść. Opisuje powiązanie drogi z
                # obróceniem obiektu o kąt alpha
UPDATE_TRANSITION_ONLINE = True     # Umożliwia aktualizwoanie parametrów macierzy kowariancji online.
STATES = 3                          # Ilość parametów wektora stanów


sigma_x = 0.1
sigma_x_squared = sigma_x**2

sigma_z = 0.1
sigma_z_squared = sigma_z ** 2


INIT_X0 = np.zeros(STATES)   # Pierwszy wektor stanu
INIT_COV = np.eye(STATES)            # Pierwsza macierz kowarinacji
INIT_B = np.eye(STATES)    # macierz kontroli wpływu sterowanaia


'''

INIT_X0 = np.array([0, 0, 0, 0, 0])   # Pierwszy wektor stanu
INIT_COV = np.eye(5)            # Pierwsza macierz kowarinacji
INIT_F = F = np.array([[1, 0, 0,0,0],#DT*cos(alpha),0,0],
                       [0, 1, 0,0,0],#DT*sin(alpha),0,0],
                       [0, 0, 1,0,0],
                       [0, 0, 0,0,0],
                       [0, 0, 0,0,0],
                       ]) # macierz przejść

INIT_H = np.array([[1, 0, 1, 0, 0],
              [0, 1, 0, 0, 0],
              [0, 0, 1, 0, 0],
              [0, 1, 0, 0, 0],
              [0, 0, 0, 0, 0]])    # obserwacje
              
INIT_SIGMA_X = np.array([[sigma_x_squared, 0, 0,0,0],
                           [0, sigma_x_squared, 0,0,0],
                           [0, 0, sigma_x_squared,0,0],
                           [0, 0, 0,sigma_x_squared,0],
                           [0, 0, 0,0,sigma_x_squared]])  # Macierz kowariancji szumów obiektu
INIT_SIGMA_Z = np.array([[sigma_z_squared, 0, 0, 0, 0],
                        [ 0, sigma_z_squared,0, 0, 0],
                        [ 0, 0, sigma_z_squared,0, 0],
                        [0, 0, 0, sigma_z_squared, 0],
                        [0, 0, 0, 0, sigma_z_squared]])# Macierz kowariancji szumów pomiaru           

'''

# Init macierz wpływu przejść
INIT_F = np.array([ [1, 0, 0],#DT*cos(alpha),0,0],
                    [0, 1,0],#DT*sin(alpha),0,0],
                    [0, 0, 1],
                    ]) # macierz przejść


# Init macierz wpływu obserwacji
INIT_H = np.array([[1, 0, 0],
                  [0, 1, 0],
                  [0, 0, 1]
                  ])    # obserwacje

# Macierz kowariancji szumów obiektu
INIT_SIGMA_X = np.array([[1, 0,0],
                               [0, 1, 0],
                               [0, 0, 1]])

# Macierz kowariancji szumów pomiaru
INIT_SIGMA_Z = np.array([[1, 0, 0],
                        [ 0, 1,0],
                        [ 0, 0, 1]])


# Funkcja generująca sparametryzowany model przejść.
def update_transition_model(n):
    return np.array([[1, 0, 0, 0, 0],#DT * cos(n)
                     [0, 1, 0, 0, 0], # DT * sin(n)
                     [0, 0, 1, 0, 0],
                     [0, 0, 0, 0, 0],
                     [0, 0, 0, 0, 0],
                     ])

# Funkcja generująca sparametryzowany model obserwacji.
def update_observation_model(n):
    return np.array([[1,0,0],
                     [0,1,0],
                     [0,0,1],
                     [0,0,0],
                     [0,0,0]])


# Funkcja generująca sparametryzowaną macierz kowarinacji błedów estymacji .
def create_est_err_cov_matrix(size, est_matrix_multiplier, params):
   q = np.array([[1, 2, params[0]],
                 [0, 1, 0],
                 [1, 0, 1]])
   W = np.eye(size) * est_matrix_multiplier
   return q @ W @ q.T


# Funkcja generująca sparametryzowaną macierz kowarinacji błedów pomiaru
def create_measure_err_cov_matrix(sig_matrix_param):
    return np.array(len(sig_matrix_param)) * sig_matrix_param