from PyQt5 import QtCore, QtGui, QtWidgets
import serial

import braille_gui

global arduino

class Arduino():
    def __init__(self, ui):
        self.arduino_conn = None
        self.connection_established = False
        self.actuators = [0,0,0,0,0,0,0,0,0]
        self.cell_chars = ['x','x','x','x','x','x','x','x','x','x','x','x','x','x','x','x','x','x','x','x']

    def connect_to_arduino(self, com_port):
        if not self.connection_established:
            try:
                #print('COM' + com_port)
                self.arduino_conn = serial.Serial('COM' + com_port, 9600) #, timeout=0.05)
                self.connection_established = True
            except:
                #print('can\'t connect')
                self.connection_established = False
        else:
            self.connection_established = False
            self.arduino_conn.close()

    def send_data(self, data):
        print('The data to be sent: ' + data)
        self.arduino_conn.write(bytes(data, 'UTF-8'))

    def read_data(self):
        #TODO: Change the condition here!!
        if self.connection_established:
            data_read = self.arduino_conn.readline()
            data_str = data_read.decode('ascii')
            self.process_data(data_str)
            return True
        else:
            return False


    def process_data(self, data_str):
        try:
            if data_str.startswith("act"):
                data_str = data_str.split(':')[1]
                #print(data_str)
                for i in range(9):
                    self.actuators[i] = data_str[i*2]
                    #print("Actuators: " + self.actuators[i])
            elif data_str.startswith("char"):
                data_str = data_str.split(':')[1]
                #print(data_str)
                for i in range(20):
                    self.cell_chars[i] = data_str[i*2]
                    #print("chars: " + self.cell_chars[i])
            else:
                print('x:' + data_str)
        except:
            print('Error could have happened here')


if __name__ == "__main__":
    import sys
    app = QtWidgets.QApplication(sys.argv)
    MainWindow = QtWidgets.QMainWindow()
    ui = braille_gui.Ui_MainWindow()
    x = ui.setupUi(MainWindow)
    s = MainWindow.show()
    sys.exit(app.exec_())