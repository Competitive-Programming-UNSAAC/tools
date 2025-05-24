# Cálculo de Ranking

Este script calcula el **ranking de estudiantes** de los diferentes procesos de selectiva.

## Puntaje de Posición en el Concurso Selectivo

Para cada estudiante `s`, este puntaje considera la posición en el **Concurso Selectivo**:

```math
PuntajePosiciónConcurso_s = \left( { EquiposTotalesConcurso - PosiciónConcurso_s + 1 \over EquiposTotalesConcurso }  \right) \left( PesoPosiciónConcurso \right)
```

## Puntaje de Rating de Codeforces

Si `n` estudiantes están participando en la selección. Para cada estudiante `s`, este puntaje será la **información de rating de Codeforces obtenida por el estudiante en los diferentes concursos en línea**.

```math
RatingCodeforcesMaximo = \max_{1 \leq s \leq n} \left( RatingCodeforces_s \right)
```

```math
PuntajeRatingCodeforces_s = \left( { RatingCodeforces_s \over RatingCodeforcesMaximo }  \right) \left( PesoRatingCodeforces \right)
```

## Puntaje de Problemas Resueltos en Codeforces

Si `n` estudiantes están participando en la selección y un estudiante resolvió `p` problemas en Codeforces. 

Para cada estudiante `s`, este puntaje se calculará considerando el número de problemas resueltos y el rating de cada problema, es decir, **los problemas difíciles dan más puntos que los problemas fáciles**.

Aquellos **problemas de Gym que fueron resueltos durante el concurso de entrenamiento debido a que no tienen un rating serán considerados con un rating de 1000 puntos**.

```math
RatingTotalProblemasResueltos_s = \sum_{k=1}^p RatingProblemaResuelto_k 
```

```math
RatingTotalProblemasResueltosMaximo = \max_{1 \leq s \leq n} \left( RatingTotalProblemasResueltos_s \right)
```

```math
PuntajeRatingProblemasResueltos_s = \left( {RatingTotalProblemasResueltos_s \over RatingTotalProblemasResueltosMaximo }  \right) \left( PesoRatingTotalProblemasResueltos \right)
```

## Ranking con Categorias

Informaciones a considerar con su respectivo **peso** que puede ser editado en el archivo de configuración:

- Posición en el **Concurso Selectivo** (70 pts)
- Número de problemas resueltos en codeforces (20 pts)
- Rating de Codeforces (10 pts)

### Puntos Totales

Para cada estudiante `s`, la cantidad total de puntos es:

```math
PuntajeTotal_s = PuntajePosiciónConcurso_s + PuntajeRatingCodeforces_s + PuntajeRatingProblemasResueltos_s
```

### Reglas de Selección

Teniendo esto en cuenta, **habrá N cupos disponibles** y se llenarán de la siguiente manera:

- _Categoría A_: **A cupos** se llenarán con estudiantes que tengan **más de 110 créditos acumulados** (del 6º semestre en adelante).

- _Categoría B_: **B cupos** se llenarán con estudiantes que tengan **110 créditos acumulados o menos** (del 1er semestre al 5º semestre).

- _Categoría W_: **W cupo** se llenará con una **estudiante mujer**, la estudiante puede ser de **_Categoría A_** o **_Categoría B_**

Para cada una de las categorías mencionadas anteriormente, el proceso de selección será el siguiente:

1. Los cupos se llenarán **teniendo en cuenta el ranking** generado.

2. Si un estudiante **no cumple con los requisitos**, el cupo será **asignado al siguiente en el ranking**.

3. Si **no hay más estudiantes en el ranking para esa categoría**, el cupo será **asignado a otra categoría** siguiendo el orden **_Categoría A_**, **_Categoría B_** y **_Categoría W_**. Eso significa que el proceso de selección se repetirá.

**_El estudiante debe tener en cuenta que una vez que acepta el cupo, está de acuerdo en participar en el evento. Si el estudiante tiene dudas, debe considerar dar la oportunidad a otros estudiantes._**

## Ranking Unico

Informaciones a considerar con su respectivo **peso** que puede ser editado en el archivo de configuración:

- Posición en el **Concurso Selectivo** (90 pts)
- Número de problemas resueltos en codeforces (10 pts)

### Puntos Totales

Para cada estudiante `s`, la cantidad total de puntos es:

```math
PuntajeTotal_s = PuntajePosiciónConcurso_s + PuntajeRatingProblemasResueltos_s
```

### Reglas de Selección

Teniendo esto en cuenta, **habrá N cupos disponibles** y se llenarán de la siguiente manera:

1. Los cupos se llenarán **teniendo en cuenta el ranking** generado.

2. Si un estudiante **no cumple con los requisitos**, el cupo será **asignado al siguiente en el ranking**.

**_El estudiante debe tener en cuenta que una vez que acepta el cupo, está de acuerdo en participar en el evento. Si el estudiante tiene dudas, debe considerar dar la oportunidad a otros estudiantes._**

## Compromiso y Requisitos de Selección

Para la selección, los estudiantes deben tener en cuenta los siguientes `requisitos`:

1. El estudiante debe **tener en cuenta que faltará a clases** en diferentes cursos durante el evento. Además, **al regresar, el estudiante debe completar todas las tareas y exámenes pendientes** del curso.

2. Se solicitará apoyo financiero a la universidad. Sin embargo, no todos los gastos del evento serán cubiertos, el estudiante **debe cubrir los gastos con su propio dinero (boletos de transporte, alojamiento y comida)**.

3. En caso de que el estudiante tenga apoyo financiero de la universidad, **al regresar, el estudiante debe reportar a la universidad los gastos incurridos**.

4. En caso de que el estudiante tenga apoyo financiero de la universidad, **al regresar, el estudiante debe participar de los eventos de programación competitiva y contribuir con su conocimiento obtenido para los otros estudiantes i.e (clases, contests, eventos). Estudiantes egresados con 200 creditos o más no son elegibles ya que poseen poco tiempo libre.**.

## Formato del documento

El documento CSV con los datos para calcular el ranking debe tener el siguiente formato:

| Id | Nombre | Género | Handle de Codeforces | Créditos | Semestre | Registrado en el Concurso | Posición en el Concurso |
| - | - | - | - | - | - | - | - |
| 204321 | Yishar Piero Nieto Barrientos | Masculino | theFixer | 175 | 8 | Sí | 1 |
| 231447 | Rosy Aurely Montalvo Solórzano | Femenino | LittleProgramer4 | 43 | 3 | Sí | 2 |
| 215733 | Jhon Efrain Quispe Chura | Masculino | zero_speed | 26 | 2 | No | 3 |

## Archivo de Configuración

El archivo `Config` contiene información sobre:

- Formato de las columnas del documento
- Pesos asignados a cada tipo de información
- Información sobre el número de equipos participantes en el Cuscotest

## Instalar dependencias

Instale las dependencias del archivo `requirements.txt` con el siguiente comando:

```bash
pip install -r requirements.txt
```

## Comando para ejecutar

Para ejecutar el script, es necesaria la ruta al documento CSV que se envía a través de los parámetros.

En este sentido, el comando para ejecutar el script es el siguiente:



```bash
python3 ranking.py [data-filepath] [output-filepath] [config-filepath]

# Ejemplo:
python3 ranking.py training-camp-argentina-2024/registered.csv training-camp-argentina-2024 Config
```