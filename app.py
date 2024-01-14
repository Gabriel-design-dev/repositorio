from flask import Flask, render_template, request, send_file, redirect, flash
import pandas as pd
from openpyxl import Workbook
from io import BytesIO
from datetime import datetime
import pandas as pd
from openpyxl import Workbook
from openpyxl.styles import Border, Side, PatternFill, Alignment, Font
from datetime import datetime

app = Flask(__name__, template_folder='template')

def procesar_archivo(archivo,titulo):
    datos = pd.read_excel(archivo)

    # ... (Resto de tu código de procesamiento)
    # Almacenar los últimos valores de las columnas 'TOTAL' y 'Unnamed: 27'
    ultimo_valor_total = datos['TOTAL'].iloc[-1]
    ultimo_valor_unnamed = datos['Unnamed: 27'].iloc[-1]

    # Seleccionar solo la columna "Descripción"
    columnas_seleccionadas = datos[['Descripción', 'TOTAL', 'Unnamed: 27']]
    columnas_seleccionadas = columnas_seleccionadas.reset_index(drop=True)

    # Convertir la columna 'Unnamed: 27' a tipo numérico solo en las filas numéricas
    columnas_seleccionadas.iloc[1:, 2] = pd.to_numeric(columnas_seleccionadas.iloc[1:, 2], errors='coerce')

    # Filtrar filas que contienen 'total' en la columna 'Descripción', excluyendo la fila 0
    columnas_filtradas = columnas_seleccionadas.copy()
    columnas_filtradas.iloc[1:, 2] = pd.to_numeric(columnas_filtradas.iloc[1:, 2], errors='coerce')
    columnas_filtradas = columnas_filtradas[~columnas_filtradas['Descripción'].fillna('').str.lower().str.contains('total')]
    
    # Ordenar solo las filas que contienen datos numéricos por la columna 'Unnamed: 27' de mayor a menor
    columnas_ordenadas = columnas_filtradas.iloc[1:].sort_values(by='Unnamed: 27', ascending=False)

    # Seleccionar los primeros 10 datos después de ordenar
    primeros_10_datos = columnas_ordenadas.head(10)

    
    # Concatenar la fila 0 y los primeros 10 datos ordenados
    resultado_final = pd.concat([columnas_filtradas.iloc[:1], primeros_10_datos])

    # Calcular la suma total de 'TOTAL' y 'Unnamed: 27' excluyendo la fila 0
    suma_total_TOTAL = resultado_final.iloc[1:]['TOTAL'].sum()
    suma_total_Unnamed = resultado_final.iloc[1:]['Unnamed: 27'].sum()

    # Crear una nueva fila con el valor "Otros" y las sumas calculadas
    fila_otros = pd.DataFrame({"Descripción": ["Otros"], "TOTAL": [suma_total_TOTAL], "Unnamed: 27": [suma_total_Unnamed]})

    # Concatenar la fila "Otros" al final del DataFrame
    resultado_final = pd.concat([resultado_final, fila_otros], ignore_index=True)
    
    fila_total = pd.DataFrame({
    "Descripción": ["Total"],
    "TOTAL": [ultimo_valor_total],
    "Unnamed: 27": [ultimo_valor_unnamed]
    })

    # Concatenar la fila "Total" al final del DataFrame
    resultado_final = pd.concat([resultado_final, fila_total], ignore_index=True)

# Calcular las diferencias entre las filas 'Total' y 'Otros'
    diferencia_total_otros_total = resultado_final.loc[resultado_final['Descripción'] == 'Total', 'TOTAL'].values[0] - resultado_final.loc[resultado_final['Descripción'] == 'Otros', 'TOTAL'].values[0]
    diferencia_total_otros_unnamed = resultado_final.loc[resultado_final['Descripción'] == 'Total', 'Unnamed: 27'].values[0] - resultado_final.loc[resultado_final['Descripción'] == 'Otros', 'Unnamed: 27'].values[0]
    
    # Actualizar los valores en la fila 'Otros'
    resultado_final.loc[resultado_final['Descripción'] == 'Otros', 'TOTAL'] = diferencia_total_otros_total
    resultado_final.loc[resultado_final['Descripción'] == 'Otros', 'Unnamed: 27'] = diferencia_total_otros_unnamed
    # ... (Código para generar el resultado_final)

   

    
