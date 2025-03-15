Crypto Price Tracker by Patrick Capano

Description:
	Crypto Price Tracker is a Python script that fetches live cryptocurrency prices from CoinGecko, logs them to an Excel file, and calculates percentage changes over time. 
	It also includes an option to automatically email the log file for easy tracking and analysis.

Features:
	✅ Fetch live crypto prices for selected coins using CoinGecko
	✅ Log data to an Excel file with timestamp
	✅ Calculate and display percentage change
	✅ Email the log file for easy sharing and tracking
	✅ Clean and limit data to the last 500 entries

Setup:
	Clone the repository:
		git clone https://github.com/patr-capa/crypto-price-tracker.git

	Navigate to the project folder:
		cd crypto-price-tracker

	Create and activate a virtual environment:
		python -m venv venv
		source venv/bin/activate   # On Windows use `.\venv\Scripts\activate`

	Install dependencies
		See below for lsit of dependencies

	Create a .env file and add your email credentials:
		EMAIL_USER=your-email@gmail.com  
		EMAIL_PASS=your-email-password  

Usage:
	Run the script:
		crypto_price_tracker.py

	Stop the script using CTRL + C to automatically send the email report.

Configuration:
	You can modify the list of tracked cryptocurrencies by changing the CRYPTOS list in crypto_price_tracker.py:
		CRYPTOS = ["bitcoin", "ethereum", "solana", "chainlink", "polkadot", "ripple", "cardano"]

Dependencies
	pandas
	pycoingecko
	python-dotenv
	openpyxl
	smtplib

Future Improvements:
	Add more detailed error handling
	Create a simple web-based or GUI display for easier tracking
	Add support for additional exchanges and currencies

License
	This project is open-source under the MIT License.
