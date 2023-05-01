import bs4
import sys
import time
from twilio.rest import Client
from twilio.base.exceptions import TwilioRestException
from selenium import webdriver
from selenium.common.exceptions import NoSuchElementException, ElementNotInteractableException, TimeoutException
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.common.by import By
from selenium.webdriver.firefox.options import Options
from webdriver_manager.firefox import GeckoDriverManager
from datetime import datetime

# Twilio configuration
toNumber = '19282666610'
fromNumber = '17609194387'
accountSid = 'AC4779e92e9bac789220ebdef983bccfba'
authToken = '27e386bb1abd2a77e85d564826d30adf'
client = Client(accountSid, authToken)

#other vars
cvvNum = '090'
BestBuyPass = 'FzkSnJn+E%k4.Ec'


# Product Page (By default, This URL will scan all RTX 3070 and 3080's at one time.)
# 3080 and 3070 url = 'https://www.bestbuy.com/site/searchpage.jsp?_dyncharset=UTF-8&id=pcat17071&iht=y&keys=keys&ks=960&list=n&qp=gpusv_facet%3DGraphics%20Processing%20Unit%20(GPU)~NVIDIA%20GeForce%20RTX%203070%5Egpusv_facet%3DGraphics%20Processing%20Unit%20(GPU)~NVIDIA%20GeForce%20RTX%203080&sc=Global&st=rtx%203080%203070&type=page&usc=All%20Categories'
#ethernet url url = 'https://www.bestbuy.com/site/searchpage.jsp?st=ethernet&_dyncharset=UTF-8&_dynSessConf=&id=pcat17071&type=page&sc=Global&cp=1&nrp=&sp=&qp=&list=n&af=true&iht=y&usc=All+Categories&ks=960&keys=keys'
url = 'https://www.bestbuy.com/site/searchpage.jsp?st=3060+ti&_dyncharset=UTF-8&_dynSessConf=&id=pcat17071&type=page&sc=Global&cp=1&nrp=&sp=&qp=&list=n&af=true&iht=y&usc=All+Categories&ks=960&keys=keys'
def timeSleep(x, driver):
    if (x != 0):
        for i in range(x, -1, -1):
            sys.stdout.write('\r')
            sys.stdout.write('{:2d} seconds'.format(i))
            sys.stdout.flush()
            time.sleep(1)
    driver.refresh()
    sys.stdout.write('\r')
    sys.stdout.write('Page refreshed\n')
    sys.stdout.flush()


def createDriver():
   """Creating driver."""
   options = Options()
   options.headless = True # Change To False if you want to see Firefox Browser Again.
   profile = webdriver.FirefoxProfile(r'C:\Users\salte\AppData\Roaming\Mozilla\Firefox\Profiles\zcvnzel9.default-release')
   driver = webdriver.Firefox(profile, options=options, executable_path=GeckoDriverManager().install())
   return driver


def driverWait(driver, findType, selector):
   """Driver Wait Settings."""
   while True:
       if findType == 'css':
           try:
               driver.find_element_by_css_selector(selector).click()
               break
           except NoSuchElementException:
               driver.implicitly_wait(0.2)
       elif findType == 'name':
           try:
               driver.find_element_by_name(selector).click()
               break
           except NoSuchElementException:
               driver.implicitly_wait(0.2)


