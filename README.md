# Finance Manager

## Description

The Finance Manager project is designed to help you efficiently manage and track your personal finances. It provides a user-friendly interface for inputting income, expenses, and savings, and generates insightful reports and visualizations.

## Features

- Monthly finance tracking
- Categorization of transactions
- Export data to Google Sheets
- Report generation (work in progress)
- Visualization of financial data (work in progress)

## Installation
To install and run the Finance Manager application, follow these steps:

1. Clone the repository.
2. Install the required dependencies.
3. Run the application.

To run the application, execute the following command in your terminal:

```bash
python3 main.py
```

## Usage
To use the Finance Manager application effectively, follow these steps:

1. Add your transactions in .csv format. If necessary, modify the `financeManager.py` file. You can obtain this file from your bank.
2. If you want to categorize transactions by different payment methods, create a csv file with the corresponding keywords. For example:

```
"Apple Pay","APPLE PAY"
"Debit Card","DEBIT CARD"
"Direct Debit","DIRECT DEBIT"
"Bank Transfer","BANK TRANSFER","SENDING MONEY","CREDIT TRANSFER"
```

3. If you want to categorize transactions by expense, create a csv file with the corresponding keywords. For example:

```
"Groceries","CARREFOUR","LIDL","WALMART"
"Transport","METRO","UBER","LIME","TAXI","BLABLACAR","CARPOOL","CAR SHARING"
"Housing","REAL ESTATE","RENT"
"Personal care","GYM"
```

4. If you want to connect and store the data in Google Sheets, follow the instructions provided in the following link: [Google Sheets Integration](https://docs.gspread.org/en/latest/oauth2.html). After obtaining the necessary credentials, add the JSON file to the project.
5. Run the program.

