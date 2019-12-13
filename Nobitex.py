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
            file = open('NobitexToken.txt', 'w')
            file.write(token)
            file.close()
            return f'Success \nToken: {token} \nYour token stored in NobitexToken.txt file.'
        elif response.status_code == 429:
            error = 'You need to log in with Iran\'s IP.'
            return error
        else:
            error = response.json()['non_field_errors']
            return 'failed', error
    else:
        return 'failed', response.json()


def profile():
    # Use this function to see your profile and personal information.
    open_token = open("token.txt", "r")
    token = open_token.read()
    header = {"Authorization": "Token " + token}
    open_token.close()
    try:
        response = requests.post(
            url=URL + "/users/profile",
            headers=header
        )
        response.raise_for_status()
        if response.status_code == 200:
            print(f"Profile: \n{response.json()}")
            # print(f"status code = {response.status_code}")
    except requests.exceptions.RequestException as error:
        if response.status_code == 401:
            print(f"ERROR! \nplease login then try again. \n{error}")
        else:
            print(f"ERROR! \n{error}")

def list_of_orders(type, srcCurrency = None, dstCurrency = "usdt", order = "-price"):
    # Use this function to get the list of orders.
    # The program shows the price from high to low by default.
    # For showing from low to high, word " price" should be entered for order variable.
    # type : "buy" or "sell"
    # srcCurrency : Source Currency
    # dstCurrency : Destination Currency
    header = {"content-type": "application/json/"}
    try:
        response = requests.post(
            url = URL + "/market/orders/list",
            headers = header,
            json = {
                "order": order,
                "type": type,
                "srcCurrency": srcCurrency,
                "dstCurrency": dstCurrency
            }
        )
        response.raise_for_status()
        if response.status_code == 200:
            print(f"List of Orders: \n{response.json()}")
            # print(f"status code = {response.status_code}")
    except requests.exceptions.RequestException as error:
        print(f"ERROR! \n{error}")

def list_of_trades(srcCurrency, dstCurrency, myTradesOnly = "no"):
    # Use this function to get the list of trades.
    # srcCurrency : Source Currency
    # dstCurrency : Destination Currency
    # myTradesOnly : Show personal trading list ("yes" or "no")
    # Limitation : 15 requests per minute.
    header = {"content-type": "application/json"}
    try:
        response = requests.post(
            url = URL + "/market/trades/list",
            headers = header,
            json = {
                "srcCurrency": srcCurrency,
                "dstCurrency": dstCurrency,
                "myTradesOnly": myTradesOnly
            }
        )
        response.raise_for_status()
        if response.status_code == 200:
            print(f"List of Trades: \n{response.json()}")
            # print(f"status code = {response.status_code}")
    except requests.exceptions.RequestException as error:
        print(f"ERROR! \n{error}")
def nobitex_statistics(srcCurrency, dstCurrency):
    # Use this function to get the latest NOBITEX market statistics.
    # srcCurrency : Source Currency
    # dstCurrency : Destination Currency
    # Limitation : 100 requests per 10 minute.
    header = {"content-type": "application/json"}
    try:
        response = requests.post(
            url = URL + "/market/stats",
            headers = header,
            json = {
                "srcCurrency": srcCurrency,
                "dstCurrency": dstCurrency
            }
        )
        response.raise_for_status()
        if response.status_code == 200:
            print(f"Nobitex Market Statistics: \n{response.json()}")
    except requests.exceptions.RequestException as error:
        print(f"ERROR! \n{error}")

def OHLC(symbol, resolution, from_, to):
    # symbol : جفت ارز
    # resolution : Candle Time Frame
    # from_ : The Beginning Time of The Interval
    # to : The Ending Time of The Interval
    from_ = int(from_)
    to = int(to)
    header = {"content-type": "application/json"}
    try:
        response = requests.post(
            url = URL + "/market/udf/history",
            headers = header,
            json = {
                "symbol": symbol,
                "resolution": resolution,
                "from": from_,
                "to": to
            }
        )
        response.raise_for_status()
        if response.status_code == 200:
            # print(response.status_code)
            print(response.json())
    except requests.exceptions.RequestException as error:
        print(f"ERROR! \n{error}")

def global_statistics():
    # Use this function to get the statistics of Binance and Kraken.
    # Limitation : 100 requests per 10 minute.
    try:
        response = requests.post(URL + "/market/global-stats")
        response.raise_for_status()
        if response.status_code == 200:
            print(f"World market statistics: \n{response.json()}")
    except requests.exceptions.RequestException as error:
        print(f"ERROR! \n{error}")

