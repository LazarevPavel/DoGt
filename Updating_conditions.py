from Obj_classes import *
from math import fabs

#-------------------------------------------------------------------------

def Update_conditions_values(Nodes_Dict, one_node):
    '''Пересчитываем все значения ограничений для узла'''

    #Считаем входящий и исходящий оборот
    turnover_in = 0
    turnover_out = 0

    for ED in Nodes_Dict[one_node]:
        if (len(ED.transport_value) != 0):
            for i in range(len(ED.transport_value)):
                if (ED.transport_value[i][0] > 0):
                    turnover_in += ED.transport_value[i][0]
                elif (ED.transport_value[i][0] < 0):
                    turnover_out += ED.transport_value[i][0]

    #Запоминаем обороты
    for one in Nodes_Dict.keys():
        if (one == one_node):
            one.IN_turnover_value = turnover_in
            one.OUT_turnover_value = -turnover_out
            break



    # Считаем кол-во входящих и исходящих связей
    sum_in = 0
    sum_out = 0
    for ED in Nodes_Dict[one_node]:
        if(len(ED.transport_value) != 0):
            if (ED.destination == one_node):
                sum_in += 1
            elif (ED.source == one_node):
                sum_out += 1

    #Запоминаем кол-во связей
    for one in Nodes_Dict.keys():
        if (one == one_node):
            one.IN_edges_real = sum_in
            one.OUT_edges_real = sum_out
            break



    #Считаем расчётный процент выхода
    for one in Nodes_Dict.keys():
        if (one == one_node):
            if (one.OUT_turnover_value != 0):
                one.Exit_out_edges_real = one.end_value / (one.OUT_turnover_value + one.end_value)
            else:
                one.Exit_out_edges_real = None
            break



    #Считаем сумму передач для связей узла
    for ED in Nodes_Dict[one_node]:
        Sum = 0
        for send in ED.transport_value:
            Sum += fabs(send[0])
        ED.real_sum_value = Sum


    return Nodes_Dict

#----------------------------------------------------------------------------------------