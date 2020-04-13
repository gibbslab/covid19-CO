from sklearn.linear_model import LinearRegression
import plotly.express as px
import numpy as np

def RegresionLineal(X, punto_x):
    x_array = np.asarray([X], dtype=np.float32).T
    punto_x_array = np.asarray(punto_x, dtype=np.float32)
    reg = LinearRegression().fit(x_array, punto_x_array)

    return reg.coef_, reg.intercept_