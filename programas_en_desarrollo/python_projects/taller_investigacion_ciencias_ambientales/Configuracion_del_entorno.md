# Entornos de trabajo Python.

### Crear un entorno de python con una versión en particular:

```bash
    conda create --name <environment_name> python=X.X
```
### Activar el entorno:

```bash
    conda activate <environment_name> 
```

### Desactivar el entorno:

```bash
    conda deactivate
```

### Instalar bibliotecas de python dentro del entorno de trabajo:

```bash
    conda install <library_name_1> <library_name_2> ... <library_name_n>
```

### Exportar entorno de python para usar en diversos sistemas operativos:

```bash
    conda env export --from-history > environment.yml
```

### Crear un entorno a partir de un archivo environment.yml:

```bash
    conda env create -f environment.yml
```

### Actualizar un entorno:

```bash
    conda env update --file environment.yml --prune
```

### Eliminar un entorno:

```bash
    conda remove --name <environment_name> --all
```

---

## Tutorial Completo: Entornos de Trabajo en Python con Conda

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
conda create --name mi_proyecto_tensorflow python=3.9
```

#### Activación del entorno
```bash
conda activate <nombre_entorno>
```
Una vez activado, el símbolo del sistema mostrará el nombre del entorno activo.

#### Desactivación del entorno
```bash
conda deactivate
```

#### Instalación de bibliotecas
```bash
conda install <biblioteca1> <biblioteca2> ...
```
**Ejemplo:**
```bash
conda install numpy pandas matplotlib
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
   conda create --name mi_proyecto_ml python=3.8
   ```
2. **Activar el entorno:**
   ```bash
   conda activate mi_proyecto_ml
   ```
3. **Instalar las bibliotecas necesarias:**
   ```bash
   conda install numpy pandas scikit-learn tensorflow
   ```
4. **Exportar el entorno a un archivo:**
   ```bash
   conda env export --from-history > environment.yml
   ```
5. **Compartir el proyecto con un colaborador:**
   Envíale el archivo `environment.yml` y que lo ejecute para crear el mismo entorno en su máquina.

### Consideraciones adicionales
* **Virtualenv:** Otra herramienta popular para crear entornos virtuales en Python.
* **Conda vs. pip:** Conda puede gestionar tanto paquetes Python como otros paquetes binarios, mientras que pip se enfoca en paquetes Python.
* **Entornos globales vs. locales:** Los entornos globales afectan a todo el sistema, mientras que los entornos locales están aislados.

**¡Con este tutorial, estarás listo para crear y gestionar entornos de trabajo en Python de manera eficiente!**

**¿Te gustaría profundizar en algún tema específico?** Por ejemplo, puedo explicar cómo resolver conflictos de versiones entre bibliotecas, cómo utilizar diferentes canales de conda, o cómo integrar entornos de trabajo con herramientas de desarrollo como Jupyter Notebook.
