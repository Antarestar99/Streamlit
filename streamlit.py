import streamlit as st
import pandas as pd
from datetime import date
from sqlalchemy import create_engine

def main():
    st.title("Cargar Formato Ventas + Clientes")

    # ==== Sección de parámetros ====
    st.subheader("Parámetros de carga")
    separador = st.text_input("Separador", value=",")
    lineas_encabezado = st.number_input("Líneas de encabezado (header)", min_value=0, value=1)
    fecha_seleccionada = st.date_input("Fecha", value=date.today())

    st.write("---")

    # ==== Subida de archivo ====
    st.subheader("Carga de Archivo")
    archivo = st.file_uploader(
        "Arrastra y suelta tu archivo (CSV o TXT)",
        type=["csv", "txt"]
    )

    # Si se ha subido un archivo, lo procesamos
    if archivo is not None:
        # Leemos el CSV/TXT con pandas
        # Si lineas_encabezado es 1 significa header en la primera línea (por ejemplo).
        # Si lineas_encabezado es 0, significa que no tiene encabezados (None).
        header_val = 0 if lineas_encabezado == 0 else 'infer'
        
        df = pd.read_csv(
            archivo,
            sep=separador,
            header=header_val
        )

        st.write("Vista previa de los datos:")
        st.dataframe(df.head(10))  # muestra las primeras 10 filas

        # Opcional: Muestra info de filas y columnas
        st.write(f"Filas: {df.shape[0]} | Columnas: {df.shape[1]}")

        # ==== Botón para subir a la base de datos ====
        if st.button("Cargar datos en PostgreSQL"):
            try:
                # Ajusta la cadena de conexión a tu entorno:
                #   usuario: contraseña@host:puerto/nombre_base
                engine = create_engine("postgresql://postgres:tu_contraseña@localhost:5432/tu_base")

                # Ojo con el nombre de la tabla. 
                # 'if_exists="append"' para añadir registros,
                # 'if_exists="replace"' para borrar la tabla y crearla de nuevo.
                df.to_sql("ventas_clientes", engine, if_exists="append", index=False)

                st.success("¡Datos cargados exitosamente en PostgreSQL!")
            except Exception as e:
                st.error(f"Ocurrió un error al cargar los datos: {e}")

if __name__ == "__main__":
    main()
