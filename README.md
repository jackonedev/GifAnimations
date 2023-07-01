# GifAnimations

Directorio de trabajo durante desarrollo de la aplicación solicitada por el cliente.

La primera versión de la app se encuentra en el repositorio: **https://github.com/jackonedev/GifAnimationsAPP/tree/main**
Dicha versión es la que se accede desde **01-data-animation/app**
Dicha versión utiliza un método de inspección visual de forma manual para seleccionar features, basandose en una categorización dada por intervalos discretos.

En **02-data-processing/** justamente se buscó encontrar otros métodos de identificación de features.
Primero se optó por una categorización mediante identificación de patrones por cluster **DBScan**.
Segundo se optó por una categorización mediante **cluster jerarquizado**.
Esos dos criterios están contemplados en el fichero: **01_corr_spearman.ipynb**
Luego se optó por implementar por medio de **Seaborn** distintos gráficos heatmap.
Eso se realizó en el fichero llamado **02_exploracion_muestras.ipynb**
Primero se prueba el heatmap por default,
segundo una con un formato personalizado,
y por último un **heatmap con dendograma** incluido.

En **03-appV2/** se realizó una versión de la app realizada en **01-data-animation/app**
Esta versión en vez de correr sobre jupyter notebook es una app que corre por **CLI**
Es decir, una aplicación con interface para usuario final.
yt: https://youtu.be/fr-4EJBEYWw

