import numpy as np
import matplotlib.pyplot as plt

# Cálculo del estrés del viento
rhoa = 1.25  # densidad del aire
Cd = 2.3e-3  # Coeficiente de arrastre
W10 = 10  # m/s velocidad del viento
Tw = rhoa * Cd * W10**2

# Cálculo de Coriolis
lat = 60 * (np.pi / 180)  # latitud
Om = 2 * np.pi / (24 * 3600)
f = 2 * Om * np.sin(lat)

# Grosor de la capa de Ekman
Az = 5e-3  # viscosidad turbulenta
De = np.pi * np.sqrt((2 * Az) / f)

# Velocidad superficial 
rhow = 1027  # densidad del agua de mar
Vo = (np.sqrt(2) * np.pi * Tw) / (rhow * f * De)

# Definición del vector de velocidad
dz = 0.5
z = -1 * np.arange(0, 2 * np.ceil(De) + dz, dz)

u = Vo * np.exp((np.pi * z) / De) * np.cos((np.pi / 4) - ((np.pi * z) / De))
v = -Vo * np.exp((np.pi * z) / De) * np.sin((np.pi / 4) - ((np.pi * z) / De))
V = np.sqrt(u**2 + v**2)

Ut = np.sum(u) * dz
Vt = np.sum(v) * dz

# Gráficas
plt.figure()
plt.plot(V, z, 'k.-', label='V')
plt.plot(u, z, 'k.-', label='u')
plt.plot(v, z, 'b.-', label='v')
plt.legend()
plt.grid()
plt.axis([-Vo, Vo, np.min(z), 0])
plt.xlabel('Velocidad')
plt.ylabel('Profundidad')
plt.title('Perfil de Velocidad en la Capa de Ekman')
plt.show()

# Gráfica 3D
fig = plt.figure()
ax = fig.add_subplot(111, projection='3d')
ax.plot3D(u, v, z, '.r')
ax.grid()
ax.set_xlabel('u')
ax.set_ylabel('v')
ax.set_zlabel('z')
plt.title('Perfil de Velocidad en 3D')
plt.show()

# Gráfica de vectores
x = np.repeat(10, len(u))
y = np.repeat(10, len(u))

plt.figure()
plt.quiver(x, y, u, v)
plt.quiver(x[0], y[0], Ut * 0.5, Vt * 0.5, color='r')
plt.title('Vector de Velocidad Superficial')
plt.show()
