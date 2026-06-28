import requests
from bs4 import BeautifulSoup
import csv

try:
    response = requests.get("https://books.toscrape.com/", timeout=5)
    response.raise_for_status() #Raises an exception that will be caught by except block

    soup = BeautifulSoup(response.content, 'html.parser')
    books = soup.find_all('article', class_='product_pod')

    data = []
    for book in books[:10]:
        title = book.h3.a["title"]
        price = book.find("p", class_="price_color").text
        price = float(price.replace("£", ""))

        data.append({
            "Title": title,
            "Price": price
        })
# Error occurs when there is no internet connection found 
except requests.exceptions.ConnectionError:
    print("Error: Unable to connect, please check your internet")

# Timeout happens when the server takes too long to respond. We have set it as 5 seconds
except requests.exceptions.Timeout:
    print("Error: Request has timed out.")

# Error occurs when the server responds, but response indicates something went wrong.
except requests.exceptions.HTTPError:  
    print("Error: There is a HTTP Error")

# To catch any request related error
except requests.exceptions.RequestException as error:
    print("An unexpected error occurred:", error)


# Accessing the api key and currency url
api_key = "ad5361217bbbafb59d0a3dc5"
url = f"https://v6.exchangerate-api.com/v6/{api_key}/latest/GBP"

response_2 = requests.get(url)
exchange_data = response_2.json()

# Prompt the user to enter the currency of their choice
currency = input("Enter currency to convert: ").upper()
if currency in exchange_data["conversion_rates"]:
    rate = exchange_data["conversion_rates"][currency]
else:
    print("Not a valid currency code.")
    exit()

# To update the currency to a currency the user prefers
for book in data[:10]:
    book[f"Price_{currency}"] = round(book["Price"] * rate, 2)

    print(f"Title: {book['Title']}")
    print(f"Price in GBP: £{book['Price']}")
    print(f"Price ({currency}): Ksh{book[f"Price_{currency}"]}")
    print("-" * 20)

with open('books.csv', 'w') as file:
    writer = csv.writer(file)
    writer.writerow(["Title", "Price in GBP", f"Price in {currency}"])

    for book in data:
        writer.writerow([
            book['Title'], 
            book['Price'], 
            book[f"Price_{currency}"]
        ])

print("Books have been saved")

