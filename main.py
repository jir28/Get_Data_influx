import random
import influxdb_client
import numpy as np


def sumValues(array_Lits):
    return round((np.sum(array_Lits)), 2)

def promT(arrTem):
    return np.mean(arrTem)


def get_data_querys(query_info):
    org = "jirs28"
    token = "CogeqAhxfHt5o-0rkeCtKiMxyhXMjJaqugbHUN_LisF7cvH9LaIyDvFAZfU5CEDVrFkiYeh_69_TQ-NKUsKCeg=="
    url = "https://us-east-1-1.aws.cloud2.influxdata.com"

    client = influxdb_client.InfluxDBClient(
        url=url,
        token=token,
        org=org
    )
    query_api = client.query_api()
    query_T = query_info
    aux = 0
    aux1 = 0
    aux2 = 0
    result1 = query_api.query(org=org, query=query_T)
    arr_tiempo = []
    for table in result1:
        for record in table.records:
            arr_tiempo.append((record.get_value()))
            if record.get_field() == 'Segundos' and aux == 0:
                aux = 1
            elif record.get_field() == 'Litros' and aux1 == 0:
                aux1 = 1
            elif record.get_field() == 'Celsius' and aux2 == 0:
                aux2 = 1
    ar_li = np.asarray(arr_tiempo).reshape(1, -1)
    if aux == 1:  # para  Tiempo
        valor = (sumValues(ar_li))/60
    elif aux1 == 1:  # para Litros
        valor = sumValues(ar_li)
    elif aux2 == 1:  # para Temperatura
        valor = promT(ar_li)

    return valor


# Tiempos para 30 dias
queryTemp = ' from(bucket:"ShowerS")\
       |> range(start: -30d)\
       |> filter(fn:(r) => r._measurement == "TemperaturaProm")\
       |> filter(fn:(r) => r._field == "Celsius" ) '
queryLiters = ' from(bucket:"ShowerS")\
            |> range(start: -30d)\
            |> filter(fn:(r) => r._measurement == "Litros")\
            |> filter(fn:(r) => r._field == "Litros" ) '

queryTime = ' from(bucket:"ShowerS")\
        |> range(start: -30d)\
        |> filter(fn:(r) => r._measurement == "Tiempo")\
        |> filter(fn:(r) => r._field == "Segundos" ) '

#####################
# Tiempos para una semana
queryTemp7 = ' from(bucket:"ShowerS")\
       |> range(start: -7d, stop: now)\
       |> filter(fn:(r) => r._measurement == "TemperaturaProm")\
       |> filter(fn:(r) => r._field == "Celsius" ) '

queryLiters7 = ' from(bucket:"ShowerS")\
            |> range(start: -7d, stop: now)\
            |> filter(fn:(r) => r._measurement == "Litros")\
            |> filter(fn:(r) => r._field == "Litros" ) '

queryTime7 = ' from(bucket:"ShowerS")\
        |> range(start: -7d, stop: now)\
        |> filter(fn:(r) => r._measurement == "Tiempo")\
        |> filter(fn:(r) => r._field == "Segundos" ) '

Lits = get_data_querys(queryLiters)
tiempos = get_data_querys(queryTime)
tempes = get_data_querys(queryTemp)
# promTim = round((np.sum(Tim))/60, 2)
print("Litros de baño : ", Lits)
print("Minutos de baño : ", tiempos)
print("TempProm de baño : ", tempes)
