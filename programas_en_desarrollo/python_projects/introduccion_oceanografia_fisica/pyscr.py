import numpy as np
import matplotlib.pyplot as plt

# Velocidad inicial
Vh = 1

# Parámetro de Coriolis
lat = 70 * (np.pi / 180)
Om = 2 * np.pi / (24 * 3600)
f = 2 * Om * np.sin(lat)

# Generar un tiempo inicialmente aleatorio
Ti = 32 * 3600  # horas en segundos
t = np.arange(1, Ti + 1)

# Calculo de las corrientes inerciales
u = Vh * np.sin(f * t)
v = Vh * np.cos(f * t)

x = np.repeat(10, len(u))
y = np.repeat(10, len(u))
a = np.arange(0, len(x), 1200)

# Gráfico de u y v
plt.figure()
plt.plot(u, v, 'r')
plt.xlabel('Componente u')
plt.ylabel('Componente v')
plt.axis('equal')
plt.axis([-1.2, 1.2, -1.2, 1.2])
plt.title('Gráfico de u y v')
plt.show()

# Gráfico de quiver
plt.figure()
plt.quiver(x[a], y[a], u[a], v[a])
plt.title('Gráfico de vectores de corriente inercial')
plt.show()