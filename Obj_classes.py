import random
#------------------------------------------------------------------------

class Node:
    """Класс узла"""

    def __init__(self, name, date, code, active, start_value, end_value, IN_edges_min, IN_edges_max, OUT_edges_min, OUT_edges_max, class_numbers, Exit_out_edges_max_beg, Exit_out_edges_allowed_difference = 0):
        """Конструктор"""
        self.name = name                     #Название узла
        self.code = code                     #Код узла
        self.date = date
        self.active = active                 #Используется ли узел
        self.start_value = start_value       #Начальное количество ресурса
        self.IN_turnover_value = 0           #Входящий оборот
        self.real_value = start_value        #Количество ресурса в настоящий момент
        self.OUT_turnover_value = 0          #Исходящий оборот
        self.end_value = end_value           #Конечное количество ресурса
        self.IN_edges_min = IN_edges_min     #Минимальное количество входящих связей узла
        self.IN_edges_real = 0               #Количество входящих связей узла в настоящий момент
        self.IN_edges_max = IN_edges_max     #Максимальное количество входящих связей узла
        self.OUT_edges_min = OUT_edges_min   #Минимальное количество исходящих связей узла
        self.OUT_edges_real = 0              #Количество исходящих связей узла в настоящий момент
        self.OUT_edges_max = OUT_edges_max   #Максимальное количество исходящих связей узла
        self.class_numbers = class_numbers   #Номера классов узла
        self.Exit_out_edges_max_beg = Exit_out_edges_max_beg
        self.Exit_out_edges_max = random.uniform(self.Exit_out_edges_max_beg - self.Exit_out_edges_max_beg/2, self.Exit_out_edges_max_beg)    #Exit_out_edges_max  #максиамльный процент выхода от входящего оборота
        self.Exit_out_edges_real = 0                  #Процент выхода от исходящего оборота на данный момент
        self.Exit_out_edges_allowed_difference = Exit_out_edges_allowed_difference
        self.type = 0                        #Тип узла по надобности в ресурсах
        self.Allowed_connections = []        #Список узлов, с которыми данный узел может иметь связи
        self.Connections_IN = []             #Список узлов, которые отдают ресурсы В данный узел
        self.Connections_OUT = []            #Список узлов, которые принимают ресурсы ИЗ данного узла
        self.allowed_difference_endvalue = 0.01

    
    def Clear_params(self):
        self.IN_turnover_value = 0  # Входящий оборот
        self.real_value = self.start_value  # Количество ресурса в настоящий момент
        self.OUT_turnover_value = 0  # Исходящий оборот
        self.IN_edges_real = 0  # Количество входящих связей узла в настоящий момент
        self.OUT_edges_real = 0  # Количество исходящих связей узла в настоящий момент
        self.Exit_out_edges_max = self.Exit_out_edges_max_beg
        self.Exit_out_edges_real = 0  # Процент выхода от входящего оборота на данный момент
        self.type = 0  # Тип узла по надобности в ресурсах
        self.Allowed_connections = []  # Список узлов, с которыми данный узел может иметь связи
        self.Connections_IN = []  # Список узлов, которые отдают ресурсы В данный узел
        self.Connections_OUT = []  # Список узлов, которые принимают ресурсы ИЗ данного узла


    pass

#-------------------------------------------------------------------

class Edge:
    """Класс связи"""

    def __init__(self, source, destination, transport_value = 0, active = 0, MIN_transport_value = 0, MAX_transport_value = 10000000):
        """Конструктор"""
        self.source = source  #Отправитель
        self.destination = destination    #Получатель

        if transport_value == 0:
            self.transport_value = []   #Если связь просто создана, то список пересылок пуст
        else:
            self.transport_value = [].append([transport_value]) #Если что-то отправляют, то сразу записываем эту пересылку

        self.active = active
        self.MIN_transport_value = MIN_transport_value
        self.MAX_transport_value = MAX_transport_value

        self.real_sum_value = 0


    def Clear_params(self):
        self.transport_value = []
        self.real_sum_value = 0

    pass

#-------------------------------------------------------------------