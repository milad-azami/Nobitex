import requests


URL = "https://testnetapi.nobitex.net"


def request(path, json=None, token=None):
    if token:
        header = {"Authorization": "Token " + token,
                  "content-type": "application/json"}
        if json:
            try:
                response = requests.post(
                    url=URL + path,
                    headers=header,
                    json=json
                )
                return True, response
            except Exception as e:
                error = f'Exception: \n{e}'
                return False, error
        else:
            try:
                response = requests.post(
                    url=URL + path,
                    headers=header
                )
                return True, response
            except Exception as e:
                error = f'Exception: \n{e}'
                return False, error
    else:
        header = {"content-type": "application/json"}
        if json:
            try:
                response = requests.post(
                    url=URL + path,
                    headers=header,
                    json=json
                )
                return True, response
            except Exception as e:
                error = f'Exception: \n{e}'
                return False, error
        else:
            try:
                response = requests.post(
                    url=URL + path,
                    headers=header
                )
                return True, response
            except Exception as e:
                error = f'Exception: \n{e}'
                return False, error


def login(username, password, remember=False):
    # return status, value: (success and token ) or (failed and error)
    # For long time tokens(30 days), remember=True  must be entered after username and password.
    # otherwise the program sends remember=False by default and receives four-hours tokens.
    remember = 'yes' if remember else 'no'
    json = {
        'username': username,
        'password': password,
        'remember': remember
    }
    status_response, response = request(json=json, path='/auth/login/')
    if status_response:
        if response.status_code == 200 and response.json()['key']:
            token = response.json()['key']
            return f'Success \nToken: {token} \nYou need this token for using other function.'
        elif response.status_code == 429:
            error = 'You need to log in with Iran\'s IP.'
            return error
        else:
            error = response.json()['non_field_errors']
            return f'failed \n{error}'
    else:
        return f'failed \n{response.json()}'


def profile(token=None):
    # Return profile and personal information.
    status_response, response = request(path='/users/profile', token=token)
    if status_response:
        if response.status_code == 200 and response.json()['profile']:
            profile_ = response.json()['profile']
            return f'ok \nProfile: \n{profile_}'
        else:
            error = response.json()['detail']
            return f'Error: \n{error}'
    else:
        return 'failed', response.json()


def list_of_orders(type_=None, src_currency=None, dst_currency='usdt', order_=True):
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
    status_response, response = request(path='/market/orders/list', json=json)
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


def list_of_trades(src_currency=None, dst_currency=None, my_trades_only=True):
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
    status_response, response = request(path='/market/trades/list', json=json)
    if status_response:
        if response.status_code == 200 and response.json()['status'] == 'ok':
            trade = response.json()['trades']
            return f'ok \nTrades: \n{trade}'
        else:
            error = response.json()['message']
            return f'failed \n{error}'
    else:
        return f'failed \n{response.json()}'


def nobitex_statistics(src_currency=None, dst_currency=None):
    # Return the latest NOBITEX market statistics.
    # src_currency : Source Currency
    # dst_currency : Destination Currency
    # Limitation : 100 requests per 10 minute.
    json = {
        "srcCurrency": src_currency,
        "dstCurrency": dst_currency
    }
    status_response, response = request(path='/market/stats', json=json)
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


def global_statistics(i=None):
    # Return the statistics of Binance and Kraken.
    # Limitation : 100 requests per 10 minute.
    del i
    status_response, response = request(path='/market/global-stats')
    if status_response:
        if response.status_code == 200 and response.json()['status'] == 'ok':
            market = response.json()['markets']
            return f'ok \nMarkets: \n{market}'
    else:
        return f'failed \n{response.json()}'


def login_attempts(token=None):
    # Return login history
    status_response, response = request(path='/users/login-attempts', token=token)
    if status_response:
        if response.status_code == 200 and response.json()['status'] == 'ok':
            attempt = response.json()['attempts']
            return f'ok \nLogin Attempts: \n{attempt}'
        else:
            error = response.json()['detail']
            return f'failed \n{error}'
    else:
        return f'failed \n{response.json()}'


