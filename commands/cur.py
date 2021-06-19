if len(text) == 4:
	amount = text[1];
	symbol = text[2].upper();
	convert = text[3].upper();
	if re.match(r"^[\d+]|[\d+\.\d+]?$", amount):
		if re.match(r"^[A-Z]{3,4}$", symbol):
			if re.match(r"^[A-Z]{3,4}$", convert):
				url = 'https://pro-api.coinmarketcap.com/v1/tools/price-conversion'
				headers = {
					'Accepts': 'application/json',
					'X-CMC_PRO_API_KEY': config.currency_apikey,
				}
				params = {
					'amount':amount,
					'symbol':symbol,
					'convert':convert
				}
				if symbol == "BYN":
					params = {
						'amount':amount,
						'id':3533,
						'convert':convert
					}
				if convert == "BYN":
					params = {
						'amount':amount,
						'symbol':symbol,
						'convert_id':3533
					}
				resp = requests.get(url=url, headers=headers, params=params)
				currency = json.loads(resp.text)
				if currency['status']['error_code'] == 0:
					update.message.reply_text(f"{currency['data']['amount']} {currency['data']['symbol']} = {round(currency['data']['quote'][convert]['price'], 2)} {convert}")
				else:
					if "symbol" in currency['status']['error_message']:
						update.message.reply_text(f"Валюта {symbol} не найдена")
					elif "convert" in currency['status']['error_message']:
						update.message.reply_text(f"Валюта {convert} не найдена")
					else:
						update.message.reply_text(f"Error {currency['status']['error_code']}: {currency['status']['error_message']}")
			else:
				update.message.reply_text(f"Валюта {convert} не найдена")
		else:
			update.message.reply_text(f"Валюта {symbol} не найдена")
	else:
		update.message.reply_text(f"Требуется количество в цифрах")
else:
	update.message.reply_text(f"Пример использования:\n/{command} <количество> <EUR/USD/RUB> <EUR/USD/RUB>")