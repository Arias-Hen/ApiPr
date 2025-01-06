from django.db import models
import pandas as pd
import joblib
import numpy as np

# Rutas de los directorios
CSV_DIR = "MyApi/csv/"
MODELS_DIR = "MyApi/models/"

def load_csv(file_name):
    """
    Carga un archivo CSV y devuelve su contenido como un DataFrame.
    """
    file_path = f"{CSV_DIR}{file_name}"
    return pd.read_csv(file_path, encoding="ISO-8859-1")

class PredictionModel:
    @staticmethod
    def predict(data):
        ciudad = data.get("ciudad")
        distrito = data.get("distrito")
        barrio = data.get("barrio")
        tipo_vivienda = int(data.get("tipo_vivienda"))
        m2 = float(data.get("m2"))
        num_habitaciones = int(data.get("num_habitaciones"))
        num_banos = int(data.get("num_banos"))
        planta = data.get("planta")
        terraza = int(data.get("terraza"))
        balcon = int(data.get("balcon"))
        ascensor = int(data.get("ascensor"))
        estado = data.get("estado")

        # Cargar datos desde los CSV
        df_ciudad = load_csv("distritos.csv")
        df_disbar = load_csv("distrito_barrio.csv")

        # Obtener valores de distrito y barrio
        distrito_val = df_ciudad[df_ciudad["distrito"] == distrito]["precio_m2_distrito"].values[0]
        barrio_val = df_disbar[df_disbar["barrio"] == barrio]["precio_m2_barrio"].values[0]

        # Preparar las entradas del modelo
        if tipo_vivienda not in [2, 5, 6]:
            X_list = [
                m2,
                float(distrito_val),
                float(barrio_val),
                tipo_vivienda,
                num_habitaciones,
                num_banos,
                planta,
                terraza,
                balcon,
                ascensor,
                estado,
            ]
            model_path = f"{MODELS_DIR}modelo_rf_pisos_joblib.pkl"
        else:
            X_list = [
                m2,
                float(distrito_val),
                float(barrio_val),
                tipo_vivienda,
                num_habitaciones,
                num_banos,
            ]
            model_path = f"{MODELS_DIR}modelo_rf_casas_joblib.pkl"

        X = np.array(X_list, dtype=np.float64).reshape(1, -1)

        # Cargar modelo y realizar predicción
        model = joblib.load(model_path)
        predicciones = model.predict(X)

        # Calcular valores corregidos
        corrector = 0.10
        predicciones_bottom = predicciones * (1 - 2 * corrector)
        precio_medio = predicciones * (1 - corrector)
        predicciones_top = predicciones

        return {
            "precio_minimo": np.round(predicciones_bottom[0], 2),
            "precio_esperado": np.round(precio_medio[0], 2),
            "precio_maximo": np.round(predicciones_top[0], 2),
        }
