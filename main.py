import io
import sys
import sqlite3

from PyQt6 import uic  # Импортируем uic
from PyQt6.QtWidgets import QApplication, QMainWindow, QTableWidgetItem

template = """<?xml version="1.0" encoding="UTF-8"?>
<ui version="4.0">
 <class>MainWindow</class>
 <widget class="QMainWindow" name="MainWindow">
  <property name="geometry">
   <rect>
    <x>0</x>
    <y>0</y>
    <width>975</width>
    <height>525</height>
   </rect>
  </property>
  <property name="minimumSize">
   <size>
    <width>975</width>
    <height>525</height>
   </size>
  </property>
  <property name="maximumSize">
   <size>
    <width>975</width>
    <height>525</height>
   </size>
  </property>
  <property name="windowTitle">
   <string>Поиск по фильмам 2.0</string>
  </property>
  <widget class="QWidget" name="centralwidget">
   <widget class="QLabel" name="label">
    <property name="geometry">
     <rect>
      <x>10</x>
      <y>10</y>
      <width>91</width>
      <height>41</height>
     </rect>
    </property>
    <property name="font">
     <font>
      <pointsize>16</pointsize>
     </font>
    </property>
    <property name="text">
     <string>Год</string>
    </property>
   </widget>
   <widget class="QLineEdit" name="year">
    <property name="geometry">
     <rect>
      <x>10</x>
      <y>70</y>
      <width>161</width>
      <height>41</height>
     </rect>
    </property>
   </widget>
   <widget class="QLabel" name="label_2">
    <property name="geometry">
     <rect>
      <x>10</x>
      <y>130</y>
      <width>141</width>
      <height>41</height>
     </rect>
    </property>
    <property name="font">
     <font>
      <pointsize>16</pointsize>
     </font>
    </property>
    <property name="text">
     <string>Название</string>
    </property>
   </widget>
   <widget class="QLineEdit" name="title">
    <property name="geometry">
     <rect>
      <x>10</x>
      <y>180</y>
      <width>161</width>
      <height>41</height>
     </rect>
    </property>
   </widget>
   <widget class="QLabel" name="label_3">
    <property name="geometry">
     <rect>
      <x>10</x>
      <y>240</y>
      <width>141</width>
      <height>31</height>
     </rect>
    </property>
    <property name="font">
     <font>
      <pointsize>16</pointsize>
     </font>
    </property>
    <property name="text">
     <string>Длина</string>
    </property>
   </widget>
   <widget class="QPushButton" name="queryButton">
    <property name="geometry">
     <rect>
      <x>10</x>
      <y>390</y>
      <width>151</width>
      <height>71</height>
     </rect>
    </property>
    <property name="font">
     <font>
      <pointsize>16</pointsize>
     </font>
    </property>
    <property name="text">
     <string>Пуск</string>
    </property>
   </widget>
   <widget class="QTableWidget" name="tableWidget">
    <property name="geometry">
     <rect>
      <x>190</x>
      <y>0</y>
      <width>781</width>
      <height>521</height>
     </rect>
    </property>
   </widget>
   <widget class="QLineEdit" name="duration">
    <property name="geometry">
     <rect>
      <x>10</x>
      <y>290</y>
      <width>161</width>
      <height>41</height>
     </rect>
    </property>
   </widget>
  </widget>
 </widget>
 <resources/>
 <connections/>
</ui>

"""


class MyWidget(QMainWindow):
    def __init__(self):
        super().__init__()
        f = io.StringIO(template)
        uic.loadUi(f, self)  # Загружаем дизайн

        self.queryButton.clicked.connect(self.act)

    def act(self):
        text = (f'SELECT * FROM films WHERE duration {self.duration.text()} AND year {self.year.text()} '
                    f'AND title {self.title.text()}')

        # Подключение к БД
        con = sqlite3.connect('films_db.sqlite')

        # Создание курсора
        cur = con.cursor()

        # Выполнение запроса и получение всех результатов
        res = cur.execute(text).fetchall()
        con.close()

        # Заполним размеры таблицы
        header_labels = ['id', 'title', 'year', 'genre', 'duration']  # Замените на ваши заголовки
        self.tableWidget.setColumnCount(len(header_labels))  # Установите количество столбцов
        self.tableWidget.setHorizontalHeaderLabels(header_labels)

        self.tableWidget.setRowCount(len(res))
        # Заполняем таблицу элементами
        for i, row in enumerate(res):
            for j, elem in enumerate(row):
                self.tableWidget.setItem(
                    i, j, QTableWidgetItem(str(elem)))


def except_hook(cls, exception, traceback):
    sys.__excepthook__(cls, exception, traceback)


if __name__ == '__main__':
    app = QApplication(sys.argv)
    ex = MyWidget()
    ex.show()
    sys.excepthook = except_hook
    sys.exit(app.exec())
