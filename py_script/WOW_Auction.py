from params import CLIENT_ID, CLIENT_SECRET, ACCESS_TOKEN, REALM_ID
import requests 
import logging
import time

logging.basicConfig(level=logging.DEBUG)

class AuctionClient:

	def __init__(self, access_token, realm_id):
		logging.info(">> Created an auction client.")
		self.realm_id = realm_id
		self.url = f"https://us.api.blizzard.com/data/wow/connected-realm/{realm_id}/auctions?namespace=dynamic-us&locale=en_US&access_token={access_token}"
	
	def get_data(self, limit=10):
		logging.info(">> Getting auction data...")
		response = requests.get(self.url).json()['auctions']

		# about 95000 records in "auctions" objects
		# 10 records for now due to oversize
		logging.info(f">> Done. We got {len(response)} records from realm_id {self.realm_id}.")
		return response[:limit]


	def run(self):
		while True:
			self.get_data()
			time.sleep(60 * 60)



client = AuctionClient(ACCESS_TOKEN, REALM_ID)
client.run()

