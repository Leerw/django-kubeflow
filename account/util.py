from pyvirtualdisplay import Display
from selenium import webdriver 
import time


def get_url(username, password):
    display = Display(visible=0, size=(800, 600))
    display.start()


    driver = webdriver.Firefox() 
    driver.maximize_window() 
    driver.implicitly_wait(3) 
    
    driver.get("http://127.0.0.1:8888") 

    element_user = driver.find_element_by_xpath('//input[@id="username_input"]')
    element_user.send_keys(username)
    element_pwd = driver.find_element_by_xpath('//input[@id="password_input"]')
    element_pwd.send_keys(password)

    commit = driver.find_element_by_xpath('//input[@id="login_submit"]')
    commit.click()

    time.sleep(3) 
    
    url = driver.current_url
    print (driver.current_url)  # current_url 方法可以得到当前页面的URL 
    print (driver.title)  # title方法可以获取当前页面的标题显示的字段 
    
    driver.quit()
    display.stop()
    return url
