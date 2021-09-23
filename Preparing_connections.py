from Obj_classes import *

#---------------------------------------------------------------------

def Finding_allowed_connections(Nodes_Dict, Edges_list):
    '''Отбираем для каждого узла те узлы, с которыми можно связаться'''
    for one_node in Nodes_Dict.keys():  #Перебираем все пары узлов
        for another_node in Nodes_Dict.keys():
            if (one_node != another_node and one_node.code != another_node.code):  #Если узел не попадает сам на себя и коды узлов в паре не равны
                for i in one_node.class_numbers:  # то сравниаем классы этих узлов
                    # Если хотя бы один класс совпадает или один из классов равен нулю
                    if (i in another_node.class_numbers or 0 in another_node.class_numbers or 0 in one_node.class_numbers):
                        one_node.Allowed_connections.append(another_node)  # Вносим узел в список узлов, с которыми можно связываться рассматриваемому узлу
                        break  # Перестаём сравнивать классы и переходим к следующему узлу


    #Исключаем запрещённые связи согласно таблице "Связи"
    for one_node in Nodes_Dict.keys():
        for another_node in one_node.Allowed_connections:
            for ED in Edges_list:
                if ED.MIN_transport_value > 0:
                    ED.active = 1
                if (ED.source == one_node.name and ED.destination == another_node.name): #Если есть запрещённая связь
                    if (ED.MAX_transport_value <= 0):
                        one_node.Allowed_connections.remove(another_node) #Убираем её


    #Делаем ссылку на узел-источник и узел-получатель по ссылке, а не по имени
    for one_node in Nodes_Dict.keys():
        for another_node in Nodes_Dict.keys():
            for ED in Edges_list:
                if (ED.source == one_node.name and ED.destination == another_node.name):
                    ED.source = one_node
                    ED.destination = another_node


    print('Finding_allowed_connections finished')

    return Nodes_Dict


#----------------------------------------------------------------------


def Creating_Node_Edges(Nodes_Dict, Edges_list):
    """Создаём все возможные связи между узлами, но пока что пустые"""

    #Идём по всем узлам
    for one_node in Nodes_Dict.keys():
        for another_node in Nodes_Dict.keys():
            if(another_node in one_node.Allowed_connections): #Если связь узлов разрешена
                #Создаём стандартную связь между узлами
                one_edge = Edge(one_node, another_node)
                Nodes_Dict[one_node].append(one_edge)

                another_edge = Edge(one_node, another_node)
                Nodes_Dict[another_node].append(another_edge)


    #Назначаем особые свойства узлов, если такие были заданы
    for ED in Edges_list:
        for node in Nodes_Dict.keys():
            for EDN in Nodes_Dict[node]:
                if (ED.source == EDN.source  and  ED.destination == EDN.destination):
                    EDN.active = ED.active
                    EDN.MIN_transport_value = ED.MIN_transport_value
                    EDN.MAX_transport_value = ED.MAX_transport_value
                    EDN.source.Connections_OUT.append(EDN.destination)
                    EDN.destination.Connections_IN.append(EDN.source)

    print('Creating_node_edges finished')

    return Nodes_Dict

#----------------------------------------------------------------------