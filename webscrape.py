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

# Grabs each product (graphics card)
containers = page_soup.findAll("div",{"class":"item-container"})
file_name = "graphics_card_products.csv"
header_columns = "brand_name, product_name, shipping_price"
with open(file_name, 'w') as f:
    f.write(header_columns + "\n")
    for container in containers:
        brand_container = container.find("div",{"class":"item-branding"})
        brand_name = brand_container.a.img["title"]

        title_container = container.find("a",{"class":"item-title"})
        product_name = title_container.text

        shipping_container = container.find("li",{"class":"price-ship"})
        shipping_price = shipping_container.text.strip()

        print(brand_name)
        print(product_name)
        print(shipping_price + "\n")

        f.write(brand_name + "," + product_name.replace("," , "|") + "," + shipping_price + "\n")
