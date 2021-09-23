from PyQt5 import QtWidgets, QtCore, QtGui
import Interface.GraphicsFrame as Design_GraphFrame
import copy
import random
import os
import tempfile


# ---------------------------------------------------


class Graphics_Frame(QtWidgets.QFrame, Design_GraphFrame.Ui_GraphicsFrame):
    '''Окно с визуализацией'''

    def __init__(self, Main_Frame, Scene, Nodes_visual, Nodes_labels_visual, Edges_visual):
        super().__init__()
        self.setupUi(self)

        # Объекты для работы с отрисовкой
        self.Scene = Scene  # Объект сцены для отрисовки
        self.Nodes_visual = Nodes_visual  # Словарь соответствия узлов их визуальному представлению
        self.Nodes_labels_visual = Nodes_labels_visual  # Словарь соответствия надписей узлов самим узлам
        self.Edges_visual = Edges_visual  # Словарь соответствия связей их визуальному представлению

        self.object_flag = -1  # флаг отметки, на какой объект в последний раз кликнули (0 - узел, 1 - связь)
        self.clicked_object_model = None  # для запоминания последнего выбранного объекта в модели
        self.clicked_object_visual = QtWidgets.QGraphicsRectItem()  # -//- на картинке
        self.prev_clicked_node_visual = QtWidgets.QGraphicsRectItem()  # Для запоминания предущего выбранного узла

        # Кнопка сохранения изменённых параметров узла или связи
        self.save_button = QtWidgets.QPushButton()
        self.save_button.setMaximumWidth(130)
        self.save_button.setText('Сохранить')
        self.save_button.clicked.connect(self.Save_object)

        #Сохранение изображения
        self.SavePicture_button.clicked.connect(self.Save_Picture)

        #Печать изображения
        self.Print_button.clicked.connect(self.Print_picture)

        # Обновляемые объекты GUI (отображение инфы об узлах, на которые кликнули)
        self.label_node_name = QtWidgets.QLabel()  # Название узла

        self.label_node_code = QtWidgets.QLabel()  # Код узла
        self.edit_node_code = QtWidgets.QTextEdit()
        self.edit_node_code.setFixedHeight(30)
        self.edit_node_code.setFixedWidth(80)

        self.label_node_StartValue = QtWidgets.QLabel()  # начальное значение узла
        self.edit_node_Start_value = QtWidgets.QTextEdit()
        self.edit_node_Start_value.setFixedHeight(30)
        self.edit_node_Start_value.setFixedWidth(80)

        self.label_node_EndValue = QtWidgets.QLabel()  # конечное значение узла
        self.edit_node_EndValue = QtWidgets.QTextEdit()
        self.edit_node_EndValue.setFixedHeight(30)
        self.edit_node_EndValue.setFixedWidth(80)

        self.label_node_IN_turnover = QtWidgets.QLabel()  # входящий оборот узла
        self.label_node_OUT_turnover = QtWidgets.QLabel()  # исходящий оборот узла

        self.label_node_IN_edges_min = QtWidgets.QLabel()  # минимум входящих связей
        self.edit_node_IN_edges_min = QtWidgets.QTextEdit()
        self.edit_node_IN_edges_min.setFixedHeight(30)
        self.edit_node_IN_edges_min.setFixedWidth(80)

        self.label_node_IN_edges_real = QtWidgets.QLabel()  # реальное количества входящих связей

        self.label_node_IN_edges_max = QtWidgets.QLabel()  # максимум входящих связей
        self.edit_node_IN_edges_max = QtWidgets.QTextEdit()
        self.edit_node_IN_edges_max.setFixedHeight(30)
        self.edit_node_IN_edges_max.setFixedWidth(80)

        self.label_node_OUT_edges_min = QtWidgets.QLabel()  # минимум исходящих связей
        self.edit_node_OUT_edges_min = QtWidgets.QTextEdit()
        self.edit_node_OUT_edges_min.setFixedHeight(30)
        self.edit_node_OUT_edges_min.setFixedWidth(80)

        self.label_node_OUT_edges_real = QtWidgets.QLabel()  # реальное количество исходящих связей

        self.label_node_OUT_edges_max = QtWidgets.QLabel()  # максимум исходящих связей
        self.edit_node_OUT_edges_max = QtWidgets.QTextEdit()
        self.edit_node_OUT_edges_max.setFixedHeight(30)
        self.edit_node_OUT_edges_max.setFixedWidth(80)

        self.label_node_MaxExitOut = QtWidgets.QLabel()  # максимальный процент выхода
        self.edit_node_MaxExitOut = QtWidgets.QTextEdit()
        self.edit_node_MaxExitOut.setFixedHeight(30)
        self.edit_node_MaxExitOut.setFixedWidth(80)

        self.label_node_RealExitOut = QtWidgets.QLabel()  # Реальный процент выхода

        # Обновляемые объекты GUI (отображение инфы о связях, на которые кликнули)
        self.label_edge_source = QtWidgets.QLabel()  # узел-источник
        self.label_edge_destination = QtWidgets.QLabel()  # узел-получатель

        self.label_edge_active = QtWidgets.QLabel()  # активность
        self.edit_edge_active = QtWidgets.QTextEdit()
        self.edit_edge_active.setFixedHeight(30)
        self.edit_edge_active.setFixedWidth(80)

        self.label_edge_MIN_transport_value = QtWidgets.QLabel()  # минимальный объём передачи связи
        self.edit_edge_MIN_transport_value = QtWidgets.QTextEdit()
        self.edit_edge_MIN_transport_value.setFixedHeight(30)
        self.edit_edge_MIN_transport_value.setFixedWidth(80)

        self.label_edge_MAX_transport_value = QtWidgets.QLabel()  # максимальный объём передачи связи
        self.edit_edge_MAX_transport_value = QtWidgets.QTextEdit()
        self.edit_edge_MAX_transport_value.setFixedHeight(30)
        self.edit_edge_MAX_transport_value.setFixedWidth(80)

        self.label_edge_real_sum_value = QtWidgets.QLabel()  # реальный объём передачи связи

        # Связываем это окно с информацией в главном окне
        self.Main_Frame = Main_Frame

        # Выводим готовую сцену визуализации
        self.GraphicsView.setScene(self.Scene)
        self.GraphicsView.show()

        # Привязываем обработчик клика левой кнопки мыши (выбор объекта)
        self.GraphicsView.mouseReleaseEvent = self.MouseLeftClick_handler
        # Привязываем обработчик прокрутки колёсика мыши
        self.GraphicsView.wheelEvent = self.MouseWheelEvent

        # Обработка нажатия кнопки "Перерасчёт"
        self.Recalculate_button.clicked.connect(self.Recalculate)

    # -------------------------------------------------------------

    #Печать картинки на дефолтном принтере
    def Print_picture(self):
        # Создаём пустую картинку размером с нашу сцену
        image = QtGui.QImage(self.Scene.width(), self.Scene.height(), QtGui.QImage.Format_ARGB32_Premultiplied)
        image.fill(QtGui.QColor(255, 255, 255))  # заливаем её белым цветом

        # Создаём рисовальщика и задаём ему флаг рендера
        painter = QtGui.QPainter(image)
        painter.setRenderHint(QtGui.QPainter.Antialiasing)

        # сцена рендерит нам картинку
        self.Scene.render(painter)

        # Сохраняем нарисованную картинку в файл
        filename = ''
        for i in range(8):
            filename += str(random.randint(0, 9))

        filename += '.png'


        #создаём временную директорию под наш файл
        dir = tempfile.TemporaryDirectory()

        #сохраняем туда картинку
        flag = image.save(tempfile.gettempdir() + filename)

        # НЕ ЗАБЫВАЕМ ОБНУЛИТЬ ПЕРЕМЕННУЮ РИСОВАЛЬЩИКА
        painter = None

        #Если картинка сохраняется норм
        if flag:
            #Отправляем сохранённую картинку на печать
            os.startfile(tempfile.gettempdir() + filename, "print")
        else:
            # Показ сообщения по итогу сохранения изображения
            msgb = QtWidgets.QMessageBox()
            msgb.setWindowTitle('Печать')
            msgb.setDefaultButton(QtWidgets.QMessageBox.Ok)
            msgb.setIcon(QtWidgets.QMessageBox.Warning)
            msgb.setText('Не удаётся осуществить печать изображения.')

            msgb.show()
            self.MSGB = msgb

    #--------------------------------------------------------------

    #Сохранение картинки в файл
    def Save_Picture(self):
        #Вызываем окно для выбора пути и имени файла-картинки для сохранения
        SaveFileDialog = QtWidgets.QFileDialog.getSaveFileName()

        #Создаём пустую картинку размером с нашу сцену
        image = QtGui.QImage(self.Scene.width(), self.Scene.height(), QtGui.QImage.Format_ARGB32_Premultiplied)
        image.fill(QtGui.QColor(255, 255, 255))  #заливаем её белым цветом

        #Создаём рисовальщика и задаём ему флаг рендера
        painter = QtGui.QPainter(image)
        painter.setRenderHint(QtGui.QPainter.Antialiasing)

        #сцена рендерит нам картинку
        self.Scene.render(painter)

        #Сохраняем нарисованную картинку в файл
        flag = image.save(SaveFileDialog[0])

        #НЕ ЗАБЫВАЕМ ОБНУЛИТЬ ПЕРЕМЕННУЮ РИСОВАЛЬЩИКА
        painter = None

        #Показ сообщения по итогу сохранения изображения
        msgb = QtWidgets.QMessageBox()
        msgb.setWindowTitle('Сохранение')
        msgb.setDefaultButton(QtWidgets.QMessageBox.Ok)

        if flag:
            msgb.setIcon(QtWidgets.QMessageBox.Information)
            msgb.setText('Сохранено успешно!')
        else:
            msgb.setIcon(QtWidgets.QMessageBox.Warning)
            msgb.setText('Не удалось сохранить изображение.\nПожалуйста, проверьте, правильно ли указано расширение сохраняемого файла.')

        msgb.show()
        self.MSGB = msgb

    #--------------------------------------------------------------

    def Recalculate(self):

        for ED in self.Main_Frame.Edges_list:
            # Переводим ссылку на узлы в имена узлов для избежания ошибки при пересчёте
            ED.source = ED.source.name
            ED.destination = ED.destination.name

        self.Main_Frame.Calculate()
        self.close()

    # -------------------------------------------------

    # Обработчик клика левой кнопки мыши (выбор объекта)
    def MouseLeftClick_handler(self, e):
        pos = e.pos()  # точка клика мыши
        flag = 0  # флаг нахождения объекта в точке

        # Идём по списку всех объектов в точке
        for item in self.GraphicsView.items(pos):
            # Проверяем, является ли объект в точке узлом
            for node in self.Nodes_visual.keys():
                # Если объект является узлом
                if self.Nodes_visual[node] == item:

                    self.clicked_object_model = node  # Запоминаем кликнутый объект модели

                    self.prev_clicked_node_visual.setBrush(
                        QtGui.QBrush(QtGui.QColor(0, 0, 255, 127)))  # Возвращаем исходный цвет предыдущему узлу
                    self.clicked_object_visual = item  # Запоминаем кликнутый объект картинки
                    self.prev_clicked_node_visual = item  # Он же и будет прошлым при следующем клике
                    self.clicked_object_visual.setBrush(
                        QtGui.QBrush(QtGui.QColor(255, 255, 0, 127)))  # Даём ему цветовое выделение
                    self.update()

                    # Очищаем боковую панель от всех объектов
                    while self.ParametersVerticalLayout.count():
                        self.ParametersVerticalLayout.itemAt(0).widget().setParent(None)

                    # Выводим данные узла в очищенную боковую панель
                    self.label_node_name.setText('Узел:\n' + node.name)
                    self.ParametersVerticalLayout.addWidget(self.label_node_name)

                    self.label_node_code.setText('Код узла:')
                    self.edit_node_code.setText(str(int(node.code)))
                    self.ParametersVerticalLayout.addWidget(self.label_node_code)
                    self.ParametersVerticalLayout.addWidget(self.edit_node_code)

                    self.label_node_StartValue.setText('Начальное значение:')
                    self.edit_node_Start_value.setText(str(node.start_value))
                    self.ParametersVerticalLayout.addWidget(self.label_node_StartValue)
                    self.ParametersVerticalLayout.addWidget(self.edit_node_Start_value)

                    self.label_node_EndValue.setText('Конечное значение:')
                    self.edit_node_EndValue.setText(str(node.end_value))
                    self.ParametersVerticalLayout.addWidget(self.label_node_EndValue)
                    self.ParametersVerticalLayout.addWidget(self.edit_node_EndValue)

                    self.label_node_IN_turnover.setText('Входящий оборот:\n' + str(node.IN_turnover_value))
                    self.label_node_OUT_turnover.setText('Исходящий оборот:\n' + str(node.OUT_turnover_value))
                    self.ParametersVerticalLayout.addWidget(self.label_node_IN_turnover)
                    self.ParametersVerticalLayout.addWidget(self.label_node_OUT_turnover)

                    self.label_node_IN_edges_min.setText('Минимум входящих\nсвязей:')
                    self.edit_node_IN_edges_min.setText(str(node.IN_edges_min))
                    self.ParametersVerticalLayout.addWidget(self.label_node_IN_edges_min)
                    self.ParametersVerticalLayout.addWidget(self.edit_node_IN_edges_min)

                    self.label_node_IN_edges_real.setText('Входящих связей\nсейчас:\n' + str(node.IN_edges_real))
                    self.ParametersVerticalLayout.addWidget(self.label_node_IN_edges_real)

                    self.label_node_IN_edges_max.setText('Максимум входящих\nсвязей:')
                    self.edit_node_IN_edges_max.setText(str(node.IN_edges_max))
                    self.ParametersVerticalLayout.addWidget(self.label_node_IN_edges_max)
                    self.ParametersVerticalLayout.addWidget(self.edit_node_IN_edges_max)

                    self.label_node_OUT_edges_min.setText('Минимум исходящих\nсвязей:')
                    self.edit_node_OUT_edges_min.setText(str(node.OUT_edges_min))
                    self.ParametersVerticalLayout.addWidget(self.label_node_OUT_edges_min)
                    self.ParametersVerticalLayout.addWidget(self.edit_node_OUT_edges_min)

                    self.label_node_OUT_edges_real.setText('Исходящих связей\nсейчас:\n' + str(node.OUT_edges_real))
                    self.ParametersVerticalLayout.addWidget(self.label_node_OUT_edges_real)

                    self.label_node_OUT_edges_max.setText('Максимум исходящих\nсвязей:')
                    self.edit_node_OUT_edges_max.setText(str(node.OUT_edges_max))
                    self.ParametersVerticalLayout.addWidget(self.label_node_OUT_edges_max)
                    self.ParametersVerticalLayout.addWidget(self.edit_node_OUT_edges_max)

                    self.label_node_MaxExitOut.setText('Максимальный процент\nвыхода:')
                    self.edit_node_MaxExitOut.setText(str(node.Exit_out_edges_max_beg))
                    self.ParametersVerticalLayout.addWidget(self.label_node_MaxExitOut)
                    self.ParametersVerticalLayout.addWidget(self.edit_node_MaxExitOut)

                    self.label_node_RealExitOut.setText('Реальный процент\nвыхода:\n' + str(node.Exit_out_edges_real))
                    self.ParametersVerticalLayout.addWidget(self.label_node_RealExitOut)

                    self.ParametersVerticalLayout.addWidget(self.save_button)

                    self.object_flag = 0  # отмечаем, что последний отображённый объект - это узел

                    flag = 1  # Отмечаем, что нашли узел
                    break  # и заканчиваем поиск

            # Если узла в точке не было
            if flag == 0:
                # Попробуем найти связь
                for edge in self.Edges_visual.keys():
                    # Если в точке найдена связь
                    if self.Edges_visual[edge] == item:

                        # Очищаем боковую панель от всех объектов
                        while self.ParametersVerticalLayout.count():
                            self.ParametersVerticalLayout.itemAt(0).widget().setParent(None)

                        # Ищем логическую связь СПИСКЕ ИЗНАЧАЛЬНЫХ СВЯЗЕЙ, которая соответствует нарисованной
                        for ED in self.Main_Frame.Edges_list:
                            if (ED.source == edge[0] and ED.destination == edge[1]):
                                self.prev_clicked_node_visual.setBrush(QtGui.QBrush(QtGui.QColor(0, 0, 255, 127)))
                                self.clicked_object_model = ED
                                self.clicked_object_visual = item
                                break

                        # Ищем логическую связь В РЕШЕНИИ, которая соответствует нарисованной
                        for ED in self.Main_Frame.old_Result_Dict[edge[0]]:
                            if (ED.source == edge[0] and ED.destination == edge[1]):
                                self.prev_clicked_node_visual.setBrush(QtGui.QBrush(QtGui.QColor(0, 0, 255, 127)))
                                self.clicked_object_model = ED
                                self.clicked_object_visual = item
                                break

                        # Выводим данные связи в очищеную боковую панель
                        self.label_edge_source.setText('Узел-отправитель:\n' + self.clicked_object_model.source.name)
                        self.ParametersVerticalLayout.addWidget(self.label_edge_source)

                        self.label_edge_destination.setText(
                            'Узел-получатель:\n' + self.clicked_object_model.destination.name)
                        self.ParametersVerticalLayout.addWidget(self.label_edge_destination)

                        self.label_edge_active.setText('Активность:')
                        self.edit_edge_active.setText(str(self.clicked_object_model.active))
                        self.ParametersVerticalLayout.addWidget(self.label_edge_active)
                        self.ParametersVerticalLayout.addWidget(self.edit_edge_active)

                        self.label_edge_MIN_transport_value.setText('Минимальный объём\nпередачи:')
                        self.edit_edge_MIN_transport_value.setText(str(self.clicked_object_model.MIN_transport_value))
                        self.ParametersVerticalLayout.addWidget(self.label_edge_MIN_transport_value)
                        self.ParametersVerticalLayout.addWidget(self.edit_edge_MIN_transport_value)

                        self.label_edge_MAX_transport_value.setText('Максимальный объём\nпередачи:')
                        self.edit_edge_MAX_transport_value.setText(str(self.clicked_object_model.MAX_transport_value))
                        self.ParametersVerticalLayout.addWidget(self.label_edge_MAX_transport_value)
                        self.ParametersVerticalLayout.addWidget(self.edit_edge_MAX_transport_value)

                        self.label_edge_real_sum_value.setText(
                            'Реальный объём\nпередачи:\n' + str(self.clicked_object_model.real_sum_value))
                        self.ParametersVerticalLayout.addWidget(self.label_edge_real_sum_value)

                        self.ParametersVerticalLayout.addWidget(self.save_button)

                        self.object_flag = 1  # отмечаем, что последний отображённый объект - это связь

                        flag = 1  # Отмечаем нахождение связи в точке
                        break  # и прекращаем поиск

            # Если по итогу поиска связь была найдена
            if flag == 1:
                break  # Окончательно прекращаем поиск

    # ----------------------------------------------------------

    # Увеличение и уменьшение масштаба
    def MouseWheelEvent(self, e):
        zoomInFactor = 1.25  # Коэффициент приближения
        zoomOutFactor = 0.8  # Коэффициент отдаления

        # Zoom
        if e.angleDelta().y() > 0:  # Если колёсо мыши прокрутилось вперёд
            zoomFactor = zoomInFactor  # приближение
        else:
            zoomFactor = zoomOutFactor  # иначе - отдаление

        # Выполняем
        self.GraphicsView.scale(zoomFactor, zoomFactor)

    # ----------------------------------------------------------

    # Сохранение изменённых параметров узла изи связи
    def Save_object(self):
        print('Сохранено: ', self.clicked_object_model)

        # Сохранение изменений узла
        if self.object_flag == 0:
            self.clicked_object_model.code = float(self.edit_node_code.toPlainText())  # Код узла
            self.clicked_object_model.start_value = float(
                self.edit_node_Start_value.toPlainText())  # Начальное количество ресурса
            self.clicked_object_model.end_value = float(
                self.edit_node_EndValue.toPlainText())  # Конечное количество ресурса
            self.clicked_object_model.IN_edges_min = float(
                self.edit_node_IN_edges_min.toPlainText())  # Минимальное количество входящих связей узла
            self.clicked_object_model.IN_edges_max = float(
                self.edit_node_IN_edges_max.toPlainText())  # Максимальное количество входящих связей узла
            self.clicked_object_model.OUT_edges_min = float(
                self.edit_node_OUT_edges_min.toPlainText())  # Минимальное количество исходящих связей узла
            self.clicked_object_model.OUT_edges_max = float(
                self.edit_node_OUT_edges_max.toPlainText())  # Максимальное количество исходящих связей узла
            self.clicked_object_model.Exit_out_edges_max_beg = float(
                self.edit_node_MaxExitOut.toPlainText())  # макс. процент выхода

            # Меняем надпись узла согласно изменениям
            name = self.clicked_object_model.name
            start = str(int(self.clicked_object_model.start_value))
            end = str(int(self.clicked_object_model.end_value))
            pos = self.clicked_object_visual.rect().center()
            pos = self.GraphicsView.mapFromScene(pos)
            items = self.GraphicsView.items(pos)
            items[0].setPlainText('' + name + '\n' + start + '\n' + end)


        # Сохранение изменений связи
        elif self.object_flag == 1:
            self.clicked_object_model.active = int(self.edit_edge_active.toPlainText())  # Показатель эффективности
            self.clicked_object_model.MIN_transport_value = float(
                self.edit_edge_MIN_transport_value.toPlainText())  # мин. объём передачи
            self.clicked_object_model.MAX_transport_value = float(
                self.edit_edge_MAX_transport_value.toPlainText())  # макс. объём передачи

            # Если связь стала обязательным к использованию и её нет в списке изначальных связей
            if (self.clicked_object_model.active == 1 or self.clicked_object_model.MIN_transport_value > 0):
                self.clicked_object_model.active = 1
                self.edit_edge_active.setText('1')

                GreenPen = QtGui.QPen(QtGui.QColor(0, 255, 0), 2, QtCore.Qt.SolidLine, QtCore.Qt.RoundCap,
                                      QtCore.Qt.RoundJoin)
                self.clicked_object_visual.setPen(GreenPen)
                self.update()

                # Добавляем изменённую связь
                self.Main_Frame.Edges_list.append(copy.copy(self.clicked_object_model))

                # Посчитаем количество одинаковых связей в списке изначальных связей
                edges_count = 0
                for ED in self.Main_Frame.Edges_list:
                    if (
                            ED.source == self.clicked_object_model.source and ED.destination == self.clicked_object_model.destination):
                        edges_count += 1

                if edges_count > 1:
                    # Удаляем копии добавляемой связи
                    for ED in self.Main_Frame.Edges_list:
                        if (
                                ED.source == self.clicked_object_model.source and ED.destination == self.clicked_object_model.destination):
                            self.Main_Frame.Edges_list.remove(ED)

            # Если связь стала запрещённой к использованию и её нет в списке изначальных связей
            if (self.clicked_object_model.MAX_transport_value <= 0):
                self.clicked_object_model.active = 0
                self.edit_edge_active.setText('0')

                # Перекрашиваем картинку
                RedPen = QtGui.QPen(QtGui.QColor(255, 0, 0), 2, QtCore.Qt.SolidLine, QtCore.Qt.RoundCap,
                                    QtCore.Qt.RoundJoin)
                self.clicked_object_visual.setPen(RedPen)
                self.update()

                # Добавляем изменённую связь
                self.Main_Frame.Edges_list.append(copy.copy(self.clicked_object_model))

                # Посчитаем количество одинаковых связей в списке изначальных связей
                edges_count = 0
                for ED in self.Main_Frame.Edges_list:
                    if (
                            ED.source == self.clicked_object_model.source and ED.destination == self.clicked_object_model.destination):
                        edges_count += 1

                if edges_count > 1:
                    # Удаляем копии добавляемой связи
                    for ED in self.Main_Frame.Edges_list:
                        if (
                                ED.source == self.clicked_object_model.source and ED.destination == self.clicked_object_model.destination):
                            self.Main_Frame.Edges_list.remove(ED)

            # Если связь стала дефолтной и она есть в списке изначальных связей
            if (self.clicked_object_model.active == 0 and self.clicked_object_model.MIN_transport_value == 0
                    and self.clicked_object_model.MAX_transport_value > 0):

                # Добавляем изменённую связь
                self.Main_Frame.Edges_list.append(copy.copy(self.clicked_object_model))

                # Посчитаем количество одинаковых связей в списке изначальных связей
                edges_count = 0
                for ED in self.Main_Frame.Edges_list:
                    if (
                            ED.source == self.clicked_object_model.source and ED.destination == self.clicked_object_model.destination):
                        edges_count += 1

                if edges_count > 1:
                    # Удаляем копии добавляемой связи
                    for ED in self.Main_Frame.Edges_list:
                        if (
                                ED.source == self.clicked_object_model.source and ED.destination == self.clicked_object_model.destination):
                            self.Main_Frame.Edges_list.remove(ED)

                # Перекрашиваем картинку
                Pen = QtGui.QPen(QtGui.QColor(0, 0, 0), 2, QtCore.Qt.SolidLine, QtCore.Qt.RoundCap, QtCore.Qt.RoundJoin)
                self.clicked_object_visual.setPen(Pen)
                self.update()

                # Если связь полностью соответствует характеристикам дефолтной
                if self.clicked_object_model.MAX_transport_value == 10000000:
                    # Удаляем эту связь из списка изначальных связей
                    for ED in self.Main_Frame.Edges_list:
                        if (
                                ED.source == self.clicked_object_model.source and ED.destination == self.clicked_object_model.destination):
                            self.Main_Frame.Edges_list.remove(ED)

        # Из-за сделанных изменений нельзя сохранять результат, так как необходимо произвести пересчёт
        self.Main_Frame.Ban_to_export()

    # ----------------------------------------------------------
