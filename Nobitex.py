import requests


class Nobitex:
    def __init__(self, testnet=False):
        self.production_address = 'https://api.nobitex.ir'
        self.testnet_address = 'https://testnetapi.nobitex.net'
        self.url = self.production_address if not testnet else self.testnet_address

    def request(self, path, json=None, token=None):
        header = {'content-type': 'application/json'}
        if token:
            header['Authorization'] = "Token " + token
        if json:
            try:
                response = requests.post(url=self.url + path, headers=header, json=json)
                return True, response
            except Exception as e:
                error = f'Exception: \n{e}'
                return False, error
        else:
            try:
                response = requests.post(url=self.url + path, headers=header)
                return True, response
            except Exception as e:
                error = f'Exception: \n{e}'
                return False, error

    def login(self, username, password, remember=False):
        # return status, value: (success and token ) or (failed and error)
        # For long time tokens(30 days), remember=True  must be entered after username and password.
        # otherwise the program sends remember=False by default and receives four-hours tokens.
        remember = 'yes' if remember else 'no'
        json = {
            'username': username,
            'password': password,
            'remember': remember
        }
        status_response, response = self.request(json=json, path='/auth/login/')
        if status_response:
            if response.status_code == 200 and response.json()['key']:
                token = response.json()['key']
                return {'status': 'success', 'token': token}
            elif response.status_code == 429:
                error = 'You need to log in with Iran\'s IP.'
                return {'status': 'failed', 'error': error}
            else:
                error = response.json()['non_field_errors']
                return {'status': 'failed', 'error': error}
        else:
            return {'status': 'failed', 'error': response}

    def profile(self, token=None):
        # Return profile and personal information.
        status_response, response = self.request(path='/users/profile', token=token)
        if status_response:
            if response.status_code == 200 and response.json()['profile']:
                profile_ = response.json()['profile']
                return f'ok \nProfile: \n{profile_}'
            else:
                error = response.json()['detail']
                return f'Error: \n{error}'
        else:
            return 'failed', response.json()

    def list_of_orders(self, type_=None, src_currency=None, dst_currency='usdt', order_=True):
        # Return list of orders.
        # The program shows the price from high to low by default.
        # For showing from low to high, word " price" should be entered for <order_> variable.
        # <type_> : "buy" or "sell"
        # <src_currency> : Source Currency
        # <dst_currency> : Destination Currency
        order_ = '-price' if order_ else 'price'
        json = {
            "order": order_,
            "type": type_,
            "srcCurrency": src_currency,
            "dstCurrency": dst_currency
        }
        status_response, response = self.request(path='/market/orders/list', json=json)
        if status_response:
            if response.status_code == 200 and response.json()['orders']:
                order_ = response.json()['orders']
                return f'ok \nOrders: \n{order_}'
            else:
                error_1 = response.json()['code']
                error_2 = response.json()['message']
                return f'failed \n{error_1} \n{error_2}'
        else:
            return f'failed \n{response.json()}'

    def list_of_trades(self, src_currency=None, dst_currency=None, my_trades_only=True):
        # Return list of trades.
        # src_currency : Source Currency
        # dst_currency : Destination Currency
        # my_trades_only : Show personal trading list (True or False)
        # Limitation : 15 requests per minute.
        my_trades_only = 'yes' if my_trades_only else 'no'
        json = {
            "srcCurrency": src_currency,
            "dstCurrency": dst_currency,
            "myTradesOnly": my_trades_only
        }
        status_response, response = self.request(path='/market/trades/list', json=json)
        if status_response:
            if response.status_code == 200 and response.json()['status'] == 'ok':
                trade = response.json()['trades']
                return f'ok \nTrades: \n{trade}'
            else:
                error = response.json()['message']
                return f'failed \n{error}'
        else:
            return f'failed \n{response.json()}'

    def nobitex_statistics(self, src_currency=None, dst_currency=None):
        # Return the latest NOBITEX market statistics.
        # src_currency : Source Currency
        # dst_currency : Destination Currency
        # Limitation : 100 requests per 10 minute.
        json = {
            "srcCurrency": src_currency,
            "dstCurrency": dst_currency
        }
        status_response, response = self.request(path='/market/stats', json=json)
        if status_response:
            if response.status_code == 200 and response.json()['status'] == 'ok':
                stats_ = response.json()['stats']
                global_ = response.json()['global']
                return f'ok \nNobitex Statistics: \n{stats_} \nGlobal: \n{global_}'
            else:
                error = response.json()['message']
                return f'failed \n{error}'
        else:
            return f'failed \n{response.json()}'

    def global_statistics(self, i=None):
        # Return the statistics of Binance and Kraken.
        # Limitation : 100 requests per 10 minute.
        del i
        status_response, response = self.request(path='/market/global-stats')
        if status_response:
            if response.status_code == 200 and response.json()['status'] == 'ok':
                market = response.json()['markets']
                return f'ok \nMarkets: \n{market}'
        else:
            return f'failed \n{response.json()}'

    def login_attempts(self, token=None):
        # Return login history
        status_response, response = self.request(path='/users/login-attempts', token=token)
        if status_response:
            if response.status_code == 200 and response.json()['status'] == 'ok':
                attempt = response.json()['attempts']
                return f'ok \nLogin Attempts: \n{attempt}'
            else:
                error = response.json()['detail']
                return f'failed \n{error}'
        else:
            return f'failed \n{response.json()}'

    def referral_code(self, token=None):
        # Return referral code.
        status_response, response = self.request(path='/users/get-referral-code', token=token)
        if status_response:
            if response.status_code == 200 and response.json()['status'] == 'ok':
                referral = response.json()['referralCode']
                return f'ok \nReferral Code: \n{referral}'
            else:
                error = response.json()['detail']
                return f'failed \n{error}'
        else:
            return f'failed \n{response.json()}'

    def limitations(self, token=None):
        # Return your limitations in NOBITEX crypto exchange.
        status_response, response = self.request(path='/users/limitations', token=token)
        if status_response:
            if response.status_code == 200 and response.json()['status'] == "ok":
                limitation = response.json()['limitations']
                return f'ok \nLimitations: \n{limitation}'
            else:
                error = response.json()['detail']
                return f'failed \n{error}'
        else:
            return f'failed \n{response.json()}'

    def wallets_list(self, token=None):
        # Return your own list of wallets.
        status_response, response = self.request(path='/users/wallets/list', token=token)
        if status_response:
            if response.status_code == 200 and response.json()['status'] == "ok":
                wallet = response.json()['wallets']
                return f'ok \nWallets: \n{wallet}'
            else:
                error = response.json()['detail']
                return f'failed \n{error}'
        else:
            return f'failed \n{response.json()}'

    def wallets_balance(self, currency=None, token=None):
        # Return your wallet balance.
        # currency : The wallet you want like "btc" or 'ltc" etc.
        json = {
            'currency': currency
        }
        status_response, response = self.request(path='/users/wallets/balance', json=json, token=token)
        if status_response:
            if response.status_code == 200 and response.json()['status'] == "ok":
                balance = response.json()['balance']
                return f'ok \nBalance: \n{balance} {currency}'
            else:
                error = response.json()
                return f'failed \n{error}'
        else:
            return f'failed \n{response.json()}'

    def transactions_list(self, wallet_id=None, token=None):
        # Return your transactions history.
        # wallet_id : ID of the wallet you want.
        wallet_id = int(wallet_id)
        json = {
            'wallet': wallet_id
        }
        status_response, response = self.request(path='/users/wallets/transactions/list', json=json, token=token)
        if status_response:
            if response.status_code == 200 and response.json()['status'] == "ok":
                transaction = response.json()['transactions']
                return f'ok \nTransactions: \n{transaction}'
            else:
                error = response.json()
                return f'failed \n{error}'
        else:
            return f'failed \n{response.json()}'

    def deposit_withdraw(self, wallet_id=None, token=None):
        # Return a list of deposits and withdrawals.
        # wallet_id : ID of the wallet you want.
        # wallets_id : string
        json = {
            'wallet': wallet_id
        }
        status_response, response = self.request(path='/users/wallets/deposits/list', json=json, token=token)
        if status_response:
            if response.status_code == 200 and response.json()['status'] == "ok":
                deposit = response.json()['deposits']
                withdraw = response.json()['withdraws']
                return f'ok \nDeposits: \n{deposit} \nWithdraws: \n{withdraw}'
            else:
                error = response.json()
                return f'failed \n{error}'
        else:
            return f'failed \n{response.json()}'

    def generate_address(self, wallet_id=None, token=None):
        # return your block chain address.
        # wallet_id : ID of the wallet you want.
        # wallets_id : string
        json = {
            'wallet': wallet_id
        }
        status_response, response = self.request(path='/users/wallets/generate-address', json=json, token=token)
        if status_response:
            if response.status_code == 200 and response.json()['status'] == "ok":
                address = response.json()['address']
                tag = response.json()['tag']
                return f'ok \nAddress: \n{address} \nTag: \n{tag}'
            else:
                error = response.json()
                return f'failed \n{error}'
        else:
            return f'failed \n{response.json()}'

    def order(self, type_, src_currency, dst_currency, amount, price, token, execution=True):
        # Use this function to order.
        # type : "buy" or "sell"
        # src_currency : Source Currency
        # dst_currency : Destination Currency
        # amount = The amount you want to buy or sell.
        # price = Price to buy or sell.
        # execution = (False = 'limit') and (True = 'market')
        # For quick order use word "market" for execution.
        # Limitation : 100 requests per 10 minutes.
        execution = 'market' if execution else 'limit'
        price = int(price)
        json = {
            "type": type_,
            "execution": execution,
            "srcCurrency": src_currency,
            "dstCurrency": dst_currency,
            "amount": amount,
            "price": price
        }
        status_response, response = self.request(path='/market/orders/add', json=json, token=token)
        if status_response:
            if response.status_code == 200 and response.json()['status'] == "ok":
                order_ = response.json()['order']
                return f'ok \nOrder: \n{order_}'
            else:
                error = response.json()
                return f'failed \n{error}'
        else:
            return f'failed \n{response.json()}'

    def order_cancel(self, src_currency, dst_currency, hours, token, execution="market"):
        # Use this function to cancel order.
        # srcCurrency : Source Currency
        # dstCurrency : Destination Currency
        # hours : To determine the time period you want to cancel its orders.
        # execution = (False = 'limit') and (True = 'market')
        execution = 'market' if execution else 'limit'
        hours = float(hours)
        json = {
            "execution": execution,
            "srcCurrency": src_currency,
            "dstCurrency": dst_currency,
            "hours": hours
        }
        status_response, response = self.request(path='/market/orders/cancel-old', json=json, token=token)
        if status_response:
            if response.status_code == 200 and response.json()['status'] == "ok":
                status = response.json()['status']
                return f'Status: \n{status}'
            else:
                error = response.json()
                return f'failed \n{error}'
        else:
            return f'failed \n{response.json()}'
