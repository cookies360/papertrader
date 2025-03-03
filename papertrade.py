import json
import os
#import requests
import yfinance as yf

# Constants

#API_KEY = "2V5PJO3K35LOH0G6"
PORTFOLIO_FILE = "portfolio.json"
STARTING_BALANCE = 1000000
#API_URL = "https://www.alphavantage.co/query"

if not os.path.exists(PORTFOLIO_FILE):
    # If the file doesn't exist, create it with some initial structure
    data = {}
    with open(PORTFOLIO_FILE, 'w') as file:
        json.dump(data, file, indent=4)
else:
    # If the file exists, load the data
    with open(PORTFOLIO_FILE, 'r') as file:
        data = json.load(file)

def save_to_file(data):
    json_object = json.dumps(data, indent=4)
    with open(str(PORTFOLIO_FILE), "w") as outfile:
        outfile.write(json_object)
    
def update_balance():
    balence = STARTING_BALANCE
    for stock, info in data.items():
        balence=balence-(info["spent"])
    return balence

def update_stock_data():
    for key in data:
        ticker = yf.Ticker(key)
        market_price = ticker.info['regularMarketPrice']
        data[key]['worth'] = market_price*data[key]['stock_num']
        data[key]['price'] = market_price

        if data[key]['tspent'] < 0 or data[key]['stock_num'] == 0:
            data[key]['tspent'] = 0
        
        save_to_file(data)

def buy_sell(stock_num, choice, name):
    if choice == "buy":
        ticker = yf.Ticker(name)
        market_price = ticker.info['regularMarketPrice']

        if update_balance()<=market_price*stock_num:
            print('you dont have the money')
            main()
        
        if name not in data:
            # If the key does not exist, add it with the desired structure
            data[name] = {'price': 0, 'worth': 0, 'spent': 0, 'stock_num': 0, 'tspent': 0}


        # Update the price for the specified item
        data[name]['price'] = market_price
        data[name]['spent'] = data[name]['spent']+market_price*stock_num
        data[name]['tspent'] = data[name]['tspent']+market_price*stock_num
        data[name]['stock_num'] = data[name]['stock_num']+stock_num
        
        save_to_file(data)
    
    if choice == "sell":
        ticker = yf.Ticker(name)
        market_price = ticker.info['regularMarketPrice']
    
        if data[name]['stock_num']-int(stock_num)<0:
            print('you dont have enough stocks')
            main()
        else:
            data[name]['spent'] = data[name]['spent']-int(market_price*stock_num)
            data[name]['tspent'] = data[name]['tspent']-int(market_price*stock_num)
            data[name]['stock_num'] = data[name]['stock_num']-int(stock_num)

            save_to_file(data)


def sell():
    name=input("What stock do you want to sell: ")
    stock_num=input("How much: ")
    buy_sell(int(stock_num), "sell", str(name))

def portfolio():
    update_stock_data()
    totalspent=0
    totalworth=0
    for key in data:
        if data[key]['stock_num'] == 0:
            pass
        else:
            print("~~~~~~~~~~")
            print(key+":")
            print("The total worth: "+str(data[key]['worth']))
            print("The current price: "+str(data[key]['price']))
            print("The amount spent: "+str(data[key]['tspent']))
            print("Stocks you own: "+str(data[key]['stock_num']))
            print("~~~~~~~~~~")

            totalspent+=int(data[key]['tspent'])
            totalworth+=int(data[key]['worth'])

    print("Loss/Gained: "+str(totalworth-totalspent))


def buy():
    name=str(input("What stock do you want: "))
    stock_num=int(input("How much: "))
    buy_sell(int(stock_num), "buy", str(name))


def main():
    """Main menu loop."""
    while True:
        if data != {}:
            print("")
            print("Amount of Money: " + str(update_balance()))
        print("\nStock Portfolio Manager")
        print("1: View Portfolio")
        print("2: Buy Stocks")
        print("3: Sell Stocks")
        print("4: Exit")
        choice = input("Choose an option: ")
        
        if choice == "1":
            portfolio()
            
        elif choice == "2":
            buy()
            
        elif choice == "3":
            sell()
            
        elif choice == "4":
            print("Alright, bye.")
            break
        else:
            print("Pick a real option.")

main()