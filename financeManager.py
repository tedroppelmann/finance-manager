import csv
import json
from typing import List
from category import Category
from paymentMethod import PaymentMethod
from sheetsConnection import SheetsConnection
from logger_config import get_logger
from transaction import Transaction
import datetime

logger = get_logger(__name__)

class FinanceManager:

	def __init__(self, bank_statement_path : str, keywords_path : str = None):
		self.keywords_path = keywords_path
		self.bank_statement_path = bank_statement_path

		self.transactions : List[Transaction] = []
		self.categories : List[Category] = []
		self.payment_methods : List[PaymentMethod] = []

		if keywords_path:
			self.__load_keywords()

	def __load_keywords(self):
		"""
		Loads the categories and payment methods from a JSON file.
		"""
		logger.info(f"Loading JSON file: {self.keywords_path}")
		with open(self.keywords_path, "r") as file:
			data = json.load(file)
			categories = data["categories"]
			payment_methods = data["payment_methods"]
			for category, keywords in categories.items():
				category_obj = Category(category, keywords)
				self.categories.append(category_obj)
			for payment_method, keywords in payment_methods.items():
				payment_method_obj = PaymentMethod(payment_method, keywords)
				self.payment_methods.append(payment_method_obj)

	def add_transactions(self, month : str, year : str):
		"""
		Reads the transactions from the bank statement file and adds them to the transactions list.
		"""
		logger.info("Reading transactions from file.")
		with open(self.bank_statement_path, "r", encoding="latin1") as file:
			csv_reader = csv.reader(file, delimiter=";")
			next(csv_reader, None) # Skip the header
			for row in csv_reader:
				try:
					date = row[5]  # DD/MM/YYYY
					description = row[6]
					amount = row[8]
					category = "Unknown"
					payment_method = "Unknown"
					transaction_date = datetime.datetime.strptime(date, "%d/%m/%Y")
					if transaction_date.strftime("%B").upper() == month and transaction_date.strftime("%Y") == year:
						amount = float(amount.replace(",", "."))
						self.transactions.append(Transaction(date, description, amount, category, payment_method))
				except Exception as e:
					logger.error(f"Error processing row: {row} - {e}")
		logger.info(f"Read {len(self.transactions)} transactions.")

		if self.keywords_path:
			self.__update_transactions()

	def __update_transactions(self):
		"""
		Updates the payment method and category of each transaction based on the keywords.
		"""
		logger.info("Updating transactions with keywords from JSON file.")
		for transaction in self.transactions:
			transaction.update_payment_method(self.payment_methods)
			transaction.update_category(self.categories)

	def check_unknown_categories(self):
		"""
		Checks if there are any transactions with unknown categories and updates them manually.
		"""
		logger.info("Checking for unknown categories.")
		for transaction in self.transactions:
			if transaction.category == "Unknown":
				has_new_keyword = transaction.update_category_manually(self.categories)
				if has_new_keyword is True:
					self.__update_transactions()
				elif has_new_keyword is None:
					break
		self.__update_keywords_json()

	def update_google_sheet(self, credentials_file : str, month : str, year : str):
		"""
		Updates the Google Sheet with the transactions for the specified month and year.
		"""
		logger.info(f"Updating Google Sheet for {month}-{year}.")
		try:
			service = SheetsConnection(credentials_file)
			ws = service.get_worksheet("Expenses", f"{month}-{year}")
			service.fill_worksheet(ws, self.transactions)
		except Exception as e:
			logger.error(f"An error occurred while updating the Google Sheet: {e}")

	def __update_keywords_json(self):
		"""
		Updates the keywords JSON file with the new categories added manually.
		"""
		logger.info("Updating category keywords in JSON file.")
		with open(self.keywords_path, "r") as jsonFile:
			data = json.load(jsonFile)

		for category in self.categories:
			data["categories"][category.name] = category.keywords
			
		with open(self.keywords_path, "w") as jsonFile:
			json.dump(data, jsonFile, indent=4)

	def save_to_csv(self, output_file : str):
		"""
		Saves the clean transactions to a CSV file.
		"""
		logger.info(f"Saving transactions to CSV file: {output_file}")
		with open(output_file, "w", newline="") as file:
			csv_writer = csv.writer(file, delimiter=";")
			csv_writer.writerow(["Date", "Amount", "Category", "Payment Method", "Description"])
			for transaction in self.transactions:
				csv_writer.writerow([transaction.date, transaction.amount, transaction.category, transaction.payment_method, transaction.description])
