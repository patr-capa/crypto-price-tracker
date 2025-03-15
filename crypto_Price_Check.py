import pandas as pd
from pycoingecko import CoinGeckoAPI
import time
from datetime import datetime
from email.message import EmailMessage
import smtplib
from dotenv import load_dotenv
import os

# Initialize CoinGecko API
cg = CoinGeckoAPI()

# Cryptos to track
CRYPTOS = ["bitcoin", "ethereum", "solana", "chainlink", "polkadot", "ripple", "cardano", "dogecoin", "vechain"]
OUTPUT_FILE = "crypto_price_log.xlsx"

# Track last prices for percentage change calculation
last_prices = {}

def fetch_crypto_prices():
    """Fetch live crypto prices from CoinGecko."""
    try:
        prices = cg.get_price(ids=CRYPTOS, vs_currencies='usd')
        return {crypto: prices.get(crypto, {}).get('usd', 'N/A') for crypto in CRYPTOS}
    except Exception as e:
        print(f"❌ Error fetching data: {e}")
        return {}

def log_prices():
    """Log crypto prices to an Excel file and calculate percentage change."""
    global last_prices

    data = []
    prices = fetch_crypto_prices()
    timestamp = datetime.now().strftime("%Y-%m-%d %H:%M:%S")

    for crypto, price in prices.items():
        last_price = last_prices.get(crypto)
        if last_price and isinstance(price, (int, float)):
            change = ((price - last_price) / last_price) * 100
            change_str = f"{change:+.5f}"
        else:
            change_str = "N/A"

        data.append([timestamp, crypto, f"{price:.5f}", change_str])

    # Create or append data to Excel file
    try:
        df = pd.DataFrame(data, columns=["Timestamp", "Crypto", "Price (USD)", "Change (%)"])

        # Try to append to existing file if it exists
        try:
            existing_df = pd.read_excel(OUTPUT_FILE, engine="openpyxl")
            df = pd.concat([existing_df, df], ignore_index=True)

            # Remove duplicates and limit to last 500 entries
            df.drop_duplicates(subset=["Timestamp", "Crypto"], keep="last", inplace=True)
            df = df.tail(500)   # Keep only last 500 entries

        except FileNotFoundError:
            pass

        df.to_excel(OUTPUT_FILE, index=False, engine="openpyxl")
        print(f"Logged prices at {timestamp}")

    except Exception as e:
        print(f"❌ Error writing to file: {e}")

    # Return the fetched prices for display
    return prices

def send_email():
    load_dotenv()

    EMAIL_USER = os.getenv("EMAIL_USER")
    EMAIL_PASSWORD = os.getenv("EMAIL_PASS")

    if not EMAIL_USER or not EMAIL_PASSWORD:
        print("❌ Missing email credentials in .env file.")
        return

    msg = EmailMessage()
    msg['Subject'] = 'Crypto Price Report'
    msg['From'] = EMAIL_USER
    msg['To'] = EMAIL_USER
    msg.set_content("Attached is the latest crypto price report")

    # Attach the Excel file
    try:
        with open(OUTPUT_FILE, 'rb') as f:
            file_data = f.read()
            file_name = OUTPUT_FILE
            msg.add_attachment(file_data, maintype='application', subtype='octet-stream', filename=file_name)

        # Send the email
        with smtplib.SMTP_SSL('smtp.gmail.com', 465) as server:
            server.login(EMAIL_USER, EMAIL_PASSWORD)
            server.send_message(msg)

        print("✅ Email sent successfully!")

    except Exception as e:
        print(f"❌ Error sending email: {e}")

def main():
    """Main loop to pull and log prices.
    Press a key on the keyboard to stop logging and send off an email with the crypto price log"""

    try:
        while True:
            prices = log_prices()
            timestamp = (f"{datetime.now().strftime('%Y-%m-%d %H:%M:%S')} - Current Prices:")

            # Print formatted prices
            print("\n" + "=" *40)
            print(f"{timestamp} - Crypto Prices:")
            print("-" * 40)

            for crypto, price in prices.items():
                last_price = last_prices.get(crypto)
                change = ((price - last_price) / last_price) * 100 if last_price else None

                change_str = f"{change:+.5f}%" if change is not None else "N/A"

                print(f"{crypto.capitalize():<10} | ${price:<10.5f} | Change: {change_str}")
                print(f"Raw values - Price: {price}, Last Price: {last_price}")

            print("=" * 40)

            # Update last price
            last_prices.update(prices)

            time.sleep(max(60, 65 - datetime.now().second))  # sleep for a minimum of 1 min

    except KeyboardInterrupt:
        print("\nScript is stopping. Sending email report...")
        send_email()
        print("\nEmail sent!")

if __name__ == "__main__":
    main()