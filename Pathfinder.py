from Obj_classes import *
from Updating_conditions import *
from Calculate_functions import *
from Type_decide import Type_decide
import math

#------------------------------------------------------------

def Choose_best_node(present_node, second_node, send_value, Nodes_Dict, Used):
    '''Выбор подходящего узла для транзитной передачи'''

    max_choosing_score = -1
    choosing_node = None

    #Выбираем наилучший узел для построения транзита
    for node in present_node.Allowed_connections:  #Идём по всем разрешённым узлам для связи у рассматриаемого узла
        if (Used[present_node][node] == 0  and  node not in present_node.Connections_IN): #Если через узел не пытались проложить транзит на этой операции
            choosing_score = 0              #Начинаем сканировать узел


            #Дальше смотрим на связи рассматриваемого узла-отправителя
            for ED in Nodes_Dict[present_node]:
                #Если через данную связь ещё ничего не передавали
                if (ED.source == present_node and ED.destination == node and  len(ED.transport_value) == 0):

                    #Если входные данные указывают, что эту связь нужно использовать
                    if (ED.active == 1 or ED.MIN_transport_value > 0) and fabs(ED.MAX_transport_value-ED.real_sum_value) >= send_value:
                        choosing_score += 50

                    #Если с построением передающей связи ограничение на максимум исходящих связей будет нарушено
                    if (len(list(set(present_node.Connections_OUT))) == present_node.OUT_edges_max):
                        choosing_score += -2000
                        break   #Перестаём рассматривать этот узел

                    #Если максимум входящих связей узла-получателя будет превышен при построении новой связи
                    if (len(list(set(node.Connections_IN))) == node.IN_edges_max):
                        choosing_score += -2000
                        break   #Перестаём рассматривать этот узел

                    #Если точь-в-точь попадаем в максимум входящих связей узла-получателя
                    if (node.IN_edges_real + 1 == node.IN_edges_max):
                        choosing_score += 5


                    #Если минимум входящих связей узла-получателя не будет достигнут с новой связью
                    if (node.IN_edges_real + 1 < node.IN_edges_min):
                        choosing_score += 20


                    # Если минимум исходящих связей узла-получателя не будет достигнут с новой связью
                    if (node.OUT_edges_real + 1 < node.OUT_edges_min):
                        choosing_score += 20

                    #Если минимум исходящих связей узла-отправителя не будет достигнут с новой связью
                    if (present_node.OUT_edges_real + 1 < present_node.OUT_edges_min):
                        choosing_score += 40


                    break


                #Если связь с данным узлом-получателем существует и она не пустая
                if (ED.source == present_node and ED.destination == node and  len(ED.transport_value) != 0):

                    if (ED.MAX_transport_value <= ED.real_sum_value):
                        choosing_score += -2000
                        break

                    choosing_score += 50   #По дефолту накидываем приоритетные очки

                    if (ED.active == 1 or ED.MIN_transport_value > 0) and fabs(ED.MAX_transport_value-ED.real_sum_value) >= send_value:
                        choosing_score += 50

                    if (node.OUT_edges_real + 1 < node.OUT_edges_min):
                        choosing_score += 20


                    break


            if (node == second_node and choosing_score >= 0):       #Если мы нашли конечный узел
                choosing_score += 50        #То накинем ему 50 очков приоритета

            #print(node.name, '----', choosing_score)

            #Отбираем узел с максимальными очками приоритета
            if (choosing_score > max_choosing_score and choosing_score > 0):
                max_choosing_score = choosing_score
                choosing_node = node


    return choosing_node


#------------------------------------------------------------