def referral_code(token=None):
    # Return referral code.
    status_response, response = request(path='/users/get-referral-code', token=token)
    if status_response:
        if response.status_code == 200 and response.json()['status'] == 'ok':
            referral = response.json()['referralCode']
            return f'ok \nReferral Code: \n{referral}'
        else:
            error = response.json()['detail']
            return f'failed \n{error}'
    else:
        return f'failed \n{response.json()}'


def limitations(token=None):
    # Return your limitations in NOBITEX crypto exchange.
    status_response, response = request(path='/users/limitations', token=token)
    if status_response:
        if response.status_code == 200 and response.json()['status'] == "ok":
            limitation = response.json()['limitations']
            return f'ok \nLimitations: \n{limitation}'
        else:
            error = response.json()['detail']
            return f'failed \n{error}'
    else:
        return f'failed \n{response.json()}'


def wallets_list(token=None):
    # Return your own list of wallets.
    status_response, response = request(path='/users/wallets/list', token=token)
    if status_response:
        if response.status_code == 200 and response.json()['status'] == "ok":
            wallet = response.json()['wallets']
            return f'ok \nWallets: \n{wallet}'
        else:
            error = response.json()['detail']
            return f'failed \n{error}'
    else:
        return f'failed \n{response.json()}'


def wallets_balance(currency=None, token=None):
    # Return your wallet balance.
    # currency : The wallet you want like "btc" or 'ltc" etc.
    json = {
        'currency': currency
    }
    status_response, response = request(path='/users/wallets/balance', json=json, token=token)
    if status_response:
        if response.status_code == 200 and response.json()['status'] == "ok":
            balance = response.json()['balance']
            return f'ok \nBalance: \n{balance} {currency}'
        else:
            error = response.json()['detail']
            return f'failed \n{error}'
    else:
        return f'failed \n{response.json()}'

def transactions_list(wallet_ID):
    # Use this function to see your transactions history.
    # wallet_ID : ID of the wallet you want.
    wallet_ID = int(wallet_ID)
    open_token = open("token.txt", "r")
    token = open_token.read()
    header = {"Authorization": "Token " + token,
              "content-type": "application/json"}
    open_token.close()
    try:
        response = requests.post(
            url = URL + "/users/wallets/transactions/list",
            headers = header,
            json = {
                "wallet": wallet_ID
            }
        )
        response.raise_for_status()
        if response.status_code == 200:
            print(f"Your transactions list: \n{response.json()}")
            # print(response.status_code)
    except requests.exceptions.RequestException as error:
        if response.status_code == 401:
            print(f"ERROR! \nplease login then try again. \n{error}")
        else:
            print(f"ERROR! \n{error}")

def deposit_withdraw(wallet_ID):
    # Use this function to get a list of deposits and withdrawals.
    # wallet_ID : ID of the wallet you want.
    open_token = open("token.txt", "r")
    token = open_token.read()
    header = {"Authorization": "Token " + token,
              "content-type": "application/json"}
    open_token.close()
    try:
        response = requests.post(
            url = URL + "/users/wallets/deposits/list",
            headers = header,
            json = {
                "wallet": wallet_ID
            }
        )
        response.raise_for_status()
        if response.status_code == 200:
            print(f"List of deposits and withdrawals: \n{response.json()}")
            # print(response.status_code)
    except requests.exceptions.RequestException as error:
        if response.status_code == 401:
            print(f"ERROR! \nplease login then try again. \n{error}")
        else:
            print(f"ERROR! \n{error}")

def generate_address(wallet_ID):
    # Use this function to generate your block chain address.
    # wallet_ID : ID of the wallet you want.
    open_token = open("token.txt", "r")
    token = open_token.read()
    header = {"Authorization": "Token " + token,
              "content-type": "application/json"}
    open_token.close()
    try:
        response = requests.post(
            url = URL + "/users/wallets/generate-address",
            headers = header,
            json = {
                "wallet": wallet_ID
            }
        )
        response.raise_for_status()
        if response.status_code == 200:
            address = response.json()["address"]
            print(f"Your block chain address: \n{address}")
            # print(response.status_code)
    except requests.exceptions.RequestException as error:
        if response.status_code == 401:
            print(f"ERROR! \nplease login then try again. \n{error}")
        else:
            print(f"ERROR! \n{error}")

