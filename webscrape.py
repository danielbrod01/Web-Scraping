from urllib.request import urlopen
from bs4 import BeautifulSoup as soup

# Store url of target page into my_url
my_url = 'https://www.newegg.com/Video-Cards-Video-Devices/Category/ID-38?Tpk=graphics%20card'

# Opening up connecting, grabbing the page
url_client = urlopen(my_url)
page_html = url_client.read()
url_client.close() # Closes

# html parsing
page_soup = soup(page_html, "html.parser")

# Grabs "container" for all products (graphics cards)
containers = page_soup.findAll("div",{"class":"item-container"})

# Set up csv file
file_name = "graphics_card_products.csv"
header_columns = "id, brand_name, product_name, price, shipping_price"
with open(file_name, 'w') as f:
    # Include header columns on first row of file
    f.write(header_columns + "\n")
    id = 0
    # For every product
    for container in containers:
        # Sets an id number
        id += 1
        # Gets brand name
        brand_container = container.find("div",{"class":"item-branding"})
        brand_name = brand_container.a.img["title"]

        # Gets product name
        product_container = container.find("a",{"class":"item-title"})
        product_name = product_container.text

        # Get product price
        price_container = container.find("li", {"class":"price-current"})
        price = price_container.strong.text + price_container.sup.text

        # Gets shipping price
        shipping_container = container.find("li",{"class":"price-ship"})
        shipping_price = shipping_container.text.strip()
        # Grabs the price digits in the string. "$3.99 shipping" --> "3.99"
        new_str = []
        for ch in shipping_price:
            if ch.isdigit() or ch == '.':
                new_str.append(str(ch))
        if new_str:
            shipping_price = ''.join(new_str)
        else:
            shipping_price = "0.00"

        # Write to file the product details for each row
        f.write(str(id) + "," + brand_name + "," + product_name.replace("," , "|") + "," + price + "," + shipping_price + "\n")
    # file closes automatically after the loop ends

# When file writing finishes
print(file_name + " file created!")
