from numpy.core.fromnumeric import size
import scipy
import numpy
import scipy.signal as sig
import matplotlib.pyplot

rr = [1.0, 1.0, 1.0, 1.0, 1.0]  # tempo em segundos
fs = 250  # taxa de amostragem
pqrst = sig.wavelets.daub(10)  # simula o sinal
ecg = scipy.concatenate([sig.resample(pqrst, int(r*fs)) for r in rr])

min_value = min(ecg)
max_value = max(ecg)

# Mudança de escala. Nova escala de 0 a 255
data_array = []
for val in ecg:
    data_array.append(int(255*(val+(-1*min_value))/(max_value-min_value)))

print("A = ", size(a))

t=scipy.arange(len(data_array))/fs

F=0.003333333
G=[]
while F <= 5:
    G.append(F)
    F += 0.004



matplotlib.pyplot.plot(G, data_array)

matplotlib.pyplot.show()
