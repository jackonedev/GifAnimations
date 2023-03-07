import numpy as np
import pandas as pd
from joblib import Parallel, delayed
from sklearn.pipeline import FeatureUnion, _fit_transform_one, _transform_one
from scipy import sparse
from sklearn.base import BaseEstimator, TransformerMixin

#################################
"""Lista de objetos:
	- PandasTransform
	- PandasFeatureUnion
	- CorrSpearman
	- FeatureDiscretize
    """
#################################


class PandasTransform(TransformerMixin, BaseEstimator):
    """Un DataFrame con herencia de Scikit-Learn"""
    def __init__(self, fn):
        self.fn = fn

    def fit(self, X, y=None):
        return self

    def transform(self, X, y=None, copy=None):
        return self.fn(X)


class PandasFeatureUnion(FeatureUnion):
    """Representa el objeto DataFrame.FeatureUnion"""

    def fit_transform(self, X, y=None, **fit_params):
        self._validate_transformers()
        result = Parallel(n_jobs=self.n_jobs)(
            delayed(_fit_transform_one)(
                transformer=trans, X=X, y=y, weight=weight, **fit_params
            )
            for name, trans, weight in self._iter()
        )

        if not result:
            # All transformers are None
            return np.zeros((X.shape[0], 0))
        Xs, transformers = zip(*result)
        self._update_transformer_list(transformers)
        if any(sparse.issparse(f) for f in Xs):
            Xs = sparse.hstack(Xs).tocsr()
        else:
            Xs = self.merge_dataframes_by_column(Xs)
        return Xs

    def merge_dataframes_by_column(self, Xs):
        return pd.concat(Xs, axis="columns", copy=False)

    def transform(self, X):
        Xs = Parallel(n_jobs=self.n_jobs)(
            delayed(_transform_one)(transformer=trans, X=X, y=None, weight=weight)
            for name, trans, weight in self._iter()
        )
        if not Xs:
            # All transformers are None
            return np.zeros((X.shape[0], 0))
        if any(sparse.issparse(f) for f in Xs):
            Xs = sparse.hstack(Xs).tocsr()
        else:
            Xs = self.merge_dataframes_by_column(Xs)
        return Xs


class CorrSpearman(BaseEstimator, TransformerMixin):
    """
    Obtener el vector con los valores de correlación entre la variable target, y el resto de las features
    """
    def __init__(self, target):
        self.target = target
        
    def fit(self, X, y=None):
        return self
    
    def transform(self, X, y=None):
        return abs(X.corr(method='spearman')[self.target].drop(index=self.target).sort_values())


class FeatureDiscretize(BaseEstimator, TransformerMixin):
    """
    Discretiza las columnas ingresadas en la cantidade nbins especificados
    """

    def __init__(self, selected_features, nbins):
        self.selected_features = selected_features
        self.nbins = nbins

    def fit(self, X, y=None):
        return self

    def transform(self, X, y=None, nbins=10):
        return pd.DataFrame(
            pd.qcut(X[self.selected_features], self.nbins, labels=False)
        )