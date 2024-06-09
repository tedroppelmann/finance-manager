import gspread
import time
from typing import List
from transaction import Transaction
from logger_config import get_logger

logger = get_logger(__name__)

class SheetsConnection:

    def __init__(self, credentials : str):
        self.credentials = credentials
        self.service = self.start_service()
    
    def start_service(self):
        logger.info("Starting Google Sheets service.")
        try:
            return gspread.service_account(filename=self.credentials)
        except FileNotFoundError:
            logger.error("Credentials file not found.")
            raise Exception("Credentials file not found.")
    
    def get_worksheet(self, sheet_name : str, worksheet_name : str):
        logger.info(f"Getting worksheet '{worksheet_name}' from spreadsheet '{sheet_name}'.")
        try:
            gc = self.service.open(sheet_name)
        except gspread.SpreadsheetNotFound:
            logger.error(f"Spreadsheet with name '{sheet_name}' not found.")
            raise Exception(f"Spreadsheet with name '{sheet_name}' not found.")
        
        try:
            ws = gc.worksheet(worksheet_name)
        except gspread.WorksheetNotFound:
            ws = gc.add_worksheet(worksheet_name, 1, 1)
        
        return ws
    
    def fill_worksheet(self, worksheet : gspread.Worksheet, transactions : List[Transaction]):
        logger.info("Filling worksheet.")
        if worksheet.row_count <= 1:
            self.add_titles(worksheet)
            for transaction in transactions:
                self.add_transaction(worksheet, transaction)
            self.set_format(worksheet)
        else:
            logger.error("Worksheet already contains data.")
            raise Exception("Worksheet already contains data.")
        
    def add_titles(self, worksheet : gspread.Worksheet):
        worksheet.append_row(["Date", "Amount", "Category", "Payment Method", "Description"])
        time.sleep(2)

    def add_transaction(self, worksheet : gspread.Worksheet, transaction : Transaction):
        worksheet.append_row([transaction.date , transaction.amount, transaction.category, transaction.payment_method, transaction.description])
        time.sleep(2)
    
    def set_format(self, worksheet : gspread.Worksheet):
        worksheet.format("A1:E1", {'textFormat': {'bold': True}})
        time.sleep(2)
        worksheet.format("B:B", {'numberFormat': {'type': 'CURRENCY', 'pattern': '€#,##0.00'}})
