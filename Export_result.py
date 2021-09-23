from Obj_classes import *
from Calculate_functions import *
import pandas as pd
import math
from xlwt import *
from xlrd import *

#------------------------------------------------------------------------

def Write_to_Excel(Result_Dict, Nodes_count, file_input, file_output):
    """Запись результата в Excel"""

    Res_file = open_workbook(file_input) # Открываем файл эксель с входными данными
    sheet = Res_file.sheet_by_index(0)

    # получаем список значений из всех записей
    vals = [sheet.row_values(rownum) for rownum in range(sheet.nrows)]


    for i, item in enumerate(Result_Dict):  #Записываем расчитанные значения
        vals[i + 3][1] = item.name
        vals[i + 3][2] = item.date
        vals[i + 3][3] = item.code
        vals[i + 3][4] = item.active
        vals[i + 3][5] = item.start_value
        vals[i + 3][6] = item.IN_turnover_value
        vals[i + 3][7] = item.OUT_turnover_value
        vals[i + 3][8] = item.real_value
        vals[i + 3][9] = item.IN_edges_min
        vals[i + 3][10] = item.IN_edges_max
        vals[i + 3][11] = item.IN_edges_real
        vals[i + 3][12] = item.OUT_edges_min
        vals[i + 3][13] = item.OUT_edges_max
        vals[i + 3][14] = item.OUT_edges_real

        for j in range(len(item.class_numbers)):
            item.class_numbers[0] = str(item.class_numbers[0]) + ' ,' + str(item.class_numbers[j])

        vals[i + 3][15] = item.class_numbers[0]
        vals[i + 3][16] = item.Exit_out_edges_max_beg
        vals[i + 3][17] = item.Exit_out_edges_real
        vals[i + 3][18] = item.Exit_out_edges_allowed_difference


    #Считаем суммарные обороты и суммы входящих\исходящих связей
    sum_in = 0
    sum_out = 0
    edges_in = 0
    edges_out = 0
    for i in Result_Dict.keys():
        sum_in += i.IN_turnover_value
        sum_out += i.OUT_turnover_value
        edges_in += i.IN_edges_real
        edges_out += i.OUT_edges_real

    vals[2][6] = sum_in
    vals[2][7] = sum_out
    vals[2][11] = edges_in
    vals[2][14] = edges_out

    for i in range(len(vals)):
        print(vals[i])


#------------------------------------------------------
    #Вывод данных для проверки
    for i in Result_Dict.keys():
        print(i.name, '----', i.real_value)

#------------------------------------------------------

    #Запись в файл
    wb = Workbook()
    ws = wb.add_sheet('Узлы')

    for i in range(len(vals)):
        for j in range(len(vals[i])):
            ws.write(i, j, vals[i][j])



    #Создаём форматный массив пересылок
    vals = [  ['Узел', '', 'Актив', 'Значение', '', ''] , ['Начальный', 'Конечный', '', 'Минимум', 'Максимум', 'Расчёт']  ]
    for node in Result_Dict.keys():
        for ED in Result_Dict[node]:
            Sum = 0
            for send in ED.transport_value:
                    if send[0] < 0:
                        Sum += math.fabs(send[0])
            if Sum !=0:
                vals.append([ED.source.name, ED.destination.name, ED.active, ED.MIN_transport_value, ED.MAX_transport_value, Sum])


    #Записываем массив пересылок
    ws = wb.add_sheet('Связи')

    for i in range(len(vals)):
        for j in range(len(vals[i])):
            ws.write(i, j, vals[i][j])

    #Сохраняем файл
    wb.save(file_output)
# -------------------------------------------------------------------------