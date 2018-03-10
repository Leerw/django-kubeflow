from pyvirtualdisplay import Display
from selenium import webdriver 
import time


def get_url(username, password):
    display = Display(visible=0, size=(800, 600))
    display.start()


    driver = webdriver.Firefox() 
    driver.maximize_window() 
    driver.implicitly_wait(3) 
    
    # Login
    driver.get("http://127.0.0.1:8888") 

    element_user = driver.find_element_by_xpath('//input[@id="username_input"]')
    element_user.send_keys(username)
    element_pwd = driver.find_element_by_xpath('//input[@id="password_input"]')
    element_pwd.send_keys(password)

    commit = driver.find_element_by_xpath('//input[@id="login_submit"]')
    commit.click()

    time.sleep(3)

    # Start Server
    start_server = driver.find_element_by_xpath('//a[@id="start"]')
    start_server.click()

    time.sleep(5)

    print(driver.current_url)
    
    # Configuration docker container
    image = driver.find_element_by_xpath('//input[@name="image"]')
    image.send_keys('gcr.io/kubeflow/tensorflow-notebook-cpu:v1')

    cpu = driver.find_element_by_xpath('//input[@name="cpu_guarantee"]')
    cpu.send_keys('1')

    mem = driver.find_element_by_xpath('//input[@name="mem_guarantee"]')
    mem.send_keys('100Mi')

    spawn = driver.find_element_by_xpath('//input[@value="Spawn"]')
    spawn.click()
    # wait for starting container
    time.sleep(30)

    url = driver.current_url
    print (driver.current_url)  # current_url 方法可以得到当前页面的URL 
    print (driver.title)  # title方法可以获取当前页面的标题显示的字段 
    
    driver.quit()
    display.stop()
    
    # return notebook url
    return url
