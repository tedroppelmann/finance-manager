from typing import List
from category import Category
from logger_config import get_logger 
import time
from paymentMethod import PaymentMethod

logger = get_logger(__name__)

class Transaction:

	def __init__(self, date : str, description : str, amount : float, category : str, payment_method : str):
		self.date = date
		self.description = description
		self.amount = amount
		self.category = category
		self.payment_method = payment_method

	def update_payment_method(self, payment_methods : List[PaymentMethod]):
		for payment_method in payment_methods:
			if payment_method.check_keywords_in_text(self.description):
				self.payment_method = payment_method.name

	def update_category(self, categories : List[Category]):
		for category in categories:
			if category.check_keywords_in_text(self.description):
				self.category = category.name
	
	def update_category_manually(self, categories : List[Category]):
		print("#"*50)
		print("Unknown category for the following transaction:")
		print(f"Transaction: {self.description}")
		print(f"Amount: {self.amount} €")
		print(f"Date: {self.date}")
		print("Choose a category from the list:")
		for i, category in enumerate(categories):
			print(f"{i+1}. {category.name}")
		print(f"{len(categories) + 1}. Keep as Unknown")
		while True:
			choice = input("Enter the number of the category (Press Enter to keep it Unknown): ")
			if choice.isdigit() and 1 <= int(choice) <= len(categories):
				self.category = categories[int(choice)-1].name
				self.add_keyword_manually(categories, choice)
				break
			elif not choice:
				break
			else:
				print("Invalid choice. Category not updated.")
		logger.info(f"Transaction categorized as {self.category} manually.")
		time.sleep(1)
	
	def add_keyword_manually(self, categories : List[Category], choice : str):
		keyword = input("Would you like to add a keyword to the category? (Press Enter to skip)")
		if keyword:
			keyword = keyword.upper()
			categories[int(choice)-1].add_keyword(keyword)
			logger.info(f"Keyword '{keyword}' added to category '{categories[int(choice)-1].name}'.")

