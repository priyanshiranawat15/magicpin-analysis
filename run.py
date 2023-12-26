import requests
from bs4 import BeautifulSoup

url = "https://magicpin.in/New-Delhi/Paharganj/Restaurant/Eatfit/store/61a193/delivery/"

# Send a GET request to the URL
response = requests.get(url)

# Check if the request was successful (status code 200)
if response.status_code == 200:
    # Parse the HTML content of the page
    soup = BeautifulSoup(response.content, 'html.parser')

    # Find the menu section
    menu_section = soup.find('div', class_='categoryListing')

    if menu_section:
        # Extract food items and their prices
        sub_menu = soup.find_all()
        for menu_item in sub_menu:
            # Extract the list of the food item
            food_item = menu_item.find_all('categoryItemHolder')

            if food_item:
                for item in food_item:

                    food_name = item.find('p', _class='itemName').text.strip()
                    food_price = item.find('span', _class='itemPrice').text.strip()
                    
                    print(f"Food: {food_name}, Price: {food_price}")
            else:
                print("Food items not found on this page")
    else:
        print("Menu section not found on the page.")
else:
    print(f"Failed to retrieve the page. Status Code: {response.status_code}")
