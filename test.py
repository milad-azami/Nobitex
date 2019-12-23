from Nobitex import Nobitex

n = Nobitex(testnet=True)
res = n.login(username="xanarahmanitest@gmail.com", password='3850240479xana', remember=True)
print(res.get('status'), res.get('error') or res.get('token'))
