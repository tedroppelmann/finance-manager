from financeManager import FinanceManager
from logger_config import get_logger
import settings # This import is necessary to access the settings variables. Create a settings.py file in the same directory as main.py and add the necessary variables.

# Change the month and year to the desired values
MONTH = "APRIL"
YEAR = "2024"

if __name__ == "__main__":
    logger = get_logger(__name__)
    logger.info("Starting finance manager.")

    finance_manager = FinanceManager(settings.BANK_STATEMENT_PATH, settings.PAYMENT_METHODS_PATH, settings.KEYWORDS_PATH)

    # Set the transactions
    finance_manager.add_transactions(MONTH, YEAR)

    # Check for unknown categories (comment this line if you don't want to update the categories manually)
    finance_manager.check_unknown_categories()

    # Export the transactions to a CSV file and update the Google Sheet (comment this line if you don't want export 
    # the transactions to a CSV file or update the Google Sheet)
    finance_manager.save_to_csv("output.csv")
    finance_manager.update_google_sheet(settings.CREDENTIALS_PATH, MONTH, YEAR)

    logger.info("Finance manager finished.")