# Cambiar el nombre de la columna "Unnamed: 27" a "TOTAL"
    resultado_final = resultado_final.rename(columns={'Unnamed: 27': 'TOTAL'})

    # Crear un nuevo libro de trabajo de Excel
    workbook = Workbook()
    sheet = workbook.active

    # Agregar un título encima de la tabla con la fecha actual
    fecha_actual = datetime.now().strftime("%d-%m-%Y, Horas: %H:%M:%S")
    titulo_completo = f"TOP 10 DE LOS TRAMITES MAS SOLICITADOS EN EL {titulo}\n(FECHA: {fecha_actual})"
    sheet.merge_cells(start_row=1, start_column=1, end_row=1, end_column=len(resultado_final.columns))
    sheet['A1'] = titulo_completo
    sheet['A1'].font = Font(size=13, bold=True)
    sheet['A1'].alignment = Alignment(wrap_text=True, horizontal='center', vertical='center')

    # Ajustar el alto de la fila para adaptarse al texto del título
    sheet.row_dimensions[1].height = 57  # Ajusta el valor según tus necesidades

    # Obtener el número de filas ocupadas por los encabezados y datos
    num_filas_datos = len(resultado_final) + 2  # Se suma 2 para incluir la fila de encabezados y la fila del título

    # Copiar los encabezados del DataFrame al libro de trabajo
    headers = [col for col in resultado_final.columns]
    sheet.append(headers)

    # Copiar los datos del DataFrame al libro de trabajo
    for row in resultado_final.itertuples(index=False):
        sheet.append(list(row))

    # Aplicar bordes a todas las celdas
    for row in sheet.iter_rows(min_row=2, max_row=num_filas_datos, min_col=1, max_col=sheet.max_column):
        for cell in row:
            cell.border = Border(left=Side(border_style='thin', color='000000'),
                                right=Side(border_style='thin', color='000000'),
                                top=Side(border_style='thin', color='000000'),
                                bottom=Side(border_style='thin', color='000000'))

    # Aplicar color a la fila de encabezados (columnas)
    for cell in sheet[2]:
        cell.fill = PatternFill(start_color="D3D3D3", end_color="D3D3D3", fill_type="solid")

    # Aplicar color a la fila de encabezados (columnas)    
    for cell in sheet[3]:
        cell.fill = PatternFill(start_color="D3D3D3", end_color="D3D3D3", fill_type="solid")

    # Aplicar color a la penúltima fila de la tabla (restamos 1 al índice máximo de filas)
    for cell in sheet[num_filas_datos - 1]:
        cell.fill = PatternFill(start_color="FFFF00", end_color="FFFF00", fill_type="solid")  # Amarillo

    # Aplicar color a la última fila de la tabla
    for cell in sheet[num_filas_datos]:
        cell.fill = PatternFill(start_color="D3D3D3", end_color="D3D3D3", fill_type="solid")

    # Ajustar el formato del texto para mostrar múltiples líneas
    for row in sheet.iter_rows(min_row=2, max_row=num_filas_datos, min_col=1, max_col=sheet.max_column):
        for cell in row:
            cell.alignment = Alignment(wrap_text=True, horizontal='center', vertical='center')

    # Establecer el ancho de la columna "Descripcion"
    sheet.column_dimensions['A'].width = 40  # Ajusta el valor según tus necesidades
    sheet.column_dimensions['B'].width = 13
    sheet.column_dimensions['C'].width = 13

    # Guardar el archivo Excel
    workbook.save('reporte_top_10_go.xlsx')


    # ... (Código para dar formato y guardar el archivo)

    # Convertir el libro de trabajo en un objeto BytesIO para descargar
    output = BytesIO()
    workbook.save(output)
    output.seek(0)

    return output

@app.route('/')
def home():
    return render_template('index.html')


@app.route('/subir')
def subir():
    return render_template('subir.html')

@app.route('/procesar', methods=['POST'])
def procesar():
    if 'archivo' not in request.files:
        flash('No se proporcionó ningún archivo')
        return redirect(request.url)

    archivo = request.files['archivo']
    titulo = request.form.get('titulo')
    
    if archivo.filename == '':
        flash('Ningún archivo seleccionado')
        return redirect(request.url)

    if archivo:
        output = procesar_archivo(archivo,titulo)
        return send_file(output, as_attachment=True, download_name=f'TOP_10_{titulo}.xlsx')

    return render_template('index.html')

@app.route('/top_10')
def top_10():
    return render_template('top_10.html')

if __name__ == '__main__':
    app.secret_key = "pinchellave"
    app.run(debug=True, host='0.0.0.0', port=5000, threaded=True)