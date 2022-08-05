import pytest
from ss import SpreadsheetAPI


class Test:
    def setup(self):
        self.spreadsheet_id = "1Lgo3zaNTP2yOf1T-U-K4BSss04U6McTBPRMGVQtTNE4"
        self.sheet_title = "Лист1"
        self.sheet_id = "0"
        self.credentials = 'tests-358414-baea7a149cfb.json'
        self.apis = 'https://www.googleapis.com/auth/spreadsheets'
        self.Test_instance = SpreadsheetAPI(self.spreadsheet_id, self.sheet_title, self.sheet_id, self.credentials,
                                            self.apis)
        self.test_ar = [['1', 'test', '3', '4'], ['1', '', '3', '4']]

    # get_sheet
    # Проерка схемы ответа из пустой таблицы
    def test_01(self):
        sheet = self.Test_instance.get_sheet()
        assert 'majorDimension' in sheet and 'range' in sheet and 'values' not in sheet

    # get_sheet
    # Проверка схемы ответа из не пустой таблицы
    def test_02(self):
        self.Test_instance.insert(self.test_ar, 'A', 'D')
        sheet = self.Test_instance.get_sheet()
        self.Test_instance.clear('A1:D2')
        assert 'majorDimension' in sheet and 'range' in sheet and 'values' in sheet

    # get_sheet
    # Проверка правильности полученных данных
    def test_03(self):
        self.Test_instance.insert(self.test_ar, 'A', 'D')
        sheet = self.Test_instance.get_sheet()
        self.Test_instance.clear('A1:D2')
        assert sheet['values'] == self.test_ar

    # get
    # Проерка схемы ответа из пустой таблицы
    def test_04(self):
        sheet = self.Test_instance.get(self.sheet_title)
        assert 'majorDimension' in sheet and 'range' in sheet and 'values' not in sheet

    # get
    # Проерка схемы ответа из не пустой таблицы
    def test_05(self):
        self.Test_instance.insert(self.test_ar, 'A', 'D')
        sheet = self.Test_instance.get(self.sheet_title)
        self.Test_instance.clear('A1:D2')
        assert 'majorDimension' in sheet and 'range' in sheet and 'values' in sheet

    # get
    # Проерка правильности полученных данных
    def test_06(self):
        self.Test_instance.insert(self.test_ar, 'A', 'D')
        sheet = self.Test_instance.get("A1:C2")
        self.Test_instance.clear('A1:D2')
        assert sheet['values'] == [['1', 'test', '3'], ['1', '', '3']]

    # get
    # Проерка правильности диапазона
    def test_07(self):
        self.Test_instance.insert(self.test_ar, 'A', 'D')
        sheet = self.Test_instance.get("A1:B2")
        self.Test_instance.clear('A1:D2')
        assert sheet['range'] == "'Лист1'!A1:B2"

    # get
    # Проерка выборки пустых ячеек из не пустой таблицы
    def test_08(self):
        self.Test_instance.insert(self.test_ar, 'A', 'D')
        sheet = self.Test_instance.get('E1:F2')
        self.Test_instance.clear('A1:D2')
        assert sheet == {'majorDimension': 'ROWS', 'range': "'Лист1'!E1:F2"}

    # insert
    # Проверка Возврата True
    def test_09(self):
        ins = self.Test_instance.insert(self.test_ar, 'A', 'D')
        self.Test_instance.clear('A1:D2')
        assert ins is True

    # insert
    # Проверка Возврата False (не существующий диапазон)
    def test_10(self):
        ins = self.Test_instance.insert(self.test_ar, 'Л', 'Я')
        assert ins is False

    # insert
    # Проверка корректной вставки
    def test_11(self):
        ins = self.Test_instance.insert(self.test_ar, 'A', 'D')
        sheet = self.Test_instance.get_sheet()
        self.Test_instance.clear('A1:D2')
        assert sheet['values'] == self.test_ar

    # insert
    # Проверка вставки 1 эллемента
    def test_12(self):
        ins = self.Test_instance.insert([['test']], 'A')
        sheet = self.Test_instance.get_sheet()
        self.Test_instance.clear('A1:D2')
        assert sheet['values'] == [['test']]

    # insert
    # Вставка в несуществующий лист
    def test_13(self):
        ins = self.Test_instance.insert(self.test_ar, 'A', 'D', 'Лист2')
        sheet = self.Test_instance.get_sheet()
        self.Test_instance.clear('A1:D2')
        assert ins is False

    # insert
    # Вставка без указания диапазона
    def test_14(self):
        ins = self.Test_instance.insert(self.test_ar)
        sheet = self.Test_instance.get_sheet()
        self.Test_instance.clear('A1:D2')
        assert sheet['values'] == self.test_ar

    # insert
    # Вставка без указания начала диапазона
    def test_15(self):
        ins = self.Test_instance.insert(self.test_ar, None, 'D')
        sheet = self.Test_instance.get_sheet()
        self.Test_instance.clear('A1:D2')
        assert sheet['values'] == self.test_ar

    # insert
    # Вставка без указания конца диапазона
    def test_16(self):
        ins = self.Test_instance.insert(self.test_ar, 'B', None)
        sheet = self.Test_instance.get_sheet()
        self.Test_instance.clear('B1:E2')
        assert sheet['values'] == [['', '1', 'test', '3', '4'], ['', '1', '', '3', '4']]

    # insert
    # Вставка в заполненные ячейки
    def test_17(self):
        ins = self.Test_instance.insert(self.test_ar, 'B', 'E')
        ins = self.Test_instance.insert(self.test_ar, 'A', 'D')
        sheet = self.Test_instance.get('A1:D2')
        self.Test_instance.clear('A1:E2')
        assert sheet['values'] == self.test_ar
