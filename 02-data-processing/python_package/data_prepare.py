import pandas as pd
import pickle

def data_info(data, name="data"):
    """Funcion que devuelve informacion de un DataFrame en formato tipo DataFrame"""
    df = pd.DataFrame(pd.Series(data.columns))
    df.columns = ["columna"]
    df.columns.name = f"info de {name}"
    # df.index.name = 'index'
    df["Nan"] = data.isna().sum().values
    df["pct_nan"] = round(df["Nan"] / data.shape[0] * 100, 2)
    df["dtype"] = data.dtypes.values
    df["count"] = data.count().values
    df["pct_reg"] = ((data.notna().sum().values / data.shape[0]) * 100).round(2)
    df["count_unique"] = [
        len(data[elemento].value_counts()) for elemento in data.columns
    ]
    df = df.reset_index(drop=False)
    df = df.sort_values(by=["dtype", "count_unique"])
    df = df.reset_index(drop=True)
    return df


def save_object(objeto, file_name):
    """Guarda el objeto en un archivo pickle"""
    with open(file_name + ".pickle", "wb") as f:
        pickle.dump(objeto, f)


