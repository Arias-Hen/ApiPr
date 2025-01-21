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
        calle = data.get("calle")
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
        df_ciudad = load_csv("tb_todo_precio_m2.csv")
        df_disbar = load_csv("tb_todo_precio_m2.csv")
        df_calles = load_csv("tb_todo_precio_m2.csv")
        df_modelos = load_csv("tb_grupo_modelo.csv") 
        
        
        # Obtener valores de distrito, barrio y calle
        distrito_val = df_ciudad[df_ciudad["distrito"] == distrito]["precio_m2_distrito"].values[0]
        barrio_val = df_disbar[df_disbar["barrio"] == barrio]["precio_m2_barrio"].values[0]
        calle_val = df_calles[df_calles["calle"] == calle]["precio_m2_calle"].values[0]
        # Determinar el modelo a usar basado en la ciudad y el distrito
        modelo_fila = df_modelos[(df_modelos["ciudad"] == ciudad) & (df_modelos["distrito"] == distrito)]
        if not modelo_fila.empty:
            modelo_archivo = modelo_fila["modelo"].iloc[0]
            model_path = f"{MODELS_DIR}{modelo_archivo}"
        else:
            raise ValueError("No se encontró un modelo para esta combinación de ciudad y distrito.")

        # Preparar las entradas del modelo
        if tipo_vivienda not in [2, 5, 6]:
            X_list = [
                m2,
                float(distrito_val),
                float(barrio_val),
                float(calle_val),
                tipo_vivienda,
                num_habitaciones,
                num_banos,
                planta,
                terraza,
                balcon,
                ascensor,
                estado,
            ]
        else:
            X_list = [
                m2,
                float(distrito_val),
                float(barrio_val),
                float(calle_val),
                tipo_vivienda,
                num_habitaciones,
                num_banos,
            ]
        print("LISTA DE SELECCION (Réplica):", X_list)
        X = np.array(X_list, dtype=np.float64).reshape(1, -1)

        if ciudad != "Madrid":
            print("EME 2", m2)
            print("LACALLE", calle_val)
            predicciones = m2 * calle_val * 1000
            corrector = 0.10
            predicciones_bottom = predicciones * (1 - corrector)
            precio_medio = predicciones
            predicciones_top = predicciones * (1 + corrector)
            return {
                "precio_minimo": np.round(predicciones_bottom, 2),
                "precio_esperado": np.round(precio_medio, 2),
                "precio_maximo": np.round(predicciones_top, 2),
            }
        else:
            model = joblib.load(model_path)
            predicciones = model.predict(X)
            corrector = 0.10
            predicciones_bottom = predicciones * (1 - corrector)
            precio_medio = predicciones
            predicciones_top = predicciones * (1 + corrector)
    
            return {
                "precio_minimo": np.round(predicciones_bottom[0], 2),
                "precio_esperado": np.round(precio_medio[0], 2),
                "precio_maximo": np.round(predicciones_top[0], 2),
            }
