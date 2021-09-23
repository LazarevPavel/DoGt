import threading
import time


class Loading_animate(threading.Thread):
    def __init__(self, Main_Frame, calc_thread, name):
        super().__init__()
        self.Main_Frame = Main_Frame
        self.calc_thread = calc_thread
        self.name = name
        self.stop_flag = False
        self.setDaemon(daemonic=True)

    def run(self):
        # Индикатор генерации решения
        while(self.calc_thread.is_alive() and self.stop_flag == False):
            if (self.Main_Frame.string_loading == 'Генерирую решение'):
                self.Main_Frame.string_loading = 'Генерирую решение.'
            elif (self.Main_Frame.string_loading == 'Генерирую решение.'):
                self.Main_Frame.string_loading = 'Генерирую решение..'
            elif (self.Main_Frame.string_loading == 'Генерирую решение..'):
                self.Main_Frame.string_loading = 'Генерирую решение...'
            elif (self.Main_Frame.string_loading == 'Генерирую решение...'):
                self.Main_Frame.string_loading = 'Генерирую решение'

            self.Main_Frame.Finish_label.setText(self.Main_Frame.string_loading)
            time.sleep(0.3)

        if(self.stop_flag == True):
            self.Main_Frame.Finish_label.setText('Генерация решения была остановлена')
            self.stop_flag = False

#---------------------------------------------