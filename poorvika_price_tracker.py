from bs4 import BeautifulSoup
from selenium import webdriver
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from webdriver_manager.chrome import ChromeDriverManager



products_to_track = [
    {
        "product_url": "https://www.poorvika.com/apple-iphone-16-pro-max-desert-titanium-1tb/p",
        "name": "iPhone 16 pro max",
        "target_price": 165000
    },
    {
        "product_url": "https://www.poorvika.com/apple-iphone-15-plus-blue-128gb/p",
        "name": "iPhone 15 plus",
        "target_price": 80000
        
    },
     {
        "product_url": "https://www.poorvika.com/samsung-galaxy-s24-ultra-5g-titanium-yellow-512gb-12gb-ram/p",
        "name": "Samsung Galaxy S24  ultra ",
        "target_price": 140000
        
    },
       {
        "product_url": "https://www.poorvika.com/samsung-galaxy-s25-ultra-5g-titanium-black-256gb-12gb-ram/p",
        "name": "Samsung Galaxy S25  ultra ",
        "target_price": 125000
        
    },
       {
        "product_url": "https://www.poorvika.com/nothing-phone-2a-5g-blue-128gb-8gb-ram/p",
        "name": "Nothing 2a ",
        "target_price": 25000
        
    },
]





def give_product_price(URL):
    options = webdriver.ChromeOptions()
    options.add_argument('headless')
    options.add_argument('window-size=1920x1080')

    driver = webdriver.Chrome(service=Service(ChromeDriverManager().install()), options=options)
    driver.get(URL)

    try:
        
        price_element = WebDriverWait(driver, 10).until(
            EC.presence_of_element_located((By.CLASS_NAME, "center-content_price_special__LGEjP"))
        )
        soup = BeautifulSoup(driver.page_source, 'html.parser')

    
        price_tag = soup.find('div', class_='center-content_price_special__LGEjP').find('b')

        product_price = price_tag.get_text().strip() if price_tag else "Price not found"
    except Exception as e:
        product_price = "Price not found"
    finally:
        driver.quit()

    return product_price

result_file = open('poorvika_result_file.txt', 'w')

try:
    for every_product in products_to_track:
        product_price_returned = give_product_price(every_product.get("product_url"))
        print(f"{every_product['name']} - {product_price_returned}")

        if product_price_returned and product_price_returned != "Price not found":
           
            my_product_price = product_price_returned.replace('₹', '').replace(',', '').strip()
            my_product_price = float(my_product_price)
            print(my_product_price)

            if my_product_price < every_product.get("target_price"):
                print("Available at your required price")
                result_file.write(f"{every_product['name']}\t- \tAvailable at target price\tCurrent price - {my_product_price}\n")
            else:
                print("Still at current price")
                result_file.write(f"{every_product['name']}- \tStill at current price\tCurrent price - {my_product_price}\n")
finally:
    result_file.close()
