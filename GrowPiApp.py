#!/usr/bin/python3
import sys
import os
import numpy
import sqlite3
import pyqtgraph
import pg_time_axis
from PyQt5 import QtWidgets, QtCore, QtGui

from GrowPiAppUi import Ui_MainWindow


# Convert .ui to .py in Terminal
# python -m PyQt5.uic.pyuic -x [FILENAME].ui -o [FILENAME].py


class Ui(QtWidgets.QMainWindow):
    def __init__(self):
        super(Ui, self).__init__(parent=None)
        self.ui = Ui_MainWindow()
        self.ui.setupUi(self)

        ####################################
        # Exit tab                         #
        ####################################
        # Connect pushbutton action
        self.ui.pbExit.clicked.connect(self.exit)
        self.ui.pbReboot.clicked.connect(self.reboot)
        self.ui.pbShutdown.clicked.connect(self.shutdown)

        ####################################
        # Temp Data tab                    #
        ####################################
        # Initialise Plotwidget
        self.win = self.ui.plotWidget
        self.plt0 = self.win.addPlot()

        # Enable antialiasing for prettier plots
        # pyqtgraph.setConfigOptions(antialias=True)

        # Initialise data arrays
        self.data_tst = []
        self.data_temp_1 = []
        self.data_av_temp_1 = []
        self.data_temp_2 = []
        self.data_av_temp_2 = []
        self.data_temp_3 = []
        self.data_av_temp_3 = []
        self.data_temp_4 = []
        self.data_av_temp_4 = []
        self.data_temp_5 = []
        self.data_av_temp_5 = []

        # Initialise sqlite
        con = sqlite3.connect('data.db')
        cur = con.cursor()

        # Create table
        cur.execute('''CREATE TABLE IF NOT EXISTS temperature
                     (timestamp real, temperature1 real, temperature2 real, 
                     temperature3 real, temperature4 real, temperature5 real)''')

        # Select all data ordered and append lists
        cur.execute(
            "SELECT * FROM temperature ORDER BY timestamp DESC LIMIT 1440")
        self.data = cur.fetchall()
        for row in self.data:
            self.data_tst.append(row[0])
            self.data_temp_1.append(row[1])
            self.data_temp_2.append(row[2])
            self.data_temp_3.append(row[3])
            self.data_temp_4.append(row[4])
            self.data_temp_5.append(row[5])

        # Average value
        self.average_1 = sum(self.data_temp_1) / float(len(self.data_temp_1))
        for i in self.data_temp_1:
            self.data_av_temp_1.append(self.average_1)
        self.average_2 = sum(self.data_temp_2) / float(len(self.data_temp_2))
        for i in self.data_temp_2:
            self.data_av_temp_2.append(self.average_2)
        self.average_3 = sum(self.data_temp_3) / float(len(self.data_temp_3))
        for i in self.data_temp_3:
            self.data_av_temp_3.append(self.average_3)
        self.average_4 = sum(self.data_temp_4) / float(len(self.data_temp_4))
        for i in self.data_temp_4:
            self.data_av_temp_4.append(self.average_4)
        self.average_5 = sum(self.data_temp_5) / float(len(self.data_temp_5))
        for i in self.data_temp_5:
            self.data_av_temp_5.append(self.average_5)

        # Add the Date-time axis
        # self.axis = pg_time_axis.DateAxisItem(orientation='bottom')
        # self.axis.attachToPlotItem(self.win.getItem(0,0))

        # Set tick font
        font = QtGui.QFont()
        font.setPixelSize(18)
        self.plt0.getAxis("bottom").tickFont = font
        # self.plt0.getAxis("bottom").setStyle(tickTextOffset=18)
        self.plt0.getAxis("left").tickFont = font
        # self.plt0.getAxis("left").setStyle(tickTextOffset=18)

        # Add Legend
        self.plt0.addLegend()
        # l = pyqtgraph.LegendItem((10, 10), offset=(0, 0))  # args are (size, offset)
        # l.setParentItem(self.plt0.graphicsItem())   # Note we do NOT call plt.addItem in this case

        # Plot data
        # self.curve0 = self.plt0.plot(x=self.data_tst, y=self.data_temp_1,
        #                            pen="r", name="Top °C")
        # self.curve1 = self.plt0.plot(x=self.data_tst, y=self.data_av_temp_1,
        #                            pen="r", style=QtCore.Qt.DotLine)
        # self.curve2 = self.plt0.plot(x=self.data_tst, y=self.data_temp_2,
        #                            pen="y", name="Middle °C")
        # self.curve3 = self.plt0.plot(x=self.data_tst, y=self.data_av_temp_2,
        #                            pen="y", style=QtCore.Qt.DotLine)
        # self.curve4 = self.plt0.plot(x=self.data_tst, y=self.data_temp_3,
        #                            pen="g", name="Bottom °C")
        # self.curve5 = self.plt0.plot(x=self.data_tst, y=self.data_av_temp_3,
        #                            pen="g", style=QtCore.Qt.DotLine)
        # self.curve6 = self.plt0.plot(x=self.data_tst, y=self.data_temp_4,
        #                            pen="b", name="Water °C")
        # self.curve7 = self.plt0.plot(x=self.data_tst, y=self.data_av_temp_4,
        #                            pen="b", style=QtCore.Qt.DotLine)
        # self.curve8 = self.plt0.plot(x=self.data_tst, y=self.data_temp_5,
        #                            pen="m", name="Room °C")
        # self.curve9 = self.plt0.plot(x=self.data_tst, y=self.data_av_temp_5,
        #                            pen="m", style=QtCore.Qt.DotLine)

        # Plot data
        self.curve0 = self.plt0.plot(y=self.data_temp_1, pen="r", name="Top °C")
        self.curve1 = self.plt0.plot(y=self.data_av_temp_1, pen="r",
                                     style=QtCore.Qt.DotLine)
        self.curve2 = self.plt0.plot(y=self.data_temp_2, pen="y",
                                     name="Middle °C")
        self.curve3 = self.plt0.plot(y=self.data_av_temp_2, pen="y",
                                     style=QtCore.Qt.DotLine)
        self.curve4 = self.plt0.plot(y=self.data_temp_3, pen="g",
                                     name="Bottom °C")
        self.curve5 = self.plt0.plot(y=self.data_av_temp_3, pen="g",
                                     style=QtCore.Qt.DotLine)
        self.curve6 = self.plt0.plot(y=self.data_temp_4, pen="b",
                                     name="Water °C")
        self.curve7 = self.plt0.plot(y=self.data_av_temp_4, pen="b",
                                     style=QtCore.Qt.DotLine)
        self.curve8 = self.plt0.plot(y=self.data_temp_5, pen="m",
                                     name="Room °C")
        self.curve9 = self.plt0.plot(y=self.data_av_temp_5, pen="m",
                                     style=QtCore.Qt.DotLine)

        # l.addItem(self.curve0, "Top °C")
        # l.addItem(self.curve2, "Middle °C")
        # l.addItem(self.curve4, "Bottom °C")
        # l.addItem(self.curve6, "Water °C")
        # l.addItem(self.curve8, "Room °C")

        # Save (commit) the changes
        con.commit()

        # Close connection
        con.close()

        self.timer = QtCore.QTimer()
        self.timer.timeout.connect(self.update_data)
        self.timer.start(60000)

        ####################################
        # Temp Settings tab                #
        ####################################
        self.ui.tw_temp.currentChanged.connect(self.get_value_temp)
        self.ui.tw_main.currentChanged.connect(self.get_value_temp)

        self.ui.dial_start.valueChanged.connect(self.ui.lcd_set_start.display)
        self.ui.dial_stop.valueChanged.connect(self.ui.lcd_set_stop.display)

        self.ui.pb_set_temp.clicked.connect(self.set_value_temp)
        self.ui.pb_set_temp.clicked.connect(self.get_value_temp)

        ####################################
        # Light Settings tab               #
        ####################################
        self.ui.tw_light.currentChanged.connect(self.get_value_light)
        self.ui.tw_main.currentChanged.connect(self.get_value_light)

        self.ui.dial_on_h.valueChanged.connect(self.ui.lcd_new_on_h.display)
        self.ui.dial_on_m.valueChanged.connect(self.ui.lcd_new_on_m.display)
        self.ui.dial_off_h.valueChanged.connect(self.ui.lcd_new_off_h.display)
        self.ui.dial_off_m.valueChanged.connect(self.ui.lcd_new_off_m.display)

        self.ui.pb_set_light.clicked.connect(self.set_value_light)
        self.ui.pb_set_light.clicked.connect(self.get_value_light)

        self.showFullScreen()
        self.show()

    def update_data(self):
        # Initialise data arrays
        update_data_tst = []
        update_data_temp_1 = []
        update_data_av_temp_1 = []
        update_data_temp_2 = []
        update_data_av_temp_2 = []
        update_data_temp_3 = []
        update_data_av_temp_3 = []
        update_data_temp_4 = []
        update_data_av_temp_4 = []
        update_data_temp_5 = []
        update_data_av_temp_5 = []

        # Initialise sqlite
        con = sqlite3.connect('data.db')
        cur = con.cursor()

        # Select all data ordered and append lists
        cur.execute(
            "SELECT * FROM temperature ORDER BY timestamp ASC LIMIT 1440")
        update_data = cur.fetchall()
        for row in update_data:
            update_data_tst.append(row[0])
            update_data_temp_1.append(row[1])
            update_data_temp_2.append(row[2])
            update_data_temp_3.append(row[3])
            update_data_temp_4.append(row[4])
            update_data_temp_5.append(row[5])

        # Average value
        update_average_1 = sum(update_data_temp_1) / float(
            len(update_data_temp_1))
        for i in update_data_temp_1:
            update_data_av_temp_1.append(update_average_1)
        update_average_2 = sum(update_data_temp_2) / float(
            len(update_data_temp_2))
        for i in update_data_temp_2:
            update_data_av_temp_2.append(update_average_2)
        update_average_3 = sum(update_data_temp_3) / float(
            len(update_data_temp_3))
        for i in update_data_temp_3:
            update_data_av_temp_3.append(update_average_3)
        update_average_4 = sum(update_data_temp_4) / float(
            len(update_data_temp_4))
        for i in update_data_temp_4:
            update_data_av_temp_4.append(update_average_4)
        update_average_5 = sum(update_data_temp_5) / float(
            len(update_data_temp_5))
        for i in update_data_temp_5:
            update_data_av_temp_5.append(update_average_5)

        # Save (commit) the changes
        con.commit()

        # Close connection
        con.close()

        # Update data
        self.curve0.setData(update_data_tst)
        self.curve0.setData(update_data_temp_1)
        self.curve1.setData(update_data_tst)
        self.curve1.setData(update_data_av_temp_1)
        self.curve2.setData(update_data_tst)
        self.curve2.setData(update_data_temp_2)
        self.curve3.setData(update_data_tst)
        self.curve3.setData(update_data_av_temp_2)
        self.curve4.setData(update_data_tst)
        self.curve4.setData(update_data_temp_3)
        self.curve5.setData(update_data_tst)
        self.curve5.setData(update_data_av_temp_3)
        self.curve6.setData(update_data_tst)
        self.curve6.setData(update_data_temp_4)
        self.curve7.setData(update_data_tst)
        self.curve7.setData(update_data_av_temp_4)
        self.curve8.setData(update_data_tst)
        self.curve8.setData(update_data_temp_5)
        self.curve9.setData(update_data_tst)
        self.curve9.setData(update_data_av_temp_5)

    def get_value_temp(self):
        setting = "fan"

        # Initialise sqlite
        con = sqlite3.connect('data.db')
        cur = con.cursor()

        # Create table
        cur.execute('''CREATE TABLE IF NOT EXISTS settings
                     (setting TEXT, data1 INT, data2 INT)''')

        # Select data
        cur.execute("SELECT data1, data2 FROM settings WHERE setting = ?",
                    (setting,))
        data = cur.fetchone()
        value_start = data[0]
        value_stop = data[1]

        # Save (commit) the changes
        con.commit()

        # Close connection
        con.close()

        self.ui.lcd_cur_start.display(value_start)
        self.ui.lcd_cur_stop.display(value_stop)

        self.repaint()

    def set_value_temp(self):
        setting = "fan"
        value_start = self.ui.lcd_set_start.value()
        value_stop = self.ui.lcd_set_stop.value()

        # Initialise sqlite
        con = sqlite3.connect('data.db')
        cur = con.cursor()

        # Create table
        cur.execute('''CREATE TABLE IF NOT EXISTS settings
                     (setting TEXT, data1 INT, data2 INT)''')

        # Insert a row of data
        cur.execute(
            "UPDATE settings SET data1 = ?, data2 = ? WHERE setting = ?",
            (value_start, value_stop, setting))

        # Save (commit) the changes
        con.commit()

        # Close connection
        con.close()

    def get_value_light(self):
        setting1 = "light on"
        setting2 = "light off"

        # Initialise sqlite
        con = sqlite3.connect('data.db')
        cur = con.cursor()

        # Create table
        cur.execute('''CREATE TABLE IF NOT EXISTS settings
                     (setting TEXT, data1 INT, data2 INT)''')

        # Select data
        cur.execute("SELECT data1, data2 FROM settings WHERE setting = ?",
                    (setting1,))
        data = cur.fetchone()
        value_light_on_h = data[0]
        value_light_on_m = data[1]

        cur.execute("SELECT data1, data2 FROM settings WHERE setting = ?",
                    (setting2,))
        data = cur.fetchone()
        value_light_off_h = data[0]
        value_light_off_m = data[1]

        # Save (commit) the changes
        con.commit()

        # Close connection
        con.close()

        self.ui.lcd_cur_on_h.display(value_light_on_h)
        self.ui.lcd_cur_on_m.display(value_light_on_m)
        self.ui.lcd_cur_off_h.display(value_light_off_h)
        self.ui.lcd_cur_off_m.display(value_light_off_m)

        self.repaint()

    def set_value_light(self):
        setting1 = "light on"
        setting2 = "light off"
        value_light_on_h = self.ui.lcd_new_on_h.value()
        value_light_on_m = self.ui.lcd_new_on_m.value()
        value_light_off_h = self.ui.lcd_new_off_h.value()
        value_light_off_m = self.ui.lcd_new_off_m.value()

        # Initialise sqlite
        con = sqlite3.connect('data.db')
        cur = con.cursor()

        # Create table
        cur.execute('''CREATE TABLE IF NOT EXISTS settings
                     (setting TEXT, data1 INT, data2 INT)''')

        # Insert a row of data
        cur.execute(
            "UPDATE settings SET data1 = ?, data2 = ? WHERE setting = ?",
            (value_light_on_h, value_light_on_m, setting1))
        cur.execute(
            "UPDATE settings SET data1 = ?, data2 = ? WHERE setting = ?",
            (value_light_off_h, value_light_off_m, setting2))

        # Save (commit) the changes
        con.commit()

        # Close connection
        con.close()

    def exit(self):
        sys.exit()

    def reboot(self):
        os.system("sudo shutdown -r now")

    def shutdown(self):
        os.system("sudo shutdown -P now")


if __name__ == "__main__":
    app = QtWidgets.QApplication(sys.argv)
    window = Ui()
    sys.exit(app.exec_())
