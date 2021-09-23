from PyQt5 import QtWidgets, QtCore, QtGui
import Interface.MainWindow as Design_MainWin
from Start_code import *
from pandas.errors import DtypeWarning, EmptyDataError, ParserError, UnsortedIndexError
# from Graph_visualization_algorithms import Find_good_visual_positions
import threading
import copy


# -----------------------------------------------

class Calc_Thread(threading.Thread):
    def __init__(self, Main_Frame, name):
        super().__init__()
        self.Main_Frame = Main_Frame
        self.name = name
        self.stop_flag = False
        self.setDaemon(daemonic=True)

    def run(self):
        Nodes_list = self.Main_Frame.Nodes_list
        Edges_list = self.Main_Frame.Edges_list
        error_str = " "

        Nodes_count = len(Nodes_list)  # Количество узлов

        # ОБНУЛЯЕМ ЗНАЧЕНИЯ ДЛЯ СОХРАНЕНИЯ ЧИСТОТЫ РАСЧЁТА
        for node in Nodes_list:
            node.Clear_params()
        for edge in Edges_list:
            edge.Clear_params()


        flag_early_error = False
        # Проверка узлов на наличие дублирующих имён
        error_str = Duplicate_checking(Nodes_list)
        if (type(" ") == type(error_str)):
            print(error_str)
            flag_early_error = True



        Result_Dict = {}
        for i in range(30000):
            if(flag_early_error == True):
                break

            if (self.stop_flag == True):
                print("OK_EXIT")
                break

            print('ИТЕРАЦИЯ', i)

            random.shuffle(Nodes_list)

            # Загоняем список узлов в функцию для РАСЧЁТА и получаем результат
            Result_Dict, flag, error_str = Calculating_Edges(Nodes_list, Edges_list)

            if (flag == 'Finish!'):  # Если распределние было достигнуто
                error_str = True
                break

            elif (flag == True):

                print(error_str)

                # ОБНУЛЯЕМ ЗНАЧЕНИЯ ДЛЯ НОВОГО КРУГА
                for node in Nodes_list:
                    node.Clear_params()

                for edge in Edges_list:
                    edge.Clear_params()

                continue

            elif (flag == False):
                print(error_str)
                break

            if i == 1000000 - 1:
                print('К сожалению, не получилось сгенерировать решение.')
                error_str = 'К сожалению, не получилось сгенерировать решение.'
                break


        # Если поток не остановили преждевременно
        if (self.stop_flag == False):
            # Если проблем не возникло
            self.Main_Frame.error_str = error_str

            for node in Result_Dict:
                for ED in Result_Dict[node]:
                    print(ED.source.name, ED.destination.name, ED.real_sum_value)

            if (self.Main_Frame.error_str == True or self.Main_Frame.error_str == 'Решение было найдено, но с некоторыми допущениями по ограничению на минимум связей для каждого узла'):
                self.Main_Frame.Result_Dict = Result_Dict
                self.Main_Frame.old_Result_Dict = copy.copy(self.Main_Frame.Result_Dict)
                self.Main_Frame.old_Edges_list = copy.copy(self.Main_Frame.Edges_list)

                self.Main_Frame.Problems_text.clear()  # Очищаем поле ошибок

                if(self.Main_Frame.error_str == True):
                    self.Main_Frame.Finish_label.setStyleSheet('color: rgb(0, 170, 0);')
                    self.Main_Frame.Finish_label.setText('Готово!')  # По выполнении уведомляем пользователя надписью ниже главной кнопки
                if(self.Main_Frame.error_str == 'Решение было найдено, но с некоторыми допущениями по ограничению на минимум связей для каждого узла'):
                    self.Main_Frame.Finish_label.setStyleSheet('color: rgb(0, 0, 170);')
                    self.Main_Frame.Finish_label.setText('Решение найдено, но с некоторыми ограничениями')
                    self.Main_Frame.Problems_text.setPlainText(error_str)

                self.Main_Frame.Calculate_button.setEnabled(True)
                self.Main_Frame.Allow_to_export()  # Разрешаем дальнейшую работу с данными


            # Если же проблемы всё-таки возникли
            elif (type(' ') == type(self.Main_Frame.error_str)):
                self.Main_Frame.Show_error(self.Main_Frame.error_str)
                self.Main_Frame.Calculate_button.setEnabled(True)
                self.Main_Frame.stop_button.setEnabled(False)
                self.Main_Frame.Make_visual_button.setEnabled(True)

                for ED in self.Main_Frame.Edges_list:
                    # Переводим ссылку на узлы в имена узлов для избежания ошибки при пересчёте
                    ED.source = ED.source.name
                    ED.destination = ED.destination.name

                self.Main_Frame.Ban_to_export()

        else:
            print("OK_EXIT")
            self.Main_Frame.Finish_label.setStyleSheet('color: rgb(0, 170, 0);')
            self.Main_Frame.Finish_label.setText('Генерация решения была остановлена')
            self.Main_Frame.Calculate_button.setEnabled(True)
            self.Main_Frame.Make_visual_button.setEnabled(True)

            if len(self.Main_Frame.Edges_list) != 0:
                if (type(self.Main_Frame.Edges_list[0].source) != type('name')):
                    for ED in self.Main_Frame.Edges_list:
                        # Переводим ссылку на узлы в имена узлов для избежания ошибки при пересчёте
                        ED.source = ED.source.name
                        ED.destination = ED.destination.name

            self.Main_Frame.Ban_to_export()
            self.stop_flag = False
# --------------------------------------------