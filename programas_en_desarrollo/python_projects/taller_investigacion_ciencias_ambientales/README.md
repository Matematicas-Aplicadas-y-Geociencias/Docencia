## Entornos de Trabajo en Python con Conda

### ¿Qué es un entorno de trabajo en Python?
Un entorno de trabajo en Python es un directorio aislado que contiene una instalación específica de Python, junto con las bibliotecas y paquetes que se requieren para un proyecto en particular. Esto permite mantener diferentes proyectos con diferentes versiones de Python y bibliotecas sin que se produzcan conflictos.

### ¿Por qué usar entornos de trabajo?
* **Aislamiento de proyectos:** Cada proyecto tiene sus propias dependencias, evitando conflictos entre versiones.
* **Reproducibilidad:** Puedes compartir fácilmente tu entorno con otros, garantizando que todos trabajen con la misma configuración.
* **Gestión de versiones:** Puedes experimentar con diferentes versiones de Python y bibliotecas sin afectar tu sistema global.

### Utilizando Conda para gestionar entornos
Conda es una herramienta de gestión de paquetes y entornos que facilita enormemente la creación y administración de entornos de Python.

#### Creación de un entorno
```bash
conda create --name <nombre_entorno> python=X.X
```
* **--name <nombre_entorno>:** Especifica el nombre que deseas asignar a tu entorno.
* **python=X.X:** Indica la versión exacta de Python que deseas instalar.

**Ejemplo:**
```bash
conda create --name mi_proyecto_unam python=3.10
```

#### Activación del entorno
```bash
conda activate <nombre_entorno>
```
Una vez activado, el símbolo del sistema mostrará el nombre del entorno activo.

Por ejemplo:
```
(nombre_entorno) directorio_del_proyecto $
```

#### Desactivación del entorno
```bash
conda deactivate
```

#### Ver los entornos existentes
Para ver los entornos que se han creado:
```bash
conda info --envs
```
o también:
```bash
conda env list
```
en ambos casos, te debe dar una respuesta similar a la siguiente:
```shell
# conda environments:
#
base                 *  /home/username/anaconda3/envs/myenv
enes_env                /home/username/anaconda3/envs/snowflakes
exam                    /home/username/anaconda3/envs/bunnies
```
El `*` indica el entorno que está activo.

#### Instalación de bibliotecas
```bash
conda install <biblioteca_1>  <biblioteca_2> ...
```
**Ejemplo:**
```bash
conda install numpy scipy matplotlib
```

#### Exportación del entorno
```bash
conda env export --from-history > environment.yml
```
Este comando crea un archivo `environment.yml` que contiene una lista de todos los paquetes y sus versiones instaladas en el entorno.

#### Creación de un entorno a partir de un archivo `environment.yml`
```bash
conda env create -f environment.yml
```
Este comando crea un nuevo entorno con las mismas especificaciones que se encuentran en el archivo `environment.yml`.

#### Actualización de un entorno
```bash
conda env update --file environment.yml --prune
```
Este comando actualiza todos los paquetes en el entorno a las versiones especificadas en el archivo `environment.yml` y elimina los paquetes que ya no son necesarios.

#### Eliminación de un entorno
```bash
conda remove --name <nombre_entorno> --all
```

### Ejemplo completo
1. **Crear un entorno para un proyecto de aprendizaje automático:**
   ```bash
   conda create --name enes_env python=3.11
   ```
2. **Activar el entorno:**
   ```bash
   conda activate enes_env
   ```
3. **Instalar las bibliotecas necesarias:**
   ```bash
   conda install numpy scipy matplotlib jupyterlab
   ```
4. **Exportar el entorno a un archivo:**
   ```bash
   conda env export --from-history > environment.yml
   ```
5. **Compartir el proyecto con un colaborador:**  
   Comparte el archivo `environment.yml` y que lo ejecute para crear el mismo entorno en su máquina.
