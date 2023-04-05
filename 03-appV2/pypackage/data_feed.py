import numpy as np
import pandas as pd
from collections import deque
from matplotlib.animation import FuncAnimation
import matplotlib.pyplot as plt
import matplotlib.dates as mdates
import datetime as dt

plt.ion()



def create_frame(drop_elements:list, dy:deque,) -> pd.DataFrame:#TODO: cambiar el nombre de los parámetros
    lista_frames = []
    while len(drop_elements) > 0:
        dy.append(drop_elements.pop())
        lista_frames.append(dy.copy())
    return lista_frames

def build_frames(data: pd.DataFrame, label: str, window:int=0) -> pd.DataFrame:
    """Storage all the results of processing the deque object
    Also, create global variables por axis formating
    """
    global y_lim_max, y_lim_min

    y_lim_max = data[label].max()
    y_lim_min = data[label].min()
    repeat=True
    if not window:
        window = len(data)
        repeat = False
    #
    if repeat:
        drop_elements = list(data[label].values)[-2::-1]
        dy = deque(data[label].values, maxlen=len(data))
    else:
        if isinstance(data[label].iloc[0], pd._libs.tslibs.timestamps.Timestamp):
            # print ('ISO 8601: YYYY-MM-DDThh:mm:ss.ss')
            dy = deque(np.zeros(window), maxlen=window)
        else:
            dy = deque(np.zeros(window), maxlen=window)
        drop_elements = list(data[label].values)[-1::-1]
    #
    lista_frames = create_frame(drop_elements, dy)
    row_keys = [f'{i}' for i in range(window)]
    return pd.DataFrame(lista_frames, columns=row_keys)

def plot_data(data: pd.Series, title=None, title_y=None, grid_y=3, fps=24, repeat=True, cache=False, window=None):#TODO: title
    fig, ax = plt.subplots()
    line, = ax.plot([], [])
    interval = 1000/fps
    label = data.name
    if title:
        plt.title(title)
    if not title_y:
        title_y = label
    
    dx = build_frames(data.reset_index(), data.reset_index().columns[0], window=window)
    dxt = pd.to_datetime(dx.iloc[-1])

    hours = dxt.dt.time.apply(lambda t: t.hour)
    minutes = dxt.dt.time.apply(lambda t: t.minute)
    seconds = dxt.dt.time.apply(lambda t: t.second)

    days = dxt.dt.day
    months = dxt.dt.month
    years = dxt.dt.year

    fechas = False
    if all(h == 0 and m == 0 and s == 0 for h, m, s in zip(hours, minutes, seconds)):
        print("Temporalidad MAYOR")
        dx = dx.replace(0, pd.Timestamp('00:00:00')).applymap(lambda x: x.to_pydatetime().strftime('%d-%m-%Y'))
        fechas = True
    elif len(days.unique()) == 1 and len(months.unique()) == 1 and len(years.unique()) == 1:
        print ('Temporalidad inferior')
        if any(hours):
            print("El eje x dinámico no contempla horas")
        dx = dx.replace(0, pd.Timestamp('00:00:00')).applymap(lambda x: x.to_pydatetime().strftime('%M:%S'))
    else:
        print("El dataframe posee variación tanto en sus fechas, como en el tiempo, y el eje x dinámico no ha sido desarrollado para ese escenario.\nSaliendo del programa")
        exit()

    df = build_frames(data.to_frame(), data.name, window=window)


    def update(i):
        date = dx.iloc[i]
        frame = df.iloc[i]
        index_min = int(date[frame !=0].index[0])
        eje_x = date.loc[:str(int(index_min)-1)].index.to_list() + date.iloc[int(index_min):].to_list()
        frame.index = eje_x

        ax.clear()
        line, = ax.plot(frame, linewidth=1)
        ax.set_ylim(y_lim_min, y_lim_max)
        ax.set_yticks(np.linspace(y_lim_min, y_lim_max, grid_y))


        #
        def axis_time():
            if i < 180:
                ax.set_xticks(eje_x[-1])
            elif i < 600:
                lista_eje_x = []
                lista_eje_x.append(eje_x[-181])
                lista_eje_x.append(eje_x[-1])
                ax.set_xticks(lista_eje_x)
            else:
                lista_eje_x = []
                lista_eje_x.append(eje_x[-181])
                lista_eje_x.append(eje_x[-1])
                lista_eje_x.append(eje_x[-i-1])
                lista_eje_x.append(eje_x[-len(eje_x[-i-1:-180])//2-180])
                ax.set_xticks(lista_eje_x)

        def axis_date():
            lista_eje_x = []
            mes_anterior = None
            for ix, fecha in enumerate(eje_x):
                fecha_split = fecha.split('-')
                if len(fecha_split) < 2:
                    continue
                mes_actual = int(fecha_split[1])
                if mes_actual != mes_anterior:
                    lista_eje_x.append(ix)
                mes_anterior = mes_actual

            ax.set_xticks(lista_eje_x)
            ax.tick_params(axis='x', labelrotation=45)

        if fechas == True:
            axis_date()
        else:
            axis_time()
        #
        ax.set_xlabel('Time')
        ax.set_ylabel(title_y)
        plt.tight_layout()
        
        return line, 
    return FuncAnimation(fig, update, frames=len(df), interval=interval, blit=False, repeat=repeat, cache_frame_data=cache)





def apply_dark_mode():
    """https://matplotlib.org/3.5.0/tutorials/introductory/customizing.html
    https://matplotlib.org/3.1.1/tutorials/colors/colors.html"""

    import matplotlib.pyplot as plt
    from matplotlib import cycler

    # import matplotlib as mpl

    colors = cycler(
        "color", ["#669FEE", "#66EE91", "#9988DD", "#EECC55", "#88BB44", "#FFBBBB"]
    )

    plt.rc("figure", facecolor="#313233")
    plt.rc(
        "axes",
        facecolor="#313233",
        edgecolor="none",
        axisbelow=True,
        grid=True,
        prop_cycle=colors,
        labelcolor="0.81",
    )

    plt.rc("grid", color="474A4A", linestyle="--", alpha=0.7)
    plt.rc("xtick", color="0.81", labelsize=12)
    plt.rc("ytick", direction="out", color="0.81", labelsize=12)
    plt.rc("legend", facecolor="#313233", edgecolor="#313233")
    plt.rc("text", color="#C9C9C9")

    plt.rcParams["axes.grid.which"] = "major" 
    plt.rcParams["axes.grid.axis"] = "y"
