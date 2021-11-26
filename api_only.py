import requests
from transitions import Machine


class TelegramBot(object):
    __api_url = 'https://api.telegram.org/bot'
    __token = ''

    size = ''
    pay = ''
    chat_id = ''
    text = ''
    last_update = ''
    states = ['wait', 'size', 'pay', 'order']

    def __init__(self):
        if self.__token == '':
            print('Enter your telegram_token: ')
            self.__token = input()

        self.machine = Machine(self, self.states, 'wait')
        self.machine.add_transition('get_size', '*', 'size', after='ask_size')
        self.machine.add_transition('get_pay', 'size', 'pay', after='ask_pay')
        self.machine.add_transition('get_order', 'pay', 'order', after='ask_order')
        self.machine.add_transition('get_ready', '*', 'wait')

    def get_updates(self):
        update = requests.get(self.__api_url + self.__token + '/getUpdates?offset=-1').json()
        if self.last_update != update['result'][0]['update_id']:
            self.chat_id = update['result'][0]['message']['chat']['id']
            self.text = update['result'][0]['message']['text']

            bot_state = self.state
            if self.text == '/start':
                self.get_size()

            elif bot_state == 'size':
                self.ask_size()

            elif bot_state == 'pay':
                self.ask_pay()

            elif bot_state == 'order':
                self.ask_order()

            if self.last_update == '':
                print('Bot connected')
            else:
                print(f'User: {self.chat_id} [{self.state}]')
            self.last_update = update['result'][0]['update_id']

    def ask_size(self):
        answer = self.text.lower()
        if answer == 'большую' or answer == 'маленькую':
            self.size = answer
            self.get_pay()
        elif self:
            ask = 'Какую вы хотите пиццу? Большую или маленькую?'
            requests.get(self.__api_url + self.__token + f'/sendMessage?chat_id={self.chat_id}&text={ask}')

    def ask_pay(self):
        answer = self.text.lower()
        if answer == 'наличкой' or answer == 'безналичным':
            self.pay = answer
            self.get_order()
        else:
            ask = 'Как вы будете платить?'
            requests.get(self.__api_url + self.__token + f'/sendMessage?chat_id={self.chat_id}&text={ask}')

    def ask_order(self):
        answer = self.text.lower()
        if answer == 'да':
            requests.get(self.__api_url + self.__token + f'/sendMessage?chat_id={self.chat_id}&text=Заказ принят')
            self.get_ready()
        elif answer == 'нет':
            self.get_size()
        else:
            ask = f'Вы хотите {self.size} пиццу, оплата - {self.pay}?'
            requests.get(self.__api_url + self.__token + f'/sendMessage?chat_id={self.chat_id}&text={ask}')