def Path_to_node(Nodes_Dict, first_node, second_node):
    '''Поиск пути от одного узла к другому'''

    #-------------------------------------------------------
    #Если только начали поиск пути
    Path = []
    Used = {}

    for node in Nodes_Dict.keys(): #Составляем список использованных/неиспользованных узлов
        Used.update({node: {}})
        for node_2 in Nodes_Dict.keys():
            if(node != node_2):
                Used[node].update({node_2: 0})
            else:
                Used[node].update({node_2: 1})

    #Находим узлы, принадлежащие именно этой копии словаря
    for node in Nodes_Dict.keys():
        if (first_node == node.name):
            first_node = node
        elif (second_node == node.name):
            second_node = node

    #Считаем, сколько нужно передавать ресурсов
    send_value = min(first_node.real_value - first_node.end_value, second_node.end_value - second_node.real_value)
    #---------------------------------------------------------

    #-----------------------------------------------------------
    #Проверим, можно ли начальному узлу-отправителю осуществлять пересылки
    present_node = first_node   #Берём узел-источник за проверяемый

    for node in Nodes_Dict.keys(): #Составляем список использованных/неиспользованных узлов
        if(node != present_node):
            Used[node][present_node] = 1      #Отмечаем его как использованный

    Path.append([present_node, send_value])   #Начинаем с него поиск пути

    if (len(present_node.Allowed_connections) == 0):  #Если узел не может ни с кем связаться
        return Nodes_Dict, Path, "Nope A_C"                                  #Выкидываем ошибку
    if (present_node.IN_edges_real > present_node.IN_edges_max): #Если кол-во входящих связей больше максимума
        return Nodes_Dict, Path, "Nope IN real>max"+' '+present_node.name                                   #Выкидываем ошибку
    if (present_node.OUT_edges_real > present_node.OUT_edges_max): #Если кол-во исходящих связей больше максимума
        return Nodes_Dict, Path, "Nope OUT real>max"+' '+present_node.name                                   #Выкидываем ошибку

    #-----------------------------------------------------------

    n = 1
    #Начинаем поиск пути
    flag = False
    while (flag != True):   #Повторяем, пока не найдём путь до конечного узла
            n = 1
            choosing_node = Choose_best_node(present_node, second_node, send_value, Nodes_Dict, Used)   #Ищем наиболее подходящий транзитный узел


            if(choosing_node == None):        #Если такой узел не был найден
                if (len(Path) > 1):           #И у нас уже был построен хоть какой-то промежуточный путь
                    Path.pop()                #Убираем этот тупиковый узел из пути
                    Used[Path[-1][0]][present_node] = 1  # Отмечаем узел как использованный (на самом деле он оказался тупиковым)
                    Used[present_node][Path[-1][0]] = 1


                    present_node.Connections_IN.remove(Path[-1][0])  # отменяем направление передачи
                    Path[-1][0].Connections_OUT.remove(present_node)  # для контактировавших узлов

                    present_node = Path[-1][0]  # И возвращаемся на один узел назад в пути


                    #Продолжаем искать путь
                    continue

                else:  #Если путь найти от начальной точки невозможно
                    error_str = 'Путь не был построен -->' + '  Начальный узел =' + first_node.name + '   Конечный узел =' + second_node.name
                    return Nodes_Dict, Path, error_str        #Если у нас не был построен никакой путь, то выкидываем ошибку


            # Осуществляем пересылки
            for ED in Nodes_Dict[present_node]:
                if (ED.source == present_node and ED.destination == choosing_node):
                    send_value = min(send_value, math.fabs(ED.MAX_transport_value - ED.real_sum_value))


            present_node.Connections_OUT.append(choosing_node)  # Отмечаем направление передачи
            choosing_node.Connections_IN.append(present_node)  # для контактирующих узлов

            Used[Path[-1][0]][choosing_node] = 1     #Отмечаем найденный узел как использованный
            Used[choosing_node][Path[-1][0]] = 1
            Path.append([choosing_node, send_value])  #Добавляем его в путь
            present_node = Path[-1][0]     #Начинаем строить путь от этого узла на следующей итерации


            if (choosing_node == second_node):
                flag = True

    print('Поиск путей завершён удачно!', '  Начальный узел =', first_node.name, '   Конечный узел =', second_node.name)
    return Nodes_Dict, Path, True