def login_attempts():
    # Use this function to get your login history
    open_token = open("token.txt", "r")
    token = open_token.read()
    header = {"Authorization": "Token " + token}
    open_token.close()
    try:
        response = requests.post(
            url=URL + "/users/login-attempts",
            headers = header
        )
        response.raise_for_status()
        if response.status_code == 200:
            print(f"Your login history: \n{response.json()}")
            # print(f"status code = {response.status_code}")
    except requests.exceptions.RequestException as error:
        if response.status_code == 401:
            print(f"ERROR! \nplease login then try again. \n{error}")
        else:
            print(f"ERROR! \n{error}")

def referral_code():
    # Use this function to get referral code.
    open_token = open("token.txt", "r")
    token = open_token.read()
    header = {"Authorization": "Token " + token}
    open_token.close()
    try:
        response = requests.post(
            url = URL + "/users/get-referral-code",
            headers = header
        )
        response.raise_for_status()
        if response.status_code == 200:
            print(f"Your referral code: \n{response.json()['referralCode']}")
            # print(f"status code = {response.status_code}")
    except requests.exceptions.RequestException as error:
        if response.status_code == 401:
            print(f"ERROR! \nplease login then try again. \n{error}")
        else:
            print(f"ERROR! \n{error}")

def add_card_number(card_number, bank_name):
    # Use this function to add bank card number.
    # card_number : Your card number.
    # bank_name : Name of the bank.
    # Limitation : 5 requests per hour.
    open_token = open("token.txt", "r")
    token = open_token.read()
    header = {"Authorization": "Token " + token,
              "content-type": "application/json"}
    open_token.close()
    try:
        response = requests.post(
            url=URL + "/users/cards-add",
            headers=header,
            json={
                "number": card_number,
                "bank": bank_name
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

def add_account_number(account_number, shaba_number, bank_name):
    # Use this function to add bank account number.
    # account_number : Your card number.
    # shaba_number : Shaba number of your bank account.
    # bank_name : Name of the bank.
    # Limitation : 5 requests per hour.
    open_token = open("token.txt", "r")
    token = open_token.read()
    header = {"Authorization": "Token " + token,
              "content-type": "application/json"}
    open_token.close()
    try:
        response = requests.post(
            url = URL + "/users/accounts-add",
            headers = header,
            json = {
                "number": account_number,
                "shaba": shaba_number,
                "bank": bank_name
            }
        )
        response.raise_for_status()
        if response.status_code == 200:
            print(f"Completed. \n{response.json()}")
            print(response.status_code)
    except requests.exceptions.RequestException as error:
        if response.status_code == 401:
            print(f"ERROR! \nplease login then try again. \n{error}")
        else:
            print(f"ERROR! \n{error}")

def limitations():
    # Use this function to see your limitations in NOBITEX crypto exchange.
    open_token = open("token.txt", "r")
    token = open_token.read()
    header = {"Authorization": "Token " + token}
    open_token.close()
    try:
        response = requests.post(
            url = URL + "/users/limitations",
            headers = header
        )
        response.raise_for_status()
        if response.status_code == 200:
            print(f"Your limitations according to your authentication: \n{response.json()}")
            # print(f"status code = {response.status_code}")
    except requests.exceptions.RequestException as error:
        if response.status_code == 401:
            print(f"ERROR! \nplease login then try again. \n{error}")
        else:
            print(f"ERROR! \n{error}")

def wallets_list():
    # Use this function to see your own list of wallets.
    open_token = open("token.txt", "r")
    token = open_token.read()
    header = {"Authorization": "Token " + token}
    open_token.close()
    try:
        response = requests.post(
            url = URL + "/users/wallets/list",
            headers = header
        )
        response.raise_for_status()
        if response.status_code == 200:
            print(f"Your wallets list: \n{response.json()}")
            # print(f"status code = {response.status_code}")
    except requests.exceptions.RequestException as error:
        if response.status_code == 401:
            print(f"ERROR! \nplease login then try again. \n{error}")
        else:
            print(f"ERROR! \n{error}")

def wallets_balance(currency):
    # Use this function to get your wallet balance.
    # currency : The wallet you want like "btc" or 'ltc" etc.
    open_token = open("token.txt", "r")
    token = open_token.read()
    header = {"Authorization": "Token " + token,
              "content-type": "application/json"}
    open_token.close()
    try:
        response = requests.post(
            url = URL + "/users/wallets/balance",
            headers = header,
            json = {
                "currency": currency
            }
        )
        response.raise_for_status()
        if response.status_code == 200:
            print(f"Your wallet balance: \n{response.json()['balance']} {currency}")
            # print(response.status_code)
    except requests.exceptions.RequestException as error:
        if response.status_code == 401:
            print(f"ERROR! \nplease login then try again. \n{error}")
        else:
            print(f"ERROR! \n{error}")

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

print(login('miladazami120@gmail.com', 'Sa3257121600', True))

