import pathlib
import urllib.error

import allure

from functions.ss import SpreadsheetAPI


class Test:
    def setup(self):
        self.spreadsheet_id = "1Lgo3zaNTP2yOf1T-U-K4BSss04U6McTBPRMGVQtTNE4"
        self.sheet_title = "Лист1"
        self.sheet_id = "0"
        ex_path = pathlib.Path.home() / 'Desktop' / 'Test_Google_Sheets_API' / 'tests' / 'tests-358414-baea7a149cfb' \
                                                                                         '.json '
        self.credentials = ex_path
        self.apis = 'https://www.googleapis.com/auth/spreadsheets'
        self.Test_instance = SpreadsheetAPI(self.spreadsheet_id, self.sheet_title, self.sheet_id, self.credentials,
                                            self.apis)
        self.test_ar = [['1', 'test', '3', '4'], ['1', '', '3', '4']]

    @allure.feature('get_sheet')
    @allure.story('Проерка схемы ответа из пустой таблицы')
    def test_01(self):
        sheet = self.Test_instance.get_sheet()
        assert 'majorDimension' in sheet and 'range' in sheet and 'values' not in sheet

    @allure.feature('get_sheet')
    @allure.story('Проверка схемы ответа из не пустой таблицы')
    def test_02(self):
        self.Test_instance.insert(self.test_ar, 'A', 'D')
        sheet = self.Test_instance.get_sheet()
        self.Test_instance.clear('A1:D2')
        assert 'majorDimension' in sheet and 'range' in sheet and 'values' in sheet

    @allure.feature('get_sheet')
    @allure.story('Проверка правильности полученных данных')
    def test_03(self):
        self.Test_instance.insert(self.test_ar, 'A', 'D')
        sheet = self.Test_instance.get_sheet()
        self.Test_instance.clear('A1:D2')
        assert sheet['values'] == self.test_ar

    @allure.feature('get')
    @allure.story('Проверка схемы ответа из пустой таблицы')
    def test_04(self):
        sheet = self.Test_instance.get(self.sheet_title)
        assert 'majorDimension' in sheet and 'range' in sheet and 'values' not in sheet

    @allure.feature('get')
    @allure.story('Проверка схемы ответа из не пустой таблицы')
    def test_05(self):
        self.Test_instance.insert(self.test_ar, 'A', 'D')
        sheet = self.Test_instance.get(self.sheet_title)
        self.Test_instance.clear('A1:D2')
        assert 'majorDimension' in sheet and 'range' in sheet and 'values' in sheet

    @allure.feature('get')
    @allure.story('Проверка правильности полученных данных')
    def test_06(self):
        self.Test_instance.insert(self.test_ar, 'A', 'D')
        sheet = self.Test_instance.get("A1:C2")
        self.Test_instance.clear('A1:D2')
        assert sheet['values'] == [['1', 'test', '3'], ['1', '', '3']]

    @allure.feature('get')
    @allure.story('Проерка правильности диапазона')
    def test_07(self):
        self.Test_instance.insert(self.test_ar, 'A', 'D')
        sheet = self.Test_instance.get("A1:B2")
        self.Test_instance.clear('A1:D2')
        assert sheet['range'] == "'Лист1'!A1:B2"

    @allure.feature('get')
    @allure.story('Проерка выборки пустых ячеек из не пустой таблицы')
    def test_08(self):
        self.Test_instance.insert(self.test_ar, 'A', 'D')
        sheet = self.Test_instance.get('E1:F2')
        self.Test_instance.clear('A1:D2')
        assert sheet == {'majorDimension': 'ROWS', 'range': "'Лист1'!E1:F2"}

    @allure.feature('insert')
    @allure.story('Проверка Возврата True')
    def test_09(self):
        ins = self.Test_instance.insert(self.test_ar, 'A', 'D')
        self.Test_instance.clear('A1:D2')
        assert ins is True

    @allure.feature('insert')
    @allure.story('Проверка Возврата False (не существующий диапазон)')
    def test_10(self):
        ins = self.Test_instance.insert(self.test_ar, 'Л', 'Я')
        assert ins is False

    @allure.feature('insert')
    @allure.story('Проверка корректной вставки')
    def test_11(self):
        self.Test_instance.insert(self.test_ar, 'A', 'D')
        sheet = self.Test_instance.get_sheet()
        self.Test_instance.clear('A1:D2')
        assert sheet['values'] == self.test_ar

    @allure.feature('insert')
    @allure.story('Проверка вставки 1 эллемента')
    def test_12(self):
        self.Test_instance.insert([['test']], 'A')
        sheet = self.Test_instance.get_sheet()
        self.Test_instance.clear('A1:D2')
        assert sheet['values'] == [['test']]

    @allure.feature('insert')
    @allure.story('Вставка в несуществующий лист')
    def test_13(self):
        ins = self.Test_instance.insert(self.test_ar, 'A', 'D', 'Лист2')
        self.Test_instance.get_sheet()
        self.Test_instance.clear('A1:D2')
        assert ins is False

    @allure.feature('insert')
    @allure.story('Вставка без указания диапазона')
    def test_14(self):
        self.Test_instance.insert(self.test_ar)
        sheet = self.Test_instance.get_sheet()
        self.Test_instance.clear('A1:D2')
        assert sheet['values'] == self.test_ar

    @allure.feature('insert')
    @allure.story('Вставка без указания начала диапазона')
    def test_15(self):
        self.Test_instance.insert(self.test_ar, None, 'D')
        sheet = self.Test_instance.get_sheet()
        self.Test_instance.clear('A1:D2')
        assert sheet['values'] == self.test_ar

    @allure.feature('insert')
    @allure.story('Вставка без указания конца диапазона')
    def test_16(self):
        self.Test_instance.insert(self.test_ar, 'B', None)
        sheet = self.Test_instance.get_sheet()
        self.Test_instance.clear('B1:E2')
        assert sheet['values'] == [['', '1', 'test', '3', '4'], ['', '1', '', '3', '4']]

    @allure.feature('insert')
    @allure.story('Вставка без указания конца и начала но с указанием страницы')
    def test_17(self):
        self.Test_instance.insert(self.test_ar, None, None, 'Лист1')
        sheet = self.Test_instance.get_sheet()
        self.Test_instance.clear('A1:D2')
        assert sheet['values'] == self.test_ar

    @allure.feature('insert')
    @allure.story('Вставка в заполненные ячейки')
    def test_18(self):
        self.Test_instance.insert(self.test_ar, 'B', 'E')
        self.Test_instance.insert(self.test_ar, 'A', 'D')
        sheet = self.Test_instance.get('A1:D2')
        self.Test_instance.clear('A1:E2')
        assert sheet['values'] == self.test_ar

    @allure.feature('insert')
    @allure.story('Вставка большего массива в меньший диапазон')
    def test_19(self):
        ins = self.Test_instance.insert(self.test_ar, 'A', 'C')
        self.Test_instance.clear('A1:D2')
        assert ins is False

    @allure.feature('clear')
    @allure.story('Удаление страницы полностью')
    def test_20(self):
        self.Test_instance.insert(self.test_ar, 'A', 'D')
        self.Test_instance.clear(self.sheet_title)
        sheet = self.Test_instance.get_sheet()
        assert 'values' not in sheet

    @allure.feature('clear')
    @allure.story('Удаление диапазона')
    def test_21(self):
        self.Test_instance.insert(self.test_ar, 'A', 'D')
        self.Test_instance.clear('C1:D2')
        sheet = self.Test_instance.get_sheet()
        self.Test_instance.clear('A1:D2')
        assert sheet['values'] == [['1', 'test'], ['1']]

    @allure.feature('clear')
    @allure.story('Удаление одной ячейки')
    def test_22(self):
        self.Test_instance.insert(self.test_ar, 'A', 'D')
        self.Test_instance.clear('A1')
        sheet = self.Test_instance.get_sheet()
        self.Test_instance.clear('A1:D2')
        assert sheet['values'] == [['', 'test', '3', '4'], ['1', '', '3', '4']]

    @allure.feature('clear')
    @allure.story('Удаление не реального листа')
    def test_23(self):
        a = urllib.error.HTTPError
        try:
            self.Test_instance.clear('Лист2')
        except Exception as e:
            a = e
        assert a.reason == 'Unable to parse range: Лист2'

    @allure.feature('clear')
    @allure.story('Удаление не реального диапазона')
    def test_24(self):
        a = urllib.error.HTTPError
        try:
            self.Test_instance.clear('Л1:K1')
        except Exception as e:
            a = e
        assert a.reason == 'Unable to parse range: Л1:K1'

    @allure.feature('clear')
    @allure.story('Удаление с диапазоном наоборот')
    def test_25(self):
        self.Test_instance.insert(self.test_ar, 'A', 'D')
        self.Test_instance.clear('D2:A1')
        sheet = self.Test_instance.get_sheet()
        assert 'values' not in sheet

    @allure.feature('get_sheet_url')
    @allure.story('Генерация')
    def test_26(self):
        assert self.Test_instance.get_sheet_url() == 'https://docs.google.com/spreadsheets/d/' + self.spreadsheet_id + \
               '/edit#gid=' + self.sheet_id
