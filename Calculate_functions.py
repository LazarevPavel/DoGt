from Obj_classes import *
from Balance_checking import *
from Type_decide import *
from Preparing_connections import *
from Updating_conditions import *
from Early_checking import *
from Pathfinder import *
from Exit_regulating import *
import random

#--------------------------------------------------------------------------

def Find_edge(one_node, second_node, Nodes_Dict):
    '''Поиск связи по указанному источнику и получателю'''

    for ED in Nodes_Dict[one_node]:
        if(ED.source == one_node and ED.destination == second_node):
            print('Find edge finished')
            return ED


#--------------------------------------------------------------------------


def Find_max_taking_node(one_node, Nodes_Dict):
    """Поиск принимающего узла, который может принять больше ресурсов, чем другие принимающие узлы.
       Поиск узлов идёт только среди тех, с которыми отдающий узел может связаться напрямую"""

    second_node = None
    max_send_value = -1
    #nodes = []
    for temp_node in Nodes_Dict.keys():  # Идём по всем узлам
        if (temp_node.type == 2 and temp_node in one_node.Allowed_connections and temp_node not in one_node.Connections_IN):  # В первую очередь ищем узлы с большими нехватками
            node_send_value = temp_node.end_value - temp_node.real_value  # Считаем, сколько ресурсов узел может принять,
            if (node_send_value > max_send_value):  # и если это значение больше нынешнего максимального,
                max_send_value = node_send_value  # то запоминаем это значение
                second_node = temp_node  # и запоминаем этот узел
            #nodes.append(temp_node)

    if(second_node != None):
        #second_node = random.choice(nodes)
        return second_node

    max_send_value = -1
    for temp_node in Nodes_Dict.keys():  # Идём по всем узлам
        if (temp_node.type == 1 and temp_node in one_node.Allowed_connections and temp_node not in one_node.Connections_IN):  # Если находим принимающий узел
            node_send_value = temp_node.end_value - temp_node.real_value  # Считаем, сколько ресурсов узел может принять,
            if (node_send_value > max_send_value):  # и если это значение больше нынешнего максимального,
                max_send_value = node_send_value  # то запоминаем это значение
                second_node = temp_node  # и запоминаем этот узел
            #nodes.append(temp_node)

    print('Find max taking node finished')

    #second_node = random.choice(nodes)
    return second_node


#----------------------------------------------------------------------


def Find_max_taking_node_from_ALL(Nodes_Dict):
    '''Поиск принимающего узла, который может принять больше ресурсов, чем другие принимающие узлы.
       Поиск осуществляется среди всех узлов'''

    second_node = None
    max_send_value = -1
    nodes = []
    for temp_node in Nodes_Dict.keys():  # Идём по всем узлам
        if (temp_node.type == 2):  # Если находим узел, который не может покрыть свои нехватки
            node_send_value = temp_node.end_value - temp_node.real_value  # Считаем, сколько ресурсов узел может принять,
            if (node_send_value > max_send_value):  # и если это значение больше нынешнего максимального,
                max_send_value = node_send_value  # то запоминаем это значение
                second_node = temp_node  # и запоминаем этот узел
            nodes.append(temp_node)


    if (second_node != None):
        second_node = random.choice(nodes)
        return second_node

    max_send_value = -1
    for temp_node in Nodes_Dict.keys():  # Идём по всем узлам
        if (temp_node.type == 1):  # Если находим принимающий узел
            node_send_value = temp_node.end_value - temp_node.real_value  # Считаем, сколько ресурсов узел может принять,
            if (node_send_value > max_send_value):  # и если это значение больше нынешнего максимального,
                max_send_value = node_send_value  # то запоминаем это значение
                second_node = temp_node  # и запоминаем этот узел
            #nodes.append(temp_node)


    print('Find max taking node FROM ALL finished')

    #second_node = random.choice(nodes)
    return second_node


#--------------------------------------------------------------------------------------------


