import bs4
import sys
import time
from selenium import webdriver
from selenium.common.exceptions import NoSuchElementException
from twilio.rest import Client
from selenium.webdriver.firefox.options import Options
from webdriver_manager.firefox import GeckoDriverManager
from twilio.base.exceptions import TwilioRestException

# Amazon credentials
username = 'salter10@msn.com'
password = 'w"dL4=^s2:Er7pJ'

# Twilio configuration
toNumber = '19282666610'
fromNumber = '17609194387'
accountSid = 'AC4779e92e9bac789220ebdef983bccfba'
authToken = '27e386bb1abd2a77e85d564826d30adf'
client = Client(accountSid, authToken)


def timeSleep(x, driver):
   for i in range(x, -1, -1):
       sys.stdout.write('\r')
       sys.stdout.write('{:2d} seconds'.format(i))
       sys.stdout.flush()
       time.sleep(1)
   try:
      driver.refresh()
   except Exception as e:
       print(e)
       timeSleep(x, driver)
   sys.stdout.write('\r')
   sys.stdout.write('Page refreshed\n')
   sys.stdout.flush()


def createDriver():
   """Creating driver."""
   options = Options()
   options.headless = False  # Change To False if you want to see Firefox Browser Again.
   profile = webdriver.FirefoxProfile(
       r'C:\Users\salte\AppData\Roaming\Mozilla\Firefox\Profiles\zcvnzel9.default-release')
   driver = webdriver.Firefox(profile, options=options, executable_path=GeckoDriverManager().install())
   return driver


def driverWait(driver, findType, selector):
   """Driver Wait Settings."""
   while True:
       if findType == 'css':
           try:
               driver.find_element_by_css_selector(selector).click();
               break
           except NoSuchElementException:
               driver.implicitly_wait(0.2)
       elif findType == 'name':
           try:
               driver.find_element_by_name(selector).click();
               break
           except NoSuchElementException:
               driver.implicitly_wait(0.2)

def tryGet(urlIn, driverIn):
    success = False
    attempts = 0
    while(success == False):
      try:
         driverIn.get(urlIn)
         success = True
         return True
      except Exception as e:
         print(e)
         time.sleep(1)
         attempts += 1
         if(attempts > 100):
            return False

def loginAttempt(driver):
   """Attempting to login Amazon Account."""
   
   tryGet('https://www.amazon.com/gp/sign-in.html', driver)
     
   try:
       usernameField = driver.find_element_by_css_selector('#ap_email')
       usernameField.send_keys(username)
       driverWait(driver, 'css', '#continue')
       passwordField = driver.find_element_by_css_selector('#ap_password')
       passwordField.send_keys(password)
       driverWait(driver, 'css', '#signInSubmit')
       time.sleep(2)
   except NoSuchElementException:
       pass
   return tryGet('https://www.amazon.com/stores/GeForce/RTX3080_GEFORCERTX30SERIES/page/6B204EA4-AAAC-4776-82B1-D7C3BD9DDC82',driver)


def findingCards(driver):
   """Scanning all cards."""
   while True:
       time.sleep(1)
       html = driver.page_source
       soup = bs4.BeautifulSoup(html, 'html.parser')
       try:
           findAllCards = soup.find_all('span', {'class': 'style__text__2xIA2'})
           for card in findAllCards:
               if 'Add to Cart' in card.get_text():
                   print('Card Available!')
                   driverWait(driver, 'css', '.style__addToCart__9TqqV')
                   driverWait(driver, 'css', '#nav-cart')
                   driverWait(driver, 'css', '.a-button-input')
                   try:
                       askingToLogin = driver.find_element_by_css_selector('#ap_password').is_displayed()
                       if askingToLogin:
                           driver.find_element_by_css_selector('#ap_password').send_keys(password)
                           driverWait(driver, 'css', '#signInSubmit')
                   except NoSuchElementException:
                       pass
                   driverWait(driver, 'css', '.a-button-input')  # Final Checkout Button!
                   print('Order Placed')
                   try:
                       client.messages.create(to=toNumber, from_=fromNumber, body='ORDER PLACED!')
                   except (NameError, TwilioRestException):
                       print('unable to send message')
                       pass
                   for i in range(3):
                       print('\a')
                       time.sleep(1)
                   time.sleep(2)
                   driver.quit()
                   return
       except (AttributeError, NoSuchElementException, TimeoutError):
           pass
       timeSleep(2, driver)


if __name__ == '__main__':
   success = 0
   while(success < 5):
      driver = createDriver()
      if(loginAttempt(driver)):
        findingCards(driver)
        success = success + 1

