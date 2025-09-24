

---

## Requisitos

* Python 3.8+ 
* duckdb  - la librería Python 
* n8n (para importar y ejecutar el workflow (docker))
* Git 

---

## Preparación (activar entorno y dependencias)

1. Clona el repositorio (si aplica):

```
git clone https://github.com/ElRicky17/Entrevista-Shadowlights.git

```

2. Crear y activar entorno virtual:

```bash


# Windows PowerShell
# py -m venv venv
# .\venv\Scripts\Activate


```

3. Instalar dependencias (pip install)
```
duckdb
pandas
```

---

## Comandos numerados (qué ejecutar)

**Punto 1**

* py crear_tabla.py
* py cargar_Datos.py

**Punto 2**

* py kpi_modeling.py  

**Punto 3**

* py metrics_access.py --start 2025-06-01 --end 2025-06-30


**Punto 4**
* Ejecutar todas las boxes o una por una en el archivo .ipynb

---

