# def version_mat(filepath):
#     with open(filepath, 'rb') as f:
#         header = f.read(128).decode('latin-1', errors='ignore')
#         if 'HDF5' in header or '\x89HDF' in open(filepath,'rb').read(4).decode('latin-1', errors='ignore'):
#             print("Versión 7.3 → usar h5py")
#         else:
#             print("Versión <7.3 → usar scipy.io.loadmat")

# version_mat('S100629A011_IslArena_1.mat')
import scipy.io
import numpy as np
import pandas as pd
import matplotlib.pyplot as plt

datos = scipy.io.loadmat('S100629A011_IslArena_1.mat', squeeze_me=True, struct_as_record=False)

datosData = datos['Data']

t1 = datosData.Average_Time;
t = pd.to_datetime(t1 - 719529, unit='D', origin='unix')
bat = datosData.Average_Battery
head = datosData.Average_Heading
pitch = datosData.Average_Pitch
roll = datosData.Average_Roll

temp = datosData.Average_Temperature
press = datosData.Average_Pressure

u = datosData.Average_VelEast
v = datosData.Average_VelNorth
w = datosData.Average_VelUp1

cor1 = datosData.Average_CorBeam1
cor2 = datosData.Average_CorBeam2
cor3 = datosData.Average_CorBeam3
cor4 = datosData.Average_CorBeam4

depth = np.arange(0.3,5.5,0.2)

fig, axes = plt.subplots(3, 1, figsize=(12, 8))

# Batería
axes[0].plot(t, bat)
axes[0].set_ylabel('Bateria')
axes[0].set_xlabel('Tiempo')
axes[0].set_title('Orientación del ADCP en la medición')
axes[0].grid(True)

# Heading
axes[1].plot(t, head, 'b')
axes[1].set_ylabel('Heading (°)')
axes[1].set_xlabel('Tiempo')
axes[1].grid(True)

# Pitch & Roll
axes[2].plot(t, pitch, 'r', label='Pitch')
axes[2].plot(t, roll, 'g', label='Roll')
axes[2].set_ylabel('Inclinación (°)')
axes[2].set_xlabel('Tiempo')
axes[2].legend(loc='best')
axes[2].grid(True)

plt.tight_layout()
plt.savefig('adcp_orientation.png')

fig, axes = plt.subplots(2, 1, figsize=(12, 8))

# Presión
axes[0].plot(t, press, 'b')
axes[0].set_ylabel('Presión')
axes[0].set_xlabel('Tiempo')
axes[0].set_title('Variación temporal de la presión y la temperatura')
axes[0].grid(True)

# Temperatura
axes[1].plot(t, temp, 'r')
axes[1].set_ylabel('Temperatura (°)')
axes[1].set_xlabel('Tiempo')
axes[1].grid(True)

plt.tight_layout()
plt.savefig('adcp_temperatura_y_presion.png')

# Velocidad
fig, ax = plt.subplots(figsize=(12, 8))

c = ax.pcolormesh(t, depth, v.T, shading='nearest')
plt.colorbar(c, ax=ax)
ax.set_xlabel('Tiempo')
ax.set_ylabel('Profundidad')
ax.set_title('Componente V (Norte-Sur)')

plt.tight_layout()
plt.savefig('Componente_v_norte-sur.png')

# Correlación
fig, ax = plt.subplots(figsize=(12, 8))

c = ax.pcolormesh(t, depth, cor1.T, shading='nearest')
plt.colorbar(c, ax=ax)
ax.set_xlabel('Tiempo')
ax.set_ylabel('Profundidad')
ax.set_title('Gráfico de correlación')

plt.tight_layout()
plt.savefig('grafico_correlacion.png')
