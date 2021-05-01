from flask import Flask, render_template, request, redirect, url_for, abort, Response, send_file
from blizzard_api import *
import redis
import threading

def updateWowTokenPrice():
	global wow_token_price
	t = threading.Timer(30.0, updateWowTokenPrice)
	t.setDaemon(True)
	t.start()
	wow_token_price = getCurrentWowTokenPrice()

	if redis_cli.hset(name="token_price", mapping=wow_token_price):
		print("Updated Wow token price to redis")

def updateActiveAuctions():
	global auction_list
	t = threading.Timer()
	
app = Flask(__name__)
wow_token_price = None
auction_list = []
pool = redis.ConnectionPool(host='localhost', port=6379, decode_responses=True)
redis_cli = redis.Redis(connection_pool=pool)

updateWowTokenPrice()

@app.route("/wowtoken", methods=["GET"])
def token():
	price, timestamp = redis_cli.hmget("token_price", "price", "last_updated_timestamp")
	return render_template("index.html", content=wow_token_price)

@app.route("/auctions", methods=["GET"])
def auctions():
	#print(auctions)
	return render_template("index.html", content=auction_list)

if __name__ == "__main__":
	app.run(debug=True)