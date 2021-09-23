from Obj_classes import *
from Type_decide import Type_decide
from Updating_conditions import Update_conditions_values
import math
#------------------------------------------------------------



def Choose_best_node(present_node, second_node, send_value, Nodes_Dict, Used, Nsends):
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
                    if (ED.active == 1 and ED.real_sum_value < ED.MIN_transport_value) and math.fabs(ED.MAX_transport_value-ED.real_sum_value) >= send_value:
                        choosing_score += 100

                    #Если с построением передающей связи ограничение на максимум исходящих связей будет нарушено
                    if (present_node.OUT_edges_real + 1 > present_node.OUT_edges_max):
                        choosing_score += -2000
                        break   #Перестаём рассматривать этот узел


                    #Если максимум входящих связей узла-получателя будет превышен при построении новой связи
                    if (node.IN_edges_real + 1 > node.IN_edges_max):
                        choosing_score += -2000
                        break   #Перестаём рассматривать этот узел


                    #Если минимум входящих связей узла-получателя не будет достигнут с новой связью
                    if (node.IN_edges_real + 1 <= node.IN_edges_min):
                        choosing_score += 20

                    # Если минимум исходящих связей узла-получателя не будет достигнут с новой связью
                    if (node.OUT_edges_real + 1 <= node.OUT_edges_min):
                        choosing_score += 20

                    #Если минимум исходящих связей узла-отправителя не будет достигнут с новой связью
                    if (present_node.OUT_edges_real + 1 < present_node.OUT_edges_min):
                        choosing_score += 20


                    if ED.MAX_transport_value <= ED.real_sum_value:
                        choosing_score += -2000
                        break


                    break

                #Если связь с данным узлом-получателем существует и она не пустая
                if (ED.source == present_node and ED.destination == node and  len(ED.transport_value) != 0):

                    if(ED.MAX_transport_value <= ED.real_sum_value):
                        choosing_score += -2000
                        break

                    choosing_score += 20   #По дефолту накидываем приоритетные очки

                    if (ED.active == 1 and ED.real_sum_value < ED.MIN_transport_value) and math.fabs(ED.MAX_transport_value-ED.real_sum_value) >= send_value:
                        choosing_score += 100

                    if (node.IN_edges_real + 1 <= node.IN_edges_min):
                        choosing_score += 20

                    if (node.OUT_edges_real + 1 <= node.OUT_edges_min):
                        choosing_score += 20


                    break


            if (node == second_node and Nsends > 1  and  choosing_score >= 0):       #Если мы нашли конечный узел и это не пересылка "туда-обратно"
                choosing_score += 100        #То накинем ему 100 очков приоритета

            #Отбираем узел с максимальными очками приоритета
            if (choosing_score > max_choosing_score and choosing_score >= 0):
                max_choosing_score = choosing_score
                choosing_node = node


    return choosing_node

#------------------------------------------------------------


def Exit_regulate(trouble_node, Nodes_Dict):
    """Построение дополнительных пересылок для удовлетворения ограничения на % выхода"""

    # Если только начали поиск петли
    Path = []
    Used = {}
    Nsends = 0

    for node in Nodes_Dict.keys():  # Составляем список использованных/неиспользованных узлов
        Used.update({node: {}})
        for node_2 in Nodes_Dict.keys():
            if (node != node_2):
                Used[node].update({node_2: 0})
            else:
                Used[node].update({node_2: 1})


    present_node = trouble_node  # Берём наш узел за проверяемый

    #Считаем, какой минимум нам надо отослать, чтобы процент от выхода стал попадать под ограничение
    if (trouble_node.Exit_out_edges_real != None):
        send_value = present_node.end_value / present_node.Exit_out_edges_max
        send_value = math.fabs(send_value - trouble_node.OUT_turnover_value - trouble_node.end_value)
        send_value = min(send_value, trouble_node.real_value)
    else:
        send_value = present_node.end_value / present_node.Exit_out_edges_max
        send_value = math.fabs(send_value - trouble_node.end_value)
        send_value = min(send_value, trouble_node.real_value)

    Path.append([present_node, send_value])  #Начинаем с него поиск пути

    start_send_value = send_value
    #------------------------------------------------------------------


    # Начинаем поиск пути
    flag = False
    while (flag != True):  # Повторяем, пока не найдём путь до конечного узла

        choosing_node = Choose_best_node(present_node, trouble_node, send_value, Nodes_Dict, Used, Nsends)  # Ищем наиболее подходящий транзитный узел

        if (choosing_node is None):  # Если такой узел не был найден
            if (len(Path) > 1):  # И у нас уже был построен хоть какой-то промежуточный путь
                Path.pop()  # Убираем этот тупиковый узел из пути
                Used[Path[-1][0]][present_node] = 1  # Отмечаем узел как использованный (на самом деле он оказался тупиковым)
                #Used[present_node][Path[-1]] = 1


                present_node.Connections_IN.remove(Path[-1][0])  # отменяем направление передачи
                Path[-1][0].Connections_OUT.remove(present_node)  # для контактировавших узлов

                present_node = Path[-1][0]  # И возвращаемся на один узел назад в пути

                Nsends -= 1

                # Продолжаем искать путь
                continue

            else:  # Если путь найти от начальной точки невозможно
                print('Петля для узла', trouble_node.name, ' не была построена!', ' Израсходованы варианты пересылок.')
                error_str = "Невозможно урегулировать выходы!"
                return Nodes_Dict, Path, error_str  #Если у нас не был построен никакой путь, то выкидываем ошибку


        # Осуществляем пересылки
        for ED in Nodes_Dict[present_node]:
            if (ED.source == present_node and ED.destination == choosing_node):
                send_value = min(send_value, math.fabs(ED.MAX_transport_value - ED.real_sum_value))


        present_node.Connections_OUT.append(choosing_node)  # Отмечаем направление передачи
        choosing_node.Connections_IN.append(present_node)  # для контактирующих узлов


        Used[Path[-1][0]][choosing_node] = 1  # Отмечаем найденный узел как использованный
        Path.append([choosing_node, send_value])  # Добавляем его в путь
        present_node = Path[-1][0]  # Начинаем строить путь от этого узла на следующей итерации

        Nsends += 1

        if (choosing_node == trouble_node):
            flag = True


    return Nodes_Dict, Path, True

#-----------------------------------------------------------------------------
