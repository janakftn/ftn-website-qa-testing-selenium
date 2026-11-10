from selenium import webdriver
from selenium.webdriver.common.by import By
import time


def load_ftn(url):
    driver = webdriver.Chrome()
    driver.maximize_window()
    driver.get(url)
    return driver

def test_button_studije():
    driver = load_ftn('https://ftn.uns.ac.rs/')
    driver.find_elements(By.CLASS_NAME, "e-n-menu-title-text")[3].click()
    time.sleep(1)
    driver.find_element(By.LINK_TEXT, 'РАДНИ КАЛЕНДАР').click()
    time.sleep(3)

    driver.switch_to.window(driver.window_handles[-1])

    assert 'Радни календар' in driver.find_element(By.XPATH,"//h2[contains(., 'Радни календар')]").text, \
        'Ne radi dugme Radni Kalendar'
    close_chrome(driver)


def test_search():
    driver = load_ftn('https://ftn.uns.ac.rs/')
    driver.find_element(By.CLASS_NAME, 'search-container').click()
    driver.find_element(By.ID, "search-input-1").send_keys("inženjerstvo informacionih sistema")
    time.sleep(1)
    driver.find_element(By.CSS_SELECTOR, ".icon.icon-magnifying-glass-search.search-icon-submit").click()
    driver.save_screenshot('sa_Ž.png')
    assert 'Студијски програми:' in driver.find_element(By.XPATH, "//h4[contains(., 'Студијски програми:')]").text, 'Search nije uspešan'
    close_chrome(driver)


def test_search_with_BUG():
    driver = load_ftn('https://ftn.uns.ac.rs/')
    driver.find_element(By.CLASS_NAME, 'search-container').click()
    driver.find_element(By.ID, "search-input-1").send_keys("inzenjerstvo informacionih sistema")
    time.sleep(1)
    driver.find_element(By.CSS_SELECTOR, ".icon.icon-magnifying-glass-search.search-icon-submit").click()
    driver.save_screenshot('sa_Z.png')

    assert 'Студијски програми:' in driver.find_element(By.XPATH, "//h4[contains(., 'Студијски програми:')]").text, \
        'Pretraga ne pronalazi rezultate bez dijakritickih znakova'
    close_chrome(driver)


def test_search_no_results():
    driver = load_ftn('https://ftn.uns.ac.rs/')
    driver.find_element(By.CLASS_NAME, 'search-container').click()
    driver.find_element(By.ID, "search-input-1").send_keys("xyz12345")
    time.sleep(1)
    driver.find_element(By.CSS_SELECTOR, ".icon.icon-magnifying-glass-search.search-icon-submit").click()
    time.sleep(2)

    assert 'Нема резултата за ваш упит.' in driver.find_element(By.TAG_NAME,"body").text, 'Ne prikazuje poruku da nema rezultata'
    close_chrome(driver)


def test_search_empty():
    driver = load_ftn('https://ftn.uns.ac.rs/')
    driver.find_element(By.CLASS_NAME, 'search-container').click()
    driver.find_element(By.CSS_SELECTOR, ".icon.icon-magnifying-glass-search.search-icon-submit").click()
    alert = driver.switch_to.alert

    assert alert.text == "Unesite najmanje 3 karaktera pre pretrage.", "Poruka za praznu pretragu nije ispravna"

    alert.accept()
    close_chrome(driver)


def test_search_two_characters():
    driver = load_ftn('https://ftn.uns.ac.rs/')
    driver.find_element(By.CLASS_NAME, 'search-container').click()
    driver.find_element(By.ID, "search-input-1").send_keys("xy")
    driver.find_element(By.CSS_SELECTOR, ".icon.icon-magnifying-glass-search.search-icon-submit").click()
    alert = driver.switch_to.alert

    assert alert.text == "Unesite najmanje 3 karaktera pre pretrage.", "Neispravna poruka za pretragu sa dva karaktera"

    alert.accept()
    close_chrome(driver)


def test_search_spaces():
    driver = load_ftn('https://ftn.uns.ac.rs/')
    driver.find_element(By.CLASS_NAME, 'search-container').click()
    driver.find_element(By.ID, "search-input-1").send_keys("     inženjerstvo informacionih sistema   ")
    time.sleep(1)
    driver.find_element(By.CSS_SELECTOR, ".icon.icon-magnifying-glass-search.search-icon-submit").click()

    assert 'Студијски програми:' in driver.find_element(By.XPATH, "//h4[contains(., 'Студијски програми:')]").text, 'Search nije uspešan'
    close_chrome(driver)


def test_search_case_sensitive_BUG():
    driver = load_ftn('https://ftn.uns.ac.rs/')
    driver.find_element(By.CLASS_NAME, 'search-container').click()
    driver.find_element(By.ID, "search-input-1").send_keys("INŽENJERSTVO INFORMACIONIH SISTEMA")
    time.sleep(1)
    driver.find_element(By.CSS_SELECTOR, ".icon.icon-magnifying-glass-search.search-icon-submit").click()


    assert 'Студијски програми:' in driver.find_element(By.XPATH, "//h4[contains(., 'Студијски програми:')]").text, \
        'Pretraga ne pronalazi rezultate kada se koriste velika slova'
    close_chrome(driver)


def test_search_long_text():
    driver = load_ftn('https://ftn.uns.ac.rs/')

    driver.find_element(By.CLASS_NAME, 'search-container').click()
    driver.find_element(By.ID, "search-input-1").send_keys("inzenjerstvo " * 100)
    driver.find_element(By.CSS_SELECTOR, ".icon.icon-magnifying-glass-search.search-icon-submit").click()
    time.sleep(2)

    assert 'Нема резултата за ваш упит.' in driver.find_element(By.TAG_NAME, "body").text, \
        'Neočekivano ponašanje pri pretrazi dugog teksta'
    close_chrome(driver)


def test_multiple_search_clicks():
    driver = load_ftn('https://ftn.uns.ac.rs/')

    driver.find_element(By.CLASS_NAME, 'search-container').click()
    driver.find_element(By.ID, "search-input-1").send_keys("matematika")

    driver.find_element(By.CSS_SELECTOR, ".icon.icon-magnifying-glass-search.search-icon-submit").click()
    time.sleep(1)

    driver.back()
    time.sleep(1)

    driver.find_element(By.CLASS_NAME, 'search-container').click()
    driver.find_element(By.CSS_SELECTOR, ".icon.icon-magnifying-glass-search.search-icon-submit").click()
    time.sleep(2)

    assert driver.find_element(By.TAG_NAME, "body").text.strip() != "", "Stranica je prazna nakon višestrukog klika"

    close_chrome(driver)



def close_chrome(driver):
    driver.minimize_window()
    driver.quit()