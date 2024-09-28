## Scoreboard

Este script muestra el **scoreboard** a partir de un archivo CSV

## Formato del documento

El documento CSV con los datos para el scoreboard debe tener el siguiente formato:

- `1` : Problema resuelto
- `-1` : Intento fallido
- `0` : Problema no resuelto

| Id | Nombre | Usuario de Codeforces | Penalización | A | B | C |
| - | - | - | - | - | - | - |
| 204321 | Yishar Piero Nieto Barrientos | theFixer | 26 | 1 | 1 | 1 |
| 231447 | Rosy Aurely Montalvo Solórzano | LittleProgramer4 | 28 | 1 | 1 | -1 |
| 215733 | Jhon Efrain Quispe Chura | zero_speed | 30 | 1 | -1 | 0 |

## Archivo de configuración

El archivo `Config` contiene información sobre:

- Formato de las columnas del documento
- Columnas de problemas del documento
- Número de problemas

## Instalar dependencias

Instale las dependencias del archivo `requirements.txt` con el siguiente comando:

```bash
pip install -r requirements.txt
```

## Ejecutar script

Para ejecutar el script, es necesario la ruta al documento CSV que se envía a través de los parámetros.

En este sentido, el comando para ejecutar el script es el siguiente:

``` bash
pyhton3 scoreboard.py [data-filepath] [output-filepath] [config-filepath]

# Ejemplo:
python3 scoreboard.py training-camp-argentina-2024/scoreboard.csv training-camp-argentina-2024 Config
```
