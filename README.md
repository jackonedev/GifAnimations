# GifAnimations
<br />
Directorio de trabajo durante desarrollo de la aplicación solicitada por el cliente.<br />
<br />
La primera versión de la app se encuentra en el repositorio: <b>https://github.com/jackonedev/GifAnimationsAPP/tree/main</b><br />
Dicha versión es la que se accede desde <b>01-data-animation/app</b><br />
Dicha versión utiliza un método de inspección visual de forma manual para seleccionar features, basandose en una categorización dada por intervalos discretos.<br />
<br />
En <b>02-data-processing/</b> justamente se buscó encontrar otros métodos de identificación de features.<br />
Primero se optó por una categorización mediante identificación de patrones por cluster <b>DBScan</b>.<br />
Segundo se optó por una categorización mediante <b>cluster jerarquizado</b>.<br />
Esos dos criterios están contemplados en el fichero: <b>01_corr_spearman.ipynb</b><br />
Luego se optó por implementar por medio de <b>Seaborn</b> distintos gráficos heatmap.<br />
Eso se realizó en el fichero llamado <b>02_exploracion_muestras.ipynb</b><br />
Primero se prueba el heatmap por default,<br />
segundo una con un formato personalizado,<br />
y por último un <b>heatmap con dendograma</b> incluido.<br />
<br />
En <b>03-appV2/</b> se realizó una versión de la app realizada en <b>01-data-animation/app</b><br />
Esta versión en vez de correr sobre jupyter notebook es una app que corre por <b>CLI</b><br />
Es decir, una aplicación con interface para usuario final.<br />
yt: <b>https://youtu.be/fr-4EJBEYWw</b>

