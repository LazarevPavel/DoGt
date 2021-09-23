from Data_prepare import *
from Obj_classes import *
from Calculate_functions import *
from Export_result import *
import random

def Duplicate_checking(Nodes_list):
    # ---------------------------------------
    # Исключаем ситуацию, когда есть несколько узлов с одинаковым именем
    trouble_nodes = []
    for i in range(len(Nodes_list) - 1):
        for j in range(i + 1, len(Nodes_list)):
            if (Nodes_list[i].name == Nodes_list[j].name):
                trouble_nodes.append(Nodes_list[i].name)

    if (len(trouble_nodes) > 0):
        error_str = "Ошибка в данных.\n\nПроблема: некоторые узлы имеют одинаковые имена.\n\nПовторяющиеся имена: "

        for i in range(len(trouble_nodes)):
            error_str += trouble_nodes[i]
            if (i != len(trouble_nodes) - 1):
                error_str += ', '

        error_str += "\n\n\nВариант решения проблемы:\n\nИсключите повторяющиеся имена в данном списке узлов."

        return error_str

    return True

#------------------------------------------------



def Start_Working(File_input):

    #ПОДГОТОВКА ДАННЫХ К РАСЧЁТУ
    Nodes_list, Edges_list, error_str = Data_Prepare(File_input) #Парсинг файла и перевод данных в список узлов

    #Если во время парсинга возникла ошибка
    if (type(" ") == type(error_str)):
        print(error_str)
        return error_str, None, None, None



    Nodes_count = len(Nodes_list)         #Количество узлов

    #Проверка узлов на наличие дублирующих имён
    error_str = Duplicate_checking(Nodes_list)
    if(type(" ") == type(error_str)):
        print(error_str)
        return error_str, None, None, None


    for i in Nodes_list:
        print(i.name, '------', i.class_numbers)


    for i in range(1000000):
        print('ИТЕРАЦИЯ', i)

        random.shuffle(Nodes_list)

        #Загоняем список узлов в функцию для РАСЧЁТА и получаем результат
        Result_Dict, flag, error_str = Calculating_Edges(Nodes_list, Edges_list)


        if(flag == 'Finish!'):   #Если распределние было достигнуто
            #Запись результата в Excel
            #Write_to_Excel(Result_Dict, Nodes_count, File_input, "Result.xls")
            return True, Nodes_list, Edges_list, Result_Dict

        elif (flag == True):

            print(error_str)

            # ОБНУЛЯЕМ ЗНАЧЕНИЯ ДЛЯ НОВОГО КРУГА
            for node in Nodes_list:
                node.Clear_params()

            for edge in Edges_list:
                edge.Clear_params()

            continue

        elif (flag==False):
            print(error_str)
            return error_str, Nodes_list, Edges_list, Result_Dict

        if i == 1000000-1:
            print('К сожалению, не получилось сгенерировать решение.')
            return 'К сожалению, не получилось сгенерировать решение.', Nodes_list, Edges_list, Result_Dict

#Запуск расчёта (на случай работы без граф. интерфейса)
#Start_Working('NachalnyeDannye.xls')