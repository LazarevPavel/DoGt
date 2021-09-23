from PyQt5 import QtWidgets, QtCore, QtGui


#Построение сцены для отрисовки и связывание объектов сцены с логическими объектами модели
def Build_graphics_scene(positions, Result_Dict, Edges_list):

    # Создаём сцену, на которой будем выстраивать логику визуализации
    scene = QtWidgets.QGraphicsScene()

    #Создаём рисующее перо чёрного цвета
    Pen = QtGui.QPen(QtGui.QColor(0,0,0), 3, QtCore.Qt.SolidLine, QtCore.Qt.RoundCap, QtCore.Qt.RoundJoin)
    RedPen = QtGui.QPen(QtGui.QColor(255,0,0), 3, QtCore.Qt.SolidLine, QtCore.Qt.RoundCap, QtCore.Qt.RoundJoin)
    GreenPen = QtGui.QPen(QtGui.QColor(0,255,0), 3, QtCore.Qt.SolidLine, QtCore.Qt.RoundCap, QtCore.Qt.RoundJoin)

    #Создаём закрашивающую кисть синевого цвета
    Brush = QtGui.QBrush(QtGui.QColor(0,0,255,127))

    #-----------------------------------------

    #Рисуем узлы по координатам
    Nodes_visual = {}
    for node in positions.keys():
        x = positions[node][0]    #Берём координаты
        y = positions[node][1]

        Rect = QtCore.QRectF(x, y, 100, 100)              #Создаём логический шаблон узла
        visual_obj = scene.addEllipse(Rect, Pen, Brush) #Рисуем узел по шаблону
        Nodes_visual.update( {node: visual_obj} )       #Связываем нарисованный узел с логическим узлом

    #-----------------------------------------

    #Рисуем надписи на узлах
    Nodes_labels_visual = {}
    for node in positions.keys():
        Label = QtWidgets.QGraphicsTextItem()
        Label.setPlainText('' + node.name + '\n' + str(node.start_value) + '\n' + str(node.end_value))
        X = Nodes_visual[node].rect().x() + 15
        Y = Nodes_visual[node].rect().y() + 10
        Label.setX(X)
        Label.setY(Y)
        Label.setScale(1.5)

        scene.addItem(Label)

    #-----------------------------------------

    #Рисуем связи по модели
    Edges_visual = {}
    for node in Result_Dict.keys():
        for ED in Result_Dict[node]:
            #Если связь в модели была построена и она ещё не была нарисована
            if len(ED.transport_value) != 0 and (ED.source, ED.destination) not in Edges_visual:

                print(ED.source.name, ED.destination.name, ED.transport_value)

                #Берём центральные координаты двух связанных узлов
                Point_source = Nodes_visual[ED.source].rect().center()
                Point_destination = Nodes_visual[ED.destination].rect().center()

                #Формируем линию и подстраиваем её под рисунок
                Line = QtCore.QLineF(Point_source, Point_destination)   #Создаём линию между узлами, линии ведут к центрам узлов
                Line.setLength(Line.length()-50)                        #уменьшаем длину линии, чтобы она не заходила внутрь узла на картинке
                point_old = (Line.x2(), Line.y2())                      #запоминаем точку соприкосновения линии и узла
                Line.setLength(Line.length() - 50)                      #Ещё раз уменьшаем длину линии, чтобы начало линии тоже не заходило внутр узла на канртинке
                point_new = (Line.x2(), Line.y2())                      #запоминаем новую конечную точку линии (теперь она не соприкасается с узлом)
                dx = point_old[0] - point_new[0]                        #считаем расстояние по оси Х до точки соприкосновения
                dy = point_old[1] - point_new[1]                        #считаем расстояние по оси Y до точки соприкосновения
                Line.translate(dx, dy)                                  #переносим линию параллельно на данное расстояние


                #Рисуем стрелку на связи
                normal_vector = Line.normalVector()  #Находим нормаль к нашей связи
                point_old = (normal_vector.x1(), normal_vector.y1())  #берём начало вектора-нормали
                middle_point = Line.pointAt(0.95)                     #берём точку на линии связи, до которой растянутся плечи стрелки
                point_new = (middle_point.x(), middle_point.y())      # берём координаты этой точки
                dx = point_new[0] - point_old[0]                      # считаем смещение по х
                dy = point_new[1] - point_old[1]                      # считаем смещение по y
                normal_vector.translate(dx, dy)                       # перемещаем нормаль по высчитанному смещению
                normal_vector.setLength(20)                           # уменьшаем длину нормали до 20 единиц

                Arrow_line_left = QtCore.QLineF(normal_vector.p2(), Line.p2())  #рисуем левое плечо стрелки
                dx = normal_vector.dx()    #катет нормали (длина проекции по х)
                dy = normal_vector.dy()    #катет нормали (длина проекции по y)
                normal_vector.translate(-dx, -dy)  #смещаем нормаль на противопложную сторону
                Arrow_line_right = QtCore.QLineF(normal_vector.p1(), Line.p2())   #рисуем правое плечо стрелки


                scene.addLine(Arrow_line_left, Pen)   #добавляем плечи стрелки
                scene.addLine(Arrow_line_right, Pen)


                #Рисуем линию и связываем её с логической связью в модели
                if ED.active == 0 and ED.MIN_transport_value == 0 and ED.MAX_transport_value > 0:
                    Edge_vis = scene.addLine(Line, Pen)
                    Edges_visual.update( {(ED.source, ED.destination): Edge_vis} )
                elif ED.active == 1 or ED.MIN_transport_value > 0:
                    Edge_vis = scene.addLine(Line, GreenPen)
                    Edges_visual.update({(ED.source, ED.destination): Edge_vis})


    #Построим запрещённые связи
    for ED in Edges_list:
        # Если связь в модели запрещена и она ещё не была нарисована
        if ED.MAX_transport_value <= 0 and (ED.source, ED.destination) not in Edges_visual:
            # Берём центральные координаты двух связанных узлов
            Point_source = Nodes_visual[ED.source].rect().center()
            Point_destination = Nodes_visual[ED.destination].rect().center()

            # Формируем линию и подстраиваем её под рисунок
            Line = QtCore.QLineF(Point_source, Point_destination)  # Создаём линию между узлами, линии ведут к центрам узлов
            Line.setLength(Line.length() - 50)  # уменьшаем длину линии, чтобы она не заходила внутрь узла на картинке
            point_old = (Line.x2(), Line.y2())  # запоминаем точку соприкосновения линии и узла
            Line.setLength(Line.length() - 50)  # Ещё раз уменьшаем длину линии, чтобы начало линии тоже не заходило внутр узла на канртинке
            point_new = (Line.x2(), Line.y2())  # запоминаем новую конечную точку линии (теперь она не соприкасается с узлом)
            dx = point_old[0] - point_new[0]  # считаем расстояние по оси Х до точки соприкосновения
            dy = point_old[1] - point_new[1]  # считаем расстояние по оси Y до точки соприкосновения
            Line.translate(dx, dy)  # переносим линию параллельно на данное расстояние

            # Рисуем стрелку на связи
            normal_vector = Line.normalVector()  # Находим нормаль к нашей связи
            point_old = (normal_vector.x1(), normal_vector.y1())  # берём начало вектора-нормали
            middle_point = Line.pointAt(0.95)  # берём точку на линии связи, до которой растянутся плечи стрелки
            point_new = (middle_point.x(), middle_point.y())  # берём координаты этой точки
            dx = point_new[0] - point_old[0]  # считаем смещение по х
            dy = point_new[1] - point_old[1]  # считаем смещение по y
            normal_vector.translate(dx, dy)  # перемещаем нормаль по высчитанному смещению
            normal_vector.setLength(20)  # уменьшаем длину нормали до 20 единиц

            Arrow_line_left = QtCore.QLineF(normal_vector.p2(), Line.p2())  # рисуем левое плечо стрелки
            dx = normal_vector.dx()  # катет нормали (длина проекции по х)
            dy = normal_vector.dy()  # катет нормали (длина проекции по y)
            normal_vector.translate(-dx, -dy)  # смещаем нормаль на противопложную сторону
            Arrow_line_right = QtCore.QLineF(normal_vector.p1(), Line.p2())  # рисуем правое плечо стрелки

            scene.addLine(Arrow_line_left, Pen)  # добавляем плечи стрелки
            scene.addLine(Arrow_line_right, Pen)

            # Рисуем линию и связываем её с логической связью в модели
            Edge_vis = scene.addLine(Line, RedPen)
            Edges_visual.update({(ED.source, ED.destination): Edge_vis})



    return scene, Nodes_visual, Nodes_labels_visual, Edges_visual