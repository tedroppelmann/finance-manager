from financeManager import FinanceManager
from logger_config import get_logger
import settings # This import is necessary to access the settings variables. Create a settings.py file in the same directory as main.py and add the necessary variables.

# Change the month and year to the desired values
MONTH = "APRIL"
YEAR = "2024"

if __name__ == "__main__":
    logger = get_logger(__name__)
    logger.info("Starting finance manager.")

    finance_manager = FinanceManager()
    finance_manager.add_payment_methods(settings.PAYMENT_METHODS_PATH)
    finance_manager.add_categories(settings.KEYWORDS_PATH)
    finance_manager.add_transactions(settings.BANK_STATEMENT_PATH, MONTH, YEAR)
    finance_manager.update_transactions()
    # finance_manager.check_unknown_categories()
    # finance_manager.update_keywords_csv(settings.KEYWORDS_PATH)
    finance_manager.save_to_csv("output.csv")
    # finance_manager.update_google_sheet(settings.CREDENTIALS_PATH, MONTH, YEAR)

    logger.info("Finance manager finished.")