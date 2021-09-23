from Obj_classes import *
from math import fabs


def Type_decide(one_node, Nodes_Dict):
        """Определение типа узла (отдающий, принимающий, в балансе, отдающий без возможности отдать, принимающий без возможности принять)
           На входе: один узел с не пустыми начальными и конечными значениями
           На выходе: тип проверяемого узла"""

        difference = one_node.real_value - one_node.end_value  #Начальный ресурс - Конечный ресурс = показатель типа узла
        if (difference > 0):   # Если показатель больше 0,
            one_node.type = -2  #то узел - отдающий.
            one_node.type = Finding_nodes_to_give_out(one_node, Nodes_Dict, difference)  #Проверяем сможет ли узел раздать свои избытки

        elif (difference < 0): #Если показатель меньше 0,
            one_node.type = 2   #то узел - принимающий.
            one_node.type = Finding_nodes_to_take_out(one_node, Nodes_Dict, difference)  #Проверяем, сможет ли узел покрыть свои нехватки

        else:
            one_node.type = 0  # В ином случае узел находится в состоянии баланса



        return one_node.type


#---------------------------------------------------------------------


def Finding_nodes_to_give_out(one_node, Nodes_Dict, difference):
    '''Проверяем, сможет ли отдающий узел прийти в состояние баланса (сможет ли раздать всем свои избыточные ресурсы)'''

    another_difference_sum = 0  # Сумма значений того, сколько не хватает принимающему узлу до баланса
    for temp_node in Nodes_Dict.keys():  # Идём по узлам
        if (one_node != temp_node  and  temp_node in one_node.Allowed_connections and temp_node not in one_node.Connections_IN):  # Если узел не попал сам на себя и связь с узлом разрешена
            another_difference = temp_node.real_value - temp_node.end_value  # то считаем разницу настоящего значения и конечного
            if (another_difference < 0):  # Если узел оказался принимающим (недостача ресурсов до баланса)
                another_difference_sum += another_difference * -1  # Суммируем кол-во недостающего ресурса с положит. значением
    # После суммирования
    if (difference > another_difference_sum):  # Если проверяемый узел может покрыть нехватки других узлов, с которыми разрешена связь, и ещё останется запас
        one_node.type = -2  # Баланс узла будет недостижим (состояние "Могу всем отдать, но ресурсы ещё останутся")

    return one_node.type


#----------------------------------------------------------------------


def Finding_nodes_to_take_out(one_node, Nodes_Dict, difference):
    '''Проверяем, сможет ли принимающий узел прийти в состояние баланса (сможет ли удовлетворить свои нехватки)'''

    another_difference_sum = 0  # Сумма значений того, сколько нужно раздать одающему узлу для достижения баланса
    for temp_node in Nodes_Dict.keys():  # Идём по узлам
        if (one_node != temp_node  and  temp_node in one_node.Allowed_connections and temp_node not in one_node.Connections_OUT):  # Если узел не попал сам на себя и связь с узлом разрешена
            another_difference = temp_node.real_value - temp_node.end_value  # то считаем разницу настоящего значения и конечного
            if (another_difference > 0):  # Если узел оказался отдающим (избыток ресурсов до баланса)
                another_difference_sum += another_difference  # Суммируем кол-во недостающего ресурса с положит. значением
    # После суммирования
    if (difference * -1 > another_difference_sum):  # Если проверяемый узел может забрать избыттки всех возможных узлов
        one_node.type = 2    #Баланс узла будет недостижим (состояние "Могу забрать у всех, но нехватка не устранится")

    return one_node.type

#----------------------------------------------------------------------