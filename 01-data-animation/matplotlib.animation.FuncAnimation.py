"""
matplotlib.animation


Es una librería muy útil para la creación de animaciones en Python utilizando Matplotlib.
La principal función se llama "FuncAnimation" que exploraremos a continuacion.
"""

import matplotlib
import matplotlib.pyplot as plt


fig = plt.figure()

def func():
    pass

matplotlib.animation.FuncAnimation(
                        fig, func, frames=None, init_func=None, 
                        fargs=None, save_count=None, interval=200, 
                        repeat_delay=None, repeat=True, blit=False
                        )


"""

>>  Parámetros de FuncAnimation:

fig: objeto matplotlib.figure.Figure
func: type function
frame: secuencia de números enteros, o un iterable, o una funcion que devuelva un iterador, default=None=range(num_frames) default=None=range(num_frames)/num_frames:cantidad de cuadros de la animacion
init_func: 
fargs: tupla de elementos adicionales que se enviara al parametros func
save_count: Es el numero de cuadros que se guardaran. default:toda la animacion
interval: Es el tiempo en milisegundos entre cuadros de la animacion
repeat_delay: Es el tiempo de retraso antes que se repita la animacion [ms]
repeat[bool]: indica si la animacion debe repetirse al finalizar
blit[bool]: indica si se debe utilizar el metodo blit para optimizar la animacion


>>  Guardar la animacion

Es importante destacar que FuncAnimation devuelve un objeto animation, que es necesario guardar para poder mostrar la animacion.
Esto se puede hacer llamando a la funcion HTML  de IPython.display para ver la animacion en una notebook o guardandola en un archivo utilizando la funcion save del objeto animation


>>  Parametros frames y save_count=MAX_FRAMES:

frames: este parametro define los cuadros que se utilizaran para la animacion.
Puede ser objeto tipo lista, una matriz, o un generador de datos que produce los cuadros para la animacion.
Por ejemplo, si estamos en una animacion de una simulacion de fisica, los frames podrian ser una lista de los estados de la simulacion en diferentes momentos de tiempo.

MAX_FRAMES: es el valor que toma el parametro save_count. Este define el numero maximo de cuadros que se guardaran en la animacion.
Es importante definir MAX_FRAMES para evitar que la animacion tenga un tamaño de archivo demasiado grande o que consuma demasiada memoria RAM.
Una buena estrategia para establer MAX_FRAMES es un numero que sea un poco mayor que el numero de cuadros que se espera reproducir en la animacion.
Por ejemplo, si se espera tener 120 cuadros, se podrá establecer un MAX_FRAMES de 150 para tener margen de seguridad.





"""





