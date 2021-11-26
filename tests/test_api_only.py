from unittest import TestCase

from api_only import TelegramBot


class test_Telegram_Size(TestCase):
    def test_Telegram_Size_big(self):
        bot = TelegramBot()
        bot.text = "Большую"
        bot.get_size()
        self.assertEqual(bot.state, 'pay')

    def test_Telegram_Size_small(self):
        bot = TelegramBot()
        bot.text = "Маленькую"
        bot.get_size()
        self.assertEqual(bot.state, 'pay')

    def test_Telegram_Size_unexpected(self):
        bot = TelegramBot()
        bot.text = "Круглую"
        bot.get_size()
        self.assertEqual(bot.state, 'size')


class test_Telegram_Pay(TestCase):
    def test_Telegram_Pay_cash(self):
        bot = TelegramBot()
        bot.text = 'Наличкой'
        bot.get_size()
        bot.get_pay()
        self.assertEqual(bot.state, 'order')

    def test_Telegram_Pay_cashless(self):
        bot = TelegramBot()
        bot.text = "Безналичным"
        bot.get_size()
        bot.get_pay()
        self.assertEqual(bot.state, 'order')

    def test_Telegram_Pay_unexpected(self):
        bot = TelegramBot()
        bot.text = "Золотом"
        bot.get_size()
        bot.get_pay()
        self.assertEqual(bot.state, 'pay')


class test_Telegram_Order(TestCase):
    def test_Telegram_Order_yes(self):
        bot = TelegramBot()
        bot.text = 'Да'
        bot.get_size()
        bot.get_pay()
        bot.get_order()
        self.assertEqual(bot.state, 'wait')

    def test_Telegram_Order_no(self):
        bot = TelegramBot()
        bot.text = 'Нет'
        bot.get_size()
        bot.get_pay()
        bot.get_order()
        self.assertEqual(bot.state, 'size')

    def test_Telegram_Order_unexpected(self):
        bot = TelegramBot()
        bot.text = 'Не знаю'
        bot.get_size()
        bot.get_pay()
        bot.get_order()
        self.assertEqual(bot.state, 'order')