def Calculating_Edges(Nodes_list, Edges_list):
    """Производит расчёт распределения ресурсов между узлами,
       осуществляет построение транспортных связей между узлами"""

    Nodes_Dict = {}  # Будущая матрица смежности
    for node in Nodes_list:  # Каждый узел заносим в словарь в качестве ключа
        Nodes_Dict.update({node: []})  # этот ключ будет ссылаться на список связей данного узла с другими узлами

    #Заполняем списки узлов, между которыми разрешена связь
    Nodes_Dict = Finding_allowed_connections(Nodes_Dict, Edges_list)

    #Создаём для каждого узла связи (без передачи значений) с каждым разрешённым узлом
    Nodes_Dict = Creating_Node_Edges(Nodes_Dict, Edges_list)

    #----------------------------------
    #Перед распределением проверяем возможность распределения с такими данными
    check_flag, error_str = Early_checking(Nodes_Dict)

    if(check_flag == False):
        return Nodes_Dict, False, error_str

    #----------------------------------




    # Определим типы узлов (принимающий, отдающий, в балансе)
    for one_node in Nodes_Dict:                            #Идём по всем узлам
        one_node.type = Type_decide(one_node, Nodes_Dict)  #Определяем состояние каждого узла


    # Подсчитываем показатели по ограничениям для всех узлов
    for node in Nodes_Dict:
        Update_conditions_values(Nodes_Dict, node)

    for one_node in Nodes_Dict:
        one_node.type = Type_decide(one_node, Nodes_Dict)


    # НАЧАЛО РАСЧЁТА
    flag = False  # Распределение ещё не завершено
    flag_2 = False
    while (flag != True):  # Пока распределение не будет завершено
        while (flag_2 != True):
            print('Начинаем прямые передачи')
            for first_node in Nodes_Dict.keys():  # Идём по всем узлам
                if (first_node.type == -1):  # Если находим ОТДАЮЩИЙ узел,


                    #то ищем принимающий узел, чья надобность в ресурсах будет максимальной
                    second_node = Find_max_taking_node(first_node, Nodes_Dict)
                    if (second_node is None):  #Если не находится принимающий узел, то выкидываем сообщение, перепроверяем состояние узла и пропускаем этот узел
                        print('Узел', ' "', first_node.name, '" ', 'не может передать ресурсы, т.к. нет принимающих узлов в доступности')
                        first_node.type = Type_decide(first_node, Nodes_Dict)
                        continue


                    #Ищем связь между двумя узлами
                    temp_edge = Find_edge(first_node, second_node, Nodes_Dict)
                    if(first_node in second_node.Connections_OUT):
                        continue
                        #one_node.type = -2
                        #second_node.type = 2
                    elif(temp_edge.MAX_transport_value <= temp_edge.real_sum_value):
                        one_node.type = -2
                        second_node.type = 2
                        continue


                    #Определяем, передать найденному узлу всё, что есть
                    #или принимающий узел не вместит всё, и придётся передать столько, сколько ему нужно
                    #или передаваемое значение слишком мало и придётся передать тот минимум, который пропустит связь
                    send_value = min(first_node.real_value - first_node.end_value, second_node.end_value - second_node.real_value)
                    send_value = min(send_value, fabs(temp_edge.MAX_transport_value - temp_edge.real_sum_value) )


                    #Фиксируем пересылки между отдающим и принимающим узлами
                    for ED in Nodes_Dict[first_node]:     #Фиксируем отдачу
                     if (ED.source == first_node and ED.destination == second_node):
                        ED.transport_value.append([-send_value])

                    for ED in Nodes_Dict[second_node]:  #Фиксируем приём
                     if (ED.source == first_node and ED.destination == second_node):
                        ED.transport_value.append([send_value])


                    #Меняем актуальные значения узлов
                    first_node.real_value -= send_value  # Отнимаем переданное значение от отдающего узла
                    second_node.real_value += send_value  # Добавляем переданное значение к принимающему узлу

                    first_node.Connections_OUT.append(second_node) #Отмечаем направление передачи
                    second_node.Connections_IN.append(first_node)  #для контактирующих узлов

                    #Пересчитываем состояния взаимодействовавших узлов
                    for node in Nodes_Dict.keys():
                        node.type = Type_decide(node, Nodes_Dict)

                    #Пересчитаем все условия ограничений для взаимодействовавших узлов
                    for node in Nodes_Dict.keys():
                        Nodes_Dict = Update_conditions_values(Nodes_Dict, node)


            for node in Nodes_Dict.keys():
                node.type = Type_decide(node, Nodes_Dict)

            for node in Nodes_Dict.keys():
                print(node.name, '----', node.type, '------', node.real_value, '------', node.IN_edges_real, '-------', node.OUT_edges_real, '----', node.Allowed_connections)


            check = True

            for node in Nodes_Dict.keys():
                if node.type == -1: #or node.type == 1:
                    check = False
                    break

            flag_2 = check


        print('Начинаем непрямые передачи')
        for first_node in Nodes_Dict.keys():  # Идём по всем узлам
            if (first_node.type == -2 or first_node.type == -1):   #Если нам попался узел, который не может отдать ресурсы напрямую
                second_node = Find_max_taking_node_from_ALL(Nodes_Dict)   #Найдём узел с самой большой нехваткой среди всех узлов

                #Найдём путь до найденного узла
                Nodes_Dict, Path, error_str = Path_to_node(Nodes_Dict, first_node.name, second_node.name)

                if (type(error_str) == type(' ')):
                    return Nodes_Dict, True, error_str

                min_send_value = Path[0][1]
                for i in range(len(Path)):
                    if (Path[i][1] < min_send_value):
                        min_send_value = Path[i][1]

                for i in range(len(Path)-1):
                    present_node = Path[i][0]
                    choosing_node = Path[i+1][0]

                    # Осуществляем пересылки
                    for ED in Nodes_Dict[present_node]:
                        if (ED.source == present_node and ED.destination == choosing_node):
                            min_send_value = min(min_send_value,  ED.MAX_transport_value - ED.real_sum_value)
                            ED.transport_value.append([-min_send_value, first_node, second_node])

                    for ED in Nodes_Dict[choosing_node]:
                        if (ED.source == present_node and ED.destination == choosing_node):
                            min_send_value = min(min_send_value, ED.MAX_transport_value - ED.real_sum_value)
                            ED.transport_value.append([min_send_value, first_node, second_node])

                    present_node.real_value += -min_send_value
                    choosing_node.real_value += min_send_value

                    present_node.Connections_OUT.append(choosing_node)  # Отмечаем направление передачи
                    choosing_node.Connections_IN.append(present_node)  # для контактирующих узлов


                    for node in Nodes_Dict.keys():
                        node.type = Type_decide(node, Nodes_Dict)

                    # Пересчитаем значения при ограничениях для каждого узла
                    for node in Nodes_Dict.keys():
                        Nodes_Dict = Update_conditions_values(Nodes_Dict, node)



                # Пересчитываем состояния взаимодействовавших узлов
                for node in Nodes_Dict.keys():
                    node.type = Type_decide(node, Nodes_Dict)

                # Пересчитаем все условия ограничений для взаимодействовавших узлов
                for node in Nodes_Dict.keys():
                    Nodes_Dict = Update_conditions_values(Nodes_Dict, node)
                    #print(node.name, '----', node.IN_edges_real,  '----', node.OUT_edges_real)


        flag = Balance_Checking(Nodes_Dict) #Проверяем, все ли узлы находятся в состоянии баланса

        for node in Nodes_Dict.keys():
            print(node.name, '----', node.type)

        print('Непрямая отдача завершена')


        if(flag == True):
            flag_last = False
            while (flag_last != True):
                for node in Nodes_Dict.keys():
                    if (node.Exit_out_edges_real is None):
                        Nodes_Dict, Path, error_str = Exit_regulate(node, Nodes_Dict)

                        if (type(error_str) == type(' ')):
                            return Nodes_Dict, True, error_str

                        min_send_value = Path[0][1]
                        for i in range(len(Path)):
                            min_send_value = min(Path[i][1], min_send_value)

                        for i in range(len(Path) - 1):
                            present_node = Path[i][0]
                            choosing_node = Path[i + 1][0]

                            # Осуществляем пересылки
                            for ED in Nodes_Dict[present_node]:
                                if (ED.source == present_node and ED.destination == choosing_node):
                                    min_send_value = min(min_send_value,  ED.MAX_transport_value - ED.real_sum_value)
                                    ED.transport_value.append([-min_send_value, Path[0][0], Path[0][0]])

                            for ED in Nodes_Dict[choosing_node]:
                                if (ED.source == present_node and ED.destination == choosing_node):
                                    min_send_value = min(min_send_value,  ED.MAX_transport_value - ED.real_sum_value)
                                    ED.transport_value.append([min_send_value, Path[0][0], Path[0][0]])

                            present_node.real_value += -min_send_value
                            choosing_node.real_value += min_send_value

                            present_node.Connections_OUT.append(choosing_node)  # Отмечаем направление передачи
                            choosing_node.Connections_IN.append(present_node)  # для контактирующих узлов


                            for one_node in Nodes_Dict.keys():
                                one_node.type = Type_decide(one_node, Nodes_Dict)

                                if(fabs(one_node.real_value - one_node.end_value) <= one_node.allowed_difference_endvalue * one_node.end_value):
                                    one_node.type = 0

                            # Пересчитаем значения при ограничениях для каждого узла
                            for one_node in Nodes_Dict.keys():
                                Nodes_Dict = Update_conditions_values(Nodes_Dict, one_node)

                        print('Поиск ПЕТЛИ завершён удачно!', '  Целевой узел =', node.name, '   Процент выхода =', node.Exit_out_edges_real)


                    elif (node.Exit_out_edges_max < node.Exit_out_edges_real) and (node.Exit_out_edges_real - node.Exit_out_edges_max > node.Exit_out_edges_allowed_difference):
                        Nodes_Dict, Path, error_str = Exit_regulate(node, Nodes_Dict)

                        if (type(error_str) == type(' ')):
                            return Nodes_Dict, True, error_str


                        min_send_value = Path[0][1]
                        for i in range(len(Path)):
                            min_send_value = min(Path[i][1], min_send_value)

                        for i in range(len(Path) - 1):
                            present_node = Path[i][0]
                            choosing_node = Path[i + 1][0]

                            # Осуществляем пересылки
                            for ED in Nodes_Dict[present_node]:
                                if (ED.source == present_node and ED.destination == choosing_node):
                                    ED.transport_value.append([-min_send_value, Path[0][0], Path[0][0]])

                            for ED in Nodes_Dict[choosing_node]:
                                if (ED.source == present_node and ED.destination == choosing_node):
                                    ED.transport_value.append([min_send_value, Path[0][0], Path[0][0]])

                            present_node.real_value += -min_send_value
                            choosing_node.real_value += min_send_value

                            present_node.Connections_OUT.append(choosing_node)  # Отмечаем направление передачи
                            choosing_node.Connections_IN.append(present_node)  # для контактирующих узлов

                            for one_node in Nodes_Dict.keys():
                                one_node.type = Type_decide(one_node, Nodes_Dict)

                                if (fabs(one_node.real_value - one_node.end_value) <= one_node.allowed_difference_endvalue * one_node.end_value):
                                    one_node.type = 0


                            # Пересчитаем значения при ограничениях для каждого узла
                            for one_node in Nodes_Dict.keys():
                                Nodes_Dict = Update_conditions_values(Nodes_Dict, one_node)

                        print('Поиск ПЕТЛИ завершён удачно!', '  Целевой узел =', node.name, '   Процент выхода =', node.Exit_out_edges_real)

                flag_last = True
                for one_node in Nodes_Dict.keys():
                    if(one_node.Exit_out_edges_real is None):
                        flag_last = False
                    elif (one_node.Exit_out_edges_max < one_node.Exit_out_edges_real) and (one_node.Exit_out_edges_real - one_node.Exit_out_edges_max > node.Exit_out_edges_allowed_difference):
                        flag_last = False


        for one_node in Nodes_Dict.keys():
            one_node.type = Type_decide(one_node, Nodes_Dict)

        # Пересчитаем значения при ограничениях для каждого узла
        for one_node in Nodes_Dict.keys():
            Nodes_Dict = Update_conditions_values(Nodes_Dict, one_node)

        #----------------------
        sum_minus = 0
        sum_plus = 0

        for node in Nodes_Dict:
            if(node.type < 0):
                sum_minus += 1
            elif(node.type > 0):
                sum_plus += 1

        if(sum_minus == 0 and sum_plus != 0) or (sum_minus != 0 and sum_plus == 0):
            return Nodes_Dict, True, 'Ошибка при распределении'
        #-----------------------

        flag = Balance_Checking(Nodes_Dict)


    for node in Nodes_Dict:
        if(node.IN_edges_min > node.IN_edges_real or node.IN_edges_max < node.IN_edges_real) or (node.OUT_edges_min > node.OUT_edges_real or node.OUT_edges_max < node.OUT_edges_real):
            return Nodes_Dict, True, 'Несоответствие ограничениям на количество связей -----> '+ node.name


    sum_in = 0
    sum_out = 0
    edges_in = 0
    edges_out = 0
    for i in Nodes_Dict.keys():
        sum_in += i.IN_turnover_value
        sum_out += i.OUT_turnover_value
        edges_in += i.IN_edges_real
        edges_out += i.OUT_edges_real


    if(edges_out != edges_in):
        return Nodes_Dict, True, 'Итоговые кол-ва исходящих и входящих связей не равны друг другу'


    for node in Nodes_Dict:
        for ED in Nodes_Dict[node]:
            if ED.active == 1 and ED.real_sum_value < ED.MIN_transport_value:
                return Nodes_Dict, True, 'Не все обязательные связи достаточно задействованы'



    #Когда баланс узлов достигнут, то
    #КОНЕЦ РАСЧЁТА
    return Nodes_Dict, 'Finish!', True

#--------------------------------------------------------------------------------------------------------