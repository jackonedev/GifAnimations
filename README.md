# GifAnimations
<br />
Directorio de trabajo durante desarrollo de la aplicación solicitada por el cliente.<br />
<br />
La primera versión de la app se encuentra en el repositorio: **https://github.com/jackonedev/GifAnimationsAPP/tree/main**<br />
Dicha versión es la que se accede desde **01-data-animation/app**<br />
Dicha versión utiliza un método de inspección visual de forma manual para seleccionar features, basandose en una categorización dada por intervalos discretos.<br />
<br />
En **02-data-processing/** justamente se buscó encontrar otros métodos de identificación de features.<br />
Primero se optó por una categorización mediante identificación de patrones por cluster **DBScan**.<br />
Segundo se optó por una categorización mediante **cluster jerarquizado**.<br />
Esos dos criterios están contemplados en el fichero: **01_corr_spearman.ipynb**<br />
Luego se optó por implementar por medio de **Seaborn** distintos gráficos heatmap.<br />
Eso se realizó en el fichero llamado **02_exploracion_muestras.ipynb**<br />
Primero se prueba el heatmap por default,<br />
segundo una con un formato personalizado,<br />
y por último un **heatmap con dendograma** incluido.<br />
<br />
En **03-appV2/** se realizó una versión de la app realizada en **01-data-animation/app**<br />
Esta versión en vez de correr sobre jupyter notebook es una app que corre por **CLI**<br />
Es decir, una aplicación con interface para usuario final.<br />
yt: https://youtu.be/fr-4EJBEYWw

