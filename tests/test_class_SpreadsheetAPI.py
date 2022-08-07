import urllib.error
from functions.ss import SpreadsheetAPI
import pytest


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
    # Вставка без указания конца и начала но с указанием страницы
    def test_17(self):
        ins = self.Test_instance.insert(self.test_ar, None, None, 'Лист1')
        sheet = self.Test_instance.get_sheet()
        self.Test_instance.clear('A1:D2')
        assert sheet['values'] == self.test_ar

    # insert
    # Вставка в заполненные ячейки
    def test_18(self):
        ins = self.Test_instance.insert(self.test_ar, 'B', 'E')
        ins = self.Test_instance.insert(self.test_ar, 'A', 'D')
        sheet = self.Test_instance.get('A1:D2')
        self.Test_instance.clear('A1:E2')
        assert sheet['values'] == self.test_ar

    # insert
    # Вставка большего массива в меньший диапазон
    def test_19(self):
        ins = self.Test_instance.insert(self.test_ar, 'A', 'C')
        self.Test_instance.clear('A1:D2')
        assert ins is False

    # clear
    # Удаление страницы полностью
    def test_20(self):
        ins = self.Test_instance.insert(self.test_ar, 'A', 'D')
        cl = self.Test_instance.clear(self.sheet_title)
        sheet = self.Test_instance.get_sheet()
        assert 'values' not in sheet

    # clear
    # Удаление диапазона
    def test_21(self):
        ins = self.Test_instance.insert(self.test_ar, 'A', 'D')
        cl = self.Test_instance.clear('C1:D2')
        sheet = self.Test_instance.get_sheet()
        cl = self.Test_instance.clear('A1:D2')
        assert sheet['values'] == [['1', 'test'], ['1']]

    # clear
    # Удаление одной ячейки
    def test_22(self):
        ins = self.Test_instance.insert(self.test_ar, 'A', 'D')
        cl = self.Test_instance.clear('A1')
        sheet = self.Test_instance.get_sheet()
        cl = self.Test_instance.clear('A1:D2')
        assert sheet['values'] == [['', 'test', '3', '4'], ['1', '', '3', '4']]

    # clear
    # Удаление не реального листа
    def test_23(self):
        a = urllib.error.HTTPError
        try:
            self.Test_instance.clear('Лист2')
        except Exception as e:
            a = e
        assert a.reason == 'Unable to parse range: Лист2'

    # clear
    # Удаление не реального диапазона
    def test_24(self):
        a = urllib.error.HTTPError
        try:
            self.Test_instance.clear('Л1:K1')
        except Exception as e:
            a = e
        assert a.reason == 'Unable to parse range: Л1:K1'

    # clear
    # Удаление с диапазоном наоборот.
    def test_25(self):
        ins = self.Test_instance.insert(self.test_ar, 'A', 'D')
        cl = self.Test_instance.clear('D2:A1')
        sheet = self.Test_instance.get_sheet()
        assert 'values' not in sheet

    # get_sheet_url
    # Генерация
    def test_26(self):
        assert self.Test_instance.get_sheet_url() == 'https://docs.google.com/spreadsheets/d/' + self.spreadsheet_id + '/edit#gid=' + self.sheet_id
