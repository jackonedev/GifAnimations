# print ('Libreria SmartSeries:\n\tClases:\n\t\t- VectorBuilder() \n\tFunciones:\n\t\t- load_dataset')
import numpy as np
import pandas as pd



def check_type_dt(dataset):  # for VectorBuilding.__init__
    if isinstance(dataset.index, pd.core.indexes.datetimes.DatetimeIndex):
        print(f"\nSerie de tiempo: {dataset.index.name}\n")
        return dataset
    else:
        cols_dt = (dataset.dtypes == "<M8[ns]").values
        if cols_dt.sum() == 0:
            indice = check_type_str(dataset)
            print(f"\nSerie de tiempo: {indice}\n")
            dataset[indice] = pd.to_datetime(
                dataset[indice], infer_datetime_format=True
            )
            return dataset.set_index(indice)
        elif cols_dt.sum() == 1:
            indice = list(dataset.loc[:, cols_dt].columns)[0]
            print(f"\nSerie de tiempo: {indice}\n")
            return dataset.set_index(indice)
        else:
            indice = select_type_dt(dataset, cols_dt)
            print(f"\nSerie de tiempo: {indice}\n")
            return dataset.set_index(indice)


def check_type_str(dataset):  # for load_dataset
    cols_mask = (dataset.dtypes == "object").values
    cols_obj = dataset.loc[:, cols_mask].columns.values
    posibles_dt = []
    if len(cols_obj) == 0:
        return print('No hay columnas tipo "object"')
    for i, elemento in enumerate(cols_obj):
        try:
            pd.to_datetime(dataset[elemento], infer_datetime_format=True)
            posibles_dt.append(elemento)
        except:
            pass
    return select_type_dt(dataset, posibles_dt)


def select_type_dt(dataset, cols_dt):  # used above in check_type_str and check_type_dt
    indice = list(dataset.loc[:, cols_dt].columns)
    if len(indice) == 1:
        return indice[0]
    for i in range(len(indice)):
        indice[i] = str(i + 1) + ") {}".format(indice[i])
    print(">> SELECCION DE SERIE DE TIEMPO:")
    for i in range(len(indice)):
        print(indice[i])
    op = input(">> ")
    try:
        op = int(op) - 1  # para empezar a contar desde cero
        indice = list(dataset.loc[:, cols_dt].columns)[op]
        return indice
    except:
        print("\nERROR: La opcion ingresada no corresponde\n")
        return







class VectorBuilder:
    """data_class para almacenamiento y tratamiento del dataset, objetivo: obtener matriz features y vector target for spliting"""

    def __init__(self, dataset):
        self.dataset = check_type_dt(dataset)
        self.vector = None
        self.target = None
        self.downsampling = None
        self.targets = []
        self.features = []

    @staticmethod
    def change_target(self, umbral):
        self.target = umbral

    def create(self, target=None, func="sum"):
        if isinstance(target, type(None)):
            self.target = list(self.dataset.columns)[0]
        else:
            self.target = target
        if self.target not in self.targets:
            self.targets.append(self.target)
        if func == "sum":  # actualizar esto con pd.agreggate
            self.vector = pd.DataFrame(
                self.dataset.groupby(self.dataset.index)[self.target].sum()
            )
            return self.vector

    def treatment(self, downsampling=False, how="MS"):
        if downsampling:
            self.downsampling = (
                self.create(self.target)[self.target].resample(how).mean().to_frame()
            )

        label = "log_" + self.target
        self.vector.loc[:, label] = pd.Series(
            np.log(self.vector[self.target]), index=self.vector.index
        )
        # if label not in self.targets: self.targets.append(label)
        if not isinstance(self.downsampling, type(None)):
            self.downsampling.loc[:, label] = pd.Series(
                np.log(self.downsampling[self.target]), index=self.downsampling.index
            )

        label = "timeIndex"
        self.vector.loc[:, label] = pd.Series(
            np.arange(self.vector.shape[0]), index=self.vector.index
        )
        if not isinstance(self.downsampling, type(None)):
            self.downsampling.loc[:, label] = pd.Series(
                np.arange(self.downsampling.shape[0]), index=self.downsampling.index
            )

        label = "timeIndex_sq"
        self.vector.loc[:, label] = pd.Series(
            np.arange(self.vector.shape[0]) ** 2, index=self.vector.index
        )
        if not isinstance(self.downsampling, type(None)):
            self.downsampling.loc[:, label] = pd.Series(
                np.arange(self.downsampling.shape[0]) ** 2,
                index=self.downsampling.index,
            )

        if downsampling and how == "MS":  # actualizar
            # crear columna con meses
            self.vector = pd.concat(
                [
                    self.vector,
                    sort_cols_by_month(
                        pd.get_dummies(
                            pd.Series(
                                [i.strftime("%b") for i in self.vector.index],
                                index=self.vector.index,
                            )
                        )
                    ),
                ],
                axis=1,
            )
            self.downsampling = pd.concat(
                [
                    self.downsampling,
                    sort_cols_by_month(
                        pd.get_dummies(
                            pd.Series(
                                [i.strftime("%b") for i in self.downsampling.index],
                                index=self.downsampling.index,
                            )
                        )
                    ),
                ],
                axis=1,
            )

        return "Vector actualizado"

    def dummy(self, how="W"):
        # change from freq to strftime
        if how == "W":
            self.vector = pd.concat(
                [
                    self.vector,
                    pd.get_dummies(
                        pd.Series(
                            [i.strftime("%U") for i in self.vector.index],
                            index=self.vector.index,
                        ),
                        prefix="sem",
                    ),
                ],
                axis=1,
            )
        if how == "M":
            self.vector = pd.concat(
                [
                    self.vector,
                    sort_cols_by_month(
                        pd.get_dummies(
                            pd.Series(
                                [i.strftime("%b") for i in self.vector.index],
                                index=self.vector.index,
                            )
                        )
                    ),
                ],
                axis=1,
            )


class Results:

    dataset = pd.DataFrame(columns=["Model"])

    def __init__(self, dataset=dataset):
        self.dataset = dataset

    def RMSE(self, prediccion, actual):
        mse = (prediccion - actual) ** 2
        rmse = np.sqrt(mse.sum() / mse.count())
        return rmse

    def add_rmse(self, label, prediccion, actual):
        self.dataset.loc[self.dataset.shape[0], "Model"] = label
        self.dataset.loc[self.dataset.Model == label, "RMSE"] = self.RMSE(
            prediccion, actual
        )
        return self.dataset

    def read_data(self, data):
        self.dataset = data.copy()
        return self.dataset
