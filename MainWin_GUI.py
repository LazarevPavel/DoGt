from PyQt5 import QtWidgets #, QtCore, QtGui
import Interface.MainWindow as Design_MainWin
from GraphicsFrame_GUI import Graphics_Frame
from Export_result import Write_to_Excel
from os.path import exists
import threading
from Data_prepare import Data_Prepare
from Calc_thread import Calc_Thread
from Loading_animate_thread import Loading_animate
from Drawning.Find_node_positions import Find_node_positions
from Drawning.Build_graphics_scene import Build_graphics_scene

#----------------------------------------------------------------------

class Main_Frame(QtWidgets.QMainWindow, Design_MainWin.Ui_MainWindow):
    '''Класс главного окна'''

    def __init__(self):
        # Это здесь нужно для доступа к переменным, методам
        # и т.д. в файле MainWindow.py
        super().__init__()
        self.setupUi(self)  # Это нужно для инициализации нашего дизайна
        self.File_input_button.clicked.connect(self.browse_file_input)    #Привязка к кнопке функции поиска входного файла
        self.File_output_button.clicked.connect(self.browse_file_output)  #Привязка к кнопке функции указания директории для выходного файла
        self.Calculate_button.clicked.connect(self.Calculate)             #Привязка к кнопке функции, начинающей весь рассчёт
        self.out_result_button.clicked.connect(self.Out_result)           #Привязка к кнопке функции, выводящей файл с результатом
        self.stop_button.clicked.connect(self.Stop_Calc)                  #Привязка к кнопке функции остановки расчёта решения
        self.Make_visual_button.clicked.connect(self.Make_visualization)  #Привязка к кнопке функции визуализации графа

        # структуры для оперирования узлами и связями
        self.error_str = ''                #Строка ошибок - что-то вроде индикатора успешности расчёта
        self.Nodes_list = []               #Список всех узлов
        self.Edges_list = []               #Список связей, указанных вручную в файле эксель
        self.old_Edges_list = []
        self.Result_Dict = {}              #Словарь итогового решения
        self.old_Result_Dict = {}
        self.string_loading = 'Генерирую решение'  #Строка для анимации
        self.positions = None

        #Все создаваемые новые окна
        self.GraphicsFrame = None

        #Тестова фигня, чтобы не париться
        #self.File_url_output.setText('C:/Users/Mvideo/PycharmProjects/Graph_Alogrithm')
        #self.Edit_filename_output.setText('Result')

        self.Calculate_button.setEnabled(False)
        self.Make_visual_button.setEnabled(False)
    #----------------------------------------------------------------------

    #Закрытие всех окон при закрытии главного окна
    def closeEvent(self, e):
        self.GraphicsFrame.close()
        self.close()

    #-----------------------------------------------------------------------

    #Функция для ручного поиска входного файла по проводнику
    def browse_file_input(self):
        file = QtWidgets.QFileDialog.getOpenFileName(self, "Выберите файл")  #Открывается окно поиска по "проводнику"
        if file:             #Если файл был выбран
            file = file[0]   #Берём путь до файла

            if exists(file):
                # ПОДГОТОВКА ДАННЫХ К РАСЧЁТУ
                self.Nodes_list, self.Edges_list, self.error_str = Data_Prepare(file)  # Парсинг файла и перевод данных в список узлов

                flag_early_error = False
                # Если во время парсинга возникла ошибка
                if (type(" ") == type(self.error_str)):
                    flag_early_error = True
                    self.Ban_to_export()
                    self.Show_error(self.error_str)
                else: #если всё в порядке
                    self.File_url_input.setText(file)                   #Вставляем путь в поле ввода
                    self.Finish_label.setText('Файл загружен успешно')
                    self.Calculate_button.setEnabled(True)              #Разрешаем проводить вычисления

            else:
                self.error_str = "Некорректно указан путь до входного файла."
                self.Ban_to_export()
                self.Show_error(self.error_str)
    # -----------------------------------------------------------------------

    #Функция для ручного указания директории для выходного файла
    def browse_file_output(self):
        directory = QtWidgets.QFileDialog.getExistingDirectory()  #Открывается окно поиска по "проводнику"
        if directory:
            directory_path = ''
            for char in directory:
                directory_path += char                    #Берём путь до директории
            self.File_url_output.setText(directory)     #И помещаем в поле для ввода

    # -----------------------------------------------------------------------

    #Вывод ошибки в область ошибок
    def Show_error(self, error_str):
        self.Finish_label.setText('Возникли проблемы!')  # Меняем статус
        self.Finish_label.setStyleSheet('color: #ff0000')  # и его цвет
        self.Problems_text.setPlainText(error_str)

    # -----------------------------------------------------------------------

    #Разрешение на экспорт и последующую работу с данными
    def Allow_to_export(self):
        self.out_result_button.setEnabled(True)
        self.Make_visual_button.setEnabled(True)
        self.stop_button.setEnabled(False)

    # -----------------------------------------------------------------------

    #Запрет на экспорт и последующую работу с данными
    def Ban_to_export(self):
        self.out_result_button.setEnabled(False)
        #self.Make_visual_button.setEnabled(False)

    #------------------------------------------------------------------------
    def Stop_Calc(self):
        self.stop_button.setEnabled(False)

        Thread_list = threading.enumerate()

        for thread in Thread_list:
            if(thread.getName() == "Loading_Thread"):
                thread.stop_flag = True
                thread.join()

        for thread in Thread_list:
            if(thread.getName() == "Calc_Thread"):
                thread.stop_flag = True

        self.Ban_to_export()
        self.stop_button.setEnabled(False)
        self.Calculate_button.setEnabled(True)

    # -----------------------------------------------------------------------

    #Функция, запускающая алгоритм расчёта
    def Calculate(self):
        self.Calculate_button.setEnabled(False)
        self.out_result_button.setEnabled(False)
        self.stop_button.setEnabled(True)

        thread = Calc_Thread(self, 'Calc_Thread')
        thread.start()

        thread_load = Loading_animate(self, thread, 'Loading_Thread')
        thread_load.start()


        #Если же проблемы всё-таки возникли
        if (type(' ') == type(self.error_str)):
            if(self.error_str != ''):
                self.Show_error(self.error_str)
                self.Ban_to_export()

    # -----------------------------------------------------------------------

    #Вывод результата распределения в файл
    def Out_result(self):
        IN = self.File_url_input.toPlainText()
        OUT = self.File_url_output.toPlainText()  # Берём путь до директории выходного файла
        OUT += '/' + self.Edit_filename_output.toPlainText() + '.xls'  # Добавляем имя файла к пути сохранения


        #Если входной файл ещё существует
        if exists(IN):
            #то выводим решение в файл
            Write_to_Excel(self.old_Result_Dict, len(self.Nodes_list), IN, OUT)
            self.Finish_label.setStyleSheet('color: rgb(0, 170, 0);')
            self.Finish_label.setText('Файл результата успешно создан!')
            self.Problems_text.clear()
        else:
            self.error_str = "Некорректно указан путь до входного файла."
            self.Show_error(self.error_str)

    # -----------------------------------------------------------------------
    #------------------------------------------------------------------------

    #Метод, создающий визуализацию
    def Make_visualization(self):
        if self.Result_Dict:  #Если итоговое решение было найдено
            #Просчитываем развёртку графа, задавая координаты узлов на плоскости
            self.positions = Find_node_positions(self.Result_Dict)

            # Делаем ссылку на узел-источник и узел-получатель по ссылке, а не по имени
            for one_node in self.old_Result_Dict.keys():
                for another_node in self.old_Result_Dict.keys():
                    for ED in self.Edges_list:
                        if (ED.source == one_node.name and ED.destination == another_node.name):
                            ED.source = one_node
                            ED.destination = another_node


            #Создаём сцену для отрисовки и связываем объекты сцены (узлы и связи) с логическими объектами модели
            Scene, Nodes_visual, Nodes_labels_visual, Edges_visual = Build_graphics_scene(self.positions, self.old_Result_Dict, self.old_Edges_list)

            self.GraphicsFrame = Graphics_Frame(self, Scene, Nodes_visual, Nodes_labels_visual, Edges_visual)
            self.GraphicsFrame.show()
