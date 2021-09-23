import Obj_classes
import networkx
from fa2l import force_atlas2_layout

#------------------------------------------
#Функция подбора визуально приятной развёртки графа

def Find_node_positions(Result_Dict):
    Graph = networkx.DiGraph()  #Создаём ориентированный граф

    #Выстраиваем узлы и связи между ними, которые имеются в решении
    for one_node in Result_Dict.keys():
        for one_edge in Result_Dict[one_node]:
            Graph.add_edge(one_edge.source, one_edge.destination)

    #Высчитываем координаты узлов на плоскости, чтобы визуально граф был смотрибельным
    positions = force_atlas2_layout(Graph,
                                    None,
                                    iterations=1000,
                                    outbound_attraction_distribution=False,
                                    lin_log_mode=False,
                                    prevent_overlapping=False,
                                    edge_weight_influence=1.0,
                                    jitter_tolerance=1.0,
                                    barnes_hut_optimize=True,
                                    barnes_hut_theta=0.5,
                                    scaling_ratio=10000.0,
                                    strong_gravity_mode=False,
                                    multithread=False,
                                    gravity=1.0)

    print('\nКоординаты узлов на графе:\n', positions)
    return positions  #Возвращаем словарь координат