from Obj_classes import *


def Early_checking(Nodes_Dict):
    """Проверяем систему узлов и связей на первоначальную возможность распределения"""

    #---------------------------------------
    #Проверка на связность с графа
    nodes = []
    for node in Nodes_Dict:
        if len(node.Allowed_connections) == 0:
            nodes.append(node.name)

    if(len(nodes) > 0):
        error_str = "Распределение невозможно.\n\nПроблема: узлы не имеет(-ют) связей ни с одним из узлов.\n\nПроблемные узлы: "

        for i in range(len(nodes)):
            error_str += nodes[i]
            if (i != len(nodes) - 1):
                error_str += ', '

        error_str += "\n\n\nВарианты решения проблемы:\n\n1. Измените коды и/или классы узлов так, чтобы все узлы представляли единую систему без разрывов на отдельные части."
        return False, error_str

    #---------------------------------------

    #Проверка на достижимость распределения при максимальном проценте выхода
    nodes = []
    for node in Nodes_Dict:
        sum = 0
        max_edges = node.OUT_edges_max
        for ED in Nodes_Dict[node]:
            if(ED.active == 1):
                sum += ED.MAX_transport_value
                max_edges -= 1
                if(max_edges == 0):
                    break

        for ED in Nodes_Dict[node]:
            if(ED.active != 1):
                sum += max_edges*ED.MAX_transport_value
                break

        if sum < (node.end_value/node.Exit_out_edges_max_beg - node.end_value):
            nodes.append(node.name)


    if(len(nodes) > 0):
        error_str = "Распределение невозможно.\n\nПроблема: Максимальный процент выхода узлов в указанном диапазоне слишком мал для удачного распределения.\n\nПроблемные узлы: "

        for i in range(len(nodes)):
            error_str += nodes[i]
            if(i != len(nodes)-1):
                error_str += ', '

        error_str += "\n\n\nВарианты решения проблемы:\n\n1. Увеличьте максимальный процент выхода для проблемных узлов.\n\n2. Увеличьте максимум значения на связи для проблемных узлов."
        return False, error_str
    #---------------------------------------------

    #Проверка достаточности количества узлов для связи с ограничениями на кол-ва свзяи
    nodes = []
    for node in Nodes_Dict:
        if (len(node.Allowed_connections) < node.OUT_edges_min + node.IN_edges_min):
            nodes.append(node.name)

    if (len(nodes) > 0):
        error_str = "Распределение невозможно.\n\nПроблема: слишком малое возможное кол-во узлов, с которыми может связаться узел. Это приведёт к невыполнению ограничения на минимальное кол-во связей.\n\nПроблемные узлы: "

        for i in range(len(nodes)):
            error_str += nodes[i]
            if(i != len(nodes)-1):
                error_str += ', '

        error_str += "\n\n\nВарианты решения проблемы:\n\n1. Понизьте требуемый минимум на кол-во связей (входящих или исходящих, или обоих видов).\n\n2. Измените коды или классы проблемных узлов таким образом, чтобы данные узлы имели большее возможное кол-во узлов для построения связи."
        return False, error_str

    #------------------------------------------------




    return True, "It's all OK!"