def order(type, srcCurrency, dstCurrency, amount, price, execution = "limit"):
    # Use this function to order.
    # type : "buy" or "sell"
    # srcCurrency : Source Currency
    # dstCurrency : Destination Currency
    # amount = The amount you want to buy.
    # price = Price to buy.
    # execution = "limit" or "market"
    # For quick order use word "market" for execution.
    # Limitation : 100 requests per 10 minutes.
    price = int(price)
    open_token = open("token.txt", "r")
    token = open_token.read()
    header = {"Authorization": "token " + token,
              "content-type": "application/json"}
    open_token.close()
    try:
        response = requests.post(
            url = URL + "/market/orders/add",
            headers = header,
            json = {
                "type": type,
                "execution": execution,
                "srcCurrency": srcCurrency,
                "dstCurrency": dstCurrency,
                "amount": amount,
                "price": price
            }
        )
        response.raise_for_status()
        if response.status_code == 200:
            print(f"Completed. \n{response.json()}")
            # print(response.status_code)
    except requests.exceptions.RequestException as error:
        if response.status_code == 401:
            print(f"ERROR! \nplease login then try again. \n{error}")
        else:
            print(f"ERROR! \n{error}")

def order_status(order_ID):
    # Use this function to get order status.
    # order_ID : Order ID
    # Limitation : 60 requests per minute.
    order_ID = int(order_ID)
    open_token = open("token.txt", "r")
    token = open_token.read()
    header = {"Authorization": "token " + token,
              "content-type": "application/json"}
    open_token.close()
    try:
        response = requests.post(
            url=URL + "/market/orders/add",
            headers=header,
            json={
                "id": order_ID
            }
        )
        response.raise_for_status()
        if response.status_code == 200:
            print(f"Order status: \n{response.json()}")
            # print(response.status_code)
    except requests.exceptions.RequestException as error:
        if response.status_code == 401:
            print(f"ERROR! \nplease login then try again. \n{error}")
        else:
            print(f"ERROR! \n{error}")

def update_status(order_ID, status):
    # Use this function to change order status.
    # order_ID : Order ID
    # status : "new" or "active" or "cancel
    # Limitation : 100 requests per 10 minutes.
    order_ID = int(order_ID)
    open_token = open("token.txt", "r")
    token = open_token.read()
    header = {"Authorization": "token " + token,
              "content-type": "application/json"}
    open_token.close()
    try:
        response = requests.post(
            url=URL + "/market/orders/add",
            headers=header,
            json={
                "order": order_ID,
                "status": status
            }
        )
        response.raise_for_status()
        if response.status_code == 200:
            print(f"Order status changed. \n{response.json()}")
            # print(response.status_code)
    except requests.exceptions.RequestException as error:
        if response.status_code == 401:
            print(f"ERROR! \nplease login then try again. \n{error}")
        else:
            print(f"ERROR! \n{error}")

def order_cancel(srcCurrency, dstCurrency, hours, execution = "market"):
    # Use this function to cancel order.
    # srcCurrency : Source Currency
    # dstCurrency : Destination Currency
    # hours : To determine the time period you want to cancel its orders.
    # execution = "limit" or "market"
    hours = float(hours)
    open_token = open("token.txt", "r")
    token = open_token.read()
    header = {"Authorization": "token " + token,
              "content-type": "application/json"}
    open_token.close()
    try:
        response = requests.post(
            url=URL + "/market/orders/cancel-old",
            headers=header,
            json={
                "execution": execution,
                "srcCurrency": srcCurrency,
                "dstCurrency": dstCurrency,
                "hours": hours
            }
        )
        response.raise_for_status()
        if response.status_code == 200:
            print(f"Completed. \n{response.json()}")
            # print(response.status_code)
    except requests.exceptions.RequestException as error:
        if response.status_code == 401:
            print(f"ERROR! \nplease login then try again. \n{error}")
        else:
            print(f"ERROR! \n{error}")

wallets_balance("btc", 'eeaa1200a7db1cdd42c2a7399054c1a38db3e36e')