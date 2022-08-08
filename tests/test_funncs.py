import allure

from functions.funcs import get_body_insert
from functions.funcs import get_range


class Test:
    def setup(self):
        self.test_ins = {
            "valueInputOption": "USER_ENTERED",
            "data": [
                {"range": 0,
                 "values": 0}
            ]}

    @allure.feature('get_body_insert')
    @allure.story('Проверяем схему с аргументами 0, 0')
    def test_01(self):
        assert get_body_insert(0, 0) == self.test_ins

    @allure.feature('get_body_insert')
    @allure.story('Проверяем схему с аргументами 1000000000, 10000000000')
    def test_02(self):
        a = self.test_ins
        a['data'][0]['range'] = 1000000000
        a['data'][0]['values'] = 10000000000
        assert get_body_insert(1000000000, 10000000000) == a

    @allure.feature('get_body_insert')
    @allure.story('Проверяем схему с аргументами A1:B4, test')
    def test_03(self):
        a = self.test_ins
        a['data'][0]['range'] = 'A1:B4'
        a['data'][0]['values'] = 'test'
        assert get_body_insert('A1:B4', 'test') == a

    @allure.feature('get_body_insert')
    @allure.story('Проверяем схему с пустыми аргументами')
    def test_04(self):
        a = self.test_ins
        a['data'][0]['range'] = None
        a['data'][0]['values'] = None
        assert get_body_insert(None, None) == a

    @allure.feature('get_range')
    @allure.story('Проверяем если есть и старт и конец')
    def test_05(self):
        assert get_range('A', 'B', 'Test') == 'Test!A:B'

    @allure.feature('get_range')
    @allure.story('Проверяем если нету старта')
    def test_06(self):
        assert get_range(None, 'B', 'Test') == 'Test!A:B'

    @allure.feature('get_range')
    @allure.story('Проверяем если нету конца')
    def test_07(self):
        assert get_range('A', None, 'Test') == 'Test!A:Z'

    @allure.feature('get_range')
    @allure.story('Проверяем если нету старта и конца')
    def test_08(self):
        assert get_range(None, None, 'Test') == 'Test'

    @allure.feature('get_range')
    @allure.story('Проверяем если нету старта и конца и нету названия старницы')
    def test_09(self):
        assert get_range(None, None, None) is None