def findingCards(driver):
    """Scanning all cards."""
    success = False
    while(success != True):
        try:
            driver.get(url)
            success = True
            print("page loaded")
            html = driver.page_source
        except:
            driver.close()
            driver.quit()
            driver.stop_client()
            driver = createDriver()
            print("failed to get url, made new driver")
            
    soup = bs4.BeautifulSoup(html, 'html.parser')
    wait = WebDriverWait(driver, 15)
    wait2 = WebDriverWait(driver, 2)
    try:
        findAllCards = soup.find('button', {'class': 'btn btn-primary btn-sm btn-block btn-leading-ficon add-to-cart-button'})
        if findAllCards:
            print(f'Button Found!: {findAllCards.get_text()}')

            # Clicking Add to Cart.
            driverWait(driver, 'css', '.add-to-cart-button')

            # Going To Cart.
            driver.get('https://www.bestbuy.com/cart')

            # Checking if item is still in cart.
            try:
                wait.until(EC.presence_of_element_located((By.XPATH, "//*[@class='btn btn-lg btn-block btn-primary']")))
                driver.find_element_by_xpath("//*[@class='btn btn-lg btn-block btn-primary']").click()
                print("Item Is Still In Cart.")
            except (NoSuchElementException, TimeoutException):
                print("Item is not in cart anymore. Restarting...")
                return 0

            # Logging Into Account.
            print("Attempting to Login.")
            try:
                wait.until(EC.presence_of_element_located((By.XPATH, "//*[@class= 'btn btn-secondary btn-lg btn-block btn-leading-ficon c-button-icon c-button-icon-leading cia-form__controls__submit ']")))
                passwordF = driver.find_element_by_id("fld-p1")
                passwordF.send_keys(BestBuyPass)
                driver.find_element_by_xpath("//*[@class= 'btn btn-secondary btn-lg btn-block btn-leading-ficon c-button-icon c-button-icon-leading cia-form__controls__submit ']").click()
                print("logged in")
            except (NoSuchElementException, TimeoutException):
                print("Login click failed")
                return 0

            # Click Shipping Option. (If Available)
            try:
                wait.until(EC.presence_of_element_located((By.CSS_SELECTOR, "#fulfillment_1losStandard0")))
                time.sleep(1)
                driverWait(driver, 'css', '#fulfillment_1losStandard0')
                print("Clicking Shipping Option.")
                driver.find_element_by_css_selector("#fulfillment_1losStandard0")
            except (NoSuchElementException, TimeoutException):
                pass

            # Trying CVV
            try:
                print("\nTrying CVV Number.\n")
                security_code = driver.find_element_by_id("credit-card-cvv")
                time.sleep(1)
                security_code.send_keys(cvvNum)  # You can enter your CVV number here.
            except (NoSuchElementException, TimeoutException):
                pass

            # Bestbuy Text Updates.
            #try:
             #   wait2.until(EC.presence_of_element_located((By.CSS_SELECTOR, "#text-updates")))
              #  driverWait(driver, 'css', '#text-updates')
               # print("Selecting Text Updates.")
            #except (NoSuchElementException, TimeoutException):
             #   pass

            # Final Checkout.
            try:
                wait2.until(EC.presence_of_element_located((By.CSS_SELECTOR, ".btn-primary")))
                driverWait(driver, 'css', '.btn-primary')
            except (NoSuchElementException, TimeoutException, ElementNotInteractableException):
                try:
                    wait2.until(EC.presence_of_element_located((By.CSS_SELECTOR, ".btn-secondary")))
                    driverWait(driver, 'css', '.btn-secondary')
                    timeSleep(1, driver)
                    wait2.until(EC.presence_of_element_located((By.CSS_SELECTOR, ".btn-primary")))
                    driverWait(driver, 'css', '.btn-primary')
                except (NoSuchElementException, TimeoutException, ElementNotInteractableException):
                    print("Could Not Complete Checkout.")
                    return 0

            # Completed Checkout.
            print('Order Placed!')
            try:
                client.messages.create(to=toNumber, from_=fromNumber, body='ORDER PLACED!')
            except (NameError, TwilioRestException):
                pass
            return 1
        else:
            return 0

    except (NoSuchElementException, TimeoutException):
        return 0


if __name__ == '__main__':
   driver = createDriver()
   purch = 0
   #currentTime = time.time()
   while(purch < 5):
      purch += findingCards(driver)
      print(purch)
      #print(currentTime - time.time())
      #currentTime = time.time()

