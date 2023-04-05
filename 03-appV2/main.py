import numpy as np
import pandas as pd
import pickle
import matplotlib.pyplot as plt

from pypackage.data_prepare import check_type_dt, data_info
from pypackage.ingresar_datos import ingreso_bool, ingreso_numerico
from pypackage.data_feed import plot_data, apply_dark_mode


from rich.console import Console
from rich.table import Table



def data_feed():
    global file_name, df
    global hack
    file_name = input('File name: ')
    hack = False
    if file_name.endswith('+') and file_name.count('+')==1:
        hack = True
        file_name = file_name[:-1]
    if not file_name.endswith('csv'):
        file_name += '.csv'
    try:
        df = pd.read_csv('data/' + file_name)
    except:
        print('File not found')
        exit()
    return data_prepare(df)

def data_prepare(df):
    df = check_type_dt(df)
    df = df.apply(lambda col: pd.to_numeric(col, errors='ignore'))
    if hack:
        with open('data/{}-processed.pkl'.format(file_name), 'wb') as f:
            pickle.dump(df, f)
    return df

def data_present():
    global console, df_col

    console = Console()
    df_col = data_info(df)
    table = Table(title="Data variables information: {} |\n shape: {}".format(file_name, df.shape))

    table.add_column("id", justify="right", style="cyan", no_wrap=True)
    table.add_column("Variable name", style="cyan")
    table.add_column("type", justify="right", style="cyan")
    table.add_column("unique", justify="right", style="cyan")
    table.add_column("nans", justify="right", style="cyan")

    id = pd.Series(list(range(1, df.shape[1]+1))).values.astype(str)
    name = df_col['columna'].values.astype(str)
    dtype = df_col['dtype'].values.astype(str)
    unique = df_col['count_unique'].values.astype(str)
    nan = df_col['Nan'].values.astype(str)

    for i in range(len(df_col)):
        table.add_row(id[i], name[i], dtype[i], unique[i], nan[i])
    console.print(table)
    return df_col

def animation_variable():
    global ani_var
    def id_input():
        ani_id = input('Variable to visualize (select id): ')
        if not ani_id.isnumeric():
            print('Please select a number')
            exit()
        ani_id = int(ani_id)
        if ani_id > len(df_col):
            print('Please select a valid id')
            exit()
        if ani_id == 0:
            print('Exiting by presing 0')
            exit()
        return ani_id

    ani_id = id_input()
    label = df_col.iloc[ani_id-1, 1]
    ani_var = df[label]
    return ani_var

def confirmation(string):
    print('Variable selected: {}'.format(string))
    confirm = ingreso_bool('Confirm variable?')
    if confirm == False:
        print('Excting by user')
        exit()
    return confirm



def main():
    global file_name, df, console, df_col, ani_var
    df = data_feed()
    df_col = data_present()
    print ('Press 0 to exit')
    ani_var = animation_variable()
    if not confirmation(ani_var.name):
        exit()

    apply_dark_mode()
    if not ingreso_bool('Select Dark Mode?'):
        plt.style.use('ggplot')


    print ('Please input animation params / the loading could take a few seconds')
    ani = plot_data(data = ani_var,
                    title = '',#TODO
                    title_y = input('Label y axis: '),
                    grid_y = ingreso_numerico('Grid y axis: '),
                    fps = ingreso_numerico('Frames per second: '),

                    repeat = ingreso_bool('Repeat animation: '),
                    cache = ingreso_bool('Cache animation: ')#TODO:window
                    )
    plt.show(block=True)

if __name__ == '__main__':
    main()