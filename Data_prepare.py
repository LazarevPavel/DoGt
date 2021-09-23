from Obj_classes import *
import pandas as pd
import numpy as np
from datetime import datetime

#---------------------------------------------------------------------------------------
def Data_Prepare(File_input):
    '''Подготовка данных к расчёту'''

    data = pd.read_excel(File_input)  # парсинг excel файла с данными
    data = data.values

    Nodes_list = []  # Список узлов

    #Проверяем данные на наличие пустых ячеек.
    for i in range(2, len(data)):
        if pd.isnull(data[i][2]):
            data[i][2] = None
        else:
            data[i][2] = data[i][2].strftime('%d-%m-%Y')

        if pd.isnull(data[i][15]):
            data[i][15] = 0

        if pd.isnull(data[i][18]):
            data[i][15] = 0

        if pd.isnull(data[i][3]) or pd.isnull(data[i][4]) or pd.isnull(data[i][5]) or pd.isnull(data[i][8]) or pd.isnull(data[i][9]) or pd.isnull(data[i][10]) or pd.isnull(data[i][12]) or pd.isnull(data[i][13]) or pd.isnull(data[i][16]):
            error_str = 'Проблема:\nВходные данные имеют пустые ячейки, которые не могут быть пропущены.\nПожалуйста, проверьте входные данные и дополните их необходимой информацией.'
            return None, None, error_str

    #Заполняем список узлов значениями из файла (элемент списка = объект класса Node)
    for i in range(2, len(data)):
        if (data[i][4] == 1):
            New_node = Node(data[i][1], data[i][2], data[i][3], data[i][4], data[i][5], data[i][8], data[i][9], data[i][10],
                            data[i][12], data[i][13], data[i][15], data[i][16], data[i][18])  # Создаём новый узел
            Nodes_list.append(New_node)  # Запихиваем этот узел в список


    #Переводим классы узлов из строкового формата в числовой формат и сохраняем классы в виде списка
    for i in Nodes_list:    #Идём по каждому узлу
        if ( type(i.class_numbers) == type(1)  or  type(i.class_numbers) == type(1.5) ):    #Если в классе единственное число (оно будет целым или дробным)
            temp = int(i.class_numbers)                                                     #то делаем список, в котором это число - единственный элемент
            i.class_numbers = []
            i.class_numbers.append(temp)
        elif ( type(i.class_numbers) == type('str') ):          #А если в классе несколько чисел (перечисленные через запятую - это стороковый тип)
            i.class_numbers = i.class_numbers.split()           #то разделяем строку по числам и заносим эти числа в список (каждое число имеет строковый тип)

            if len(i.class_numbers) != 1:                       #Если длина списка не равна единице (это будут элементы строкового типа)
                for j in range(0, len(i.class_numbers)):        #то переводим каждое число в списке в целочисленный формат
                    i.class_numbers[j] = i.class_numbers[j].replace(',', '.0')
                    i.class_numbers[j] = int(float(i.class_numbers[j]))


    #ТЕПЕРЬ СЧИТАЕМ ДАННЫЕ О СВЯЗЯХ
    data_edges = pd.read_excel(File_input, 1)
    data_edges = data_edges.values

    Edges_list = []

    if len(data_edges) > 0:
        for i in range(1, len(data_edges)):
            one_edge = Edge(data_edges[i][0], data_edges[i][1], transport_value=0, active=0, MIN_transport_value=data_edges[i][3], MAX_transport_value=data_edges[i][4])
            Edges_list.append(one_edge)



    return Nodes_list, Edges_list, True
#------------------------------------------------------------------------------------------