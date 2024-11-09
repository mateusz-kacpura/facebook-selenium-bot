from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.common.action_chains import ActionChains
from selenium.webdriver.chrome.service import Service
from selenium.common.exceptions import TimeoutException
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.common.keys import Keys
import time

# Inicjalizacja przeglądarki
def initialize_browser():
    service = Service("C:\\Users\\engli\\Downloads\\chromedriver-win64\\chromedriver-win64\\chromedriver.exe")  # Podaj ścieżkę do chromedriver
    options = webdriver.ChromeOptions()
    options.add_argument("--no-sandbox")
    options.add_argument("--disable-dev-shm-usage")
    
    # Ustawienie nagłówka User-Agent
    options.add_argument("user-agent=Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/110.0.5481.177 Safari/537.36")
    
    # Wyłączenie flagi wykrywalności Selenium
    options.add_experimental_option("excludeSwitches", ["enable-automation"])
    options.add_experimental_option("useAutomationExtension", False)
    
    driver = webdriver.Chrome(service=service, options=options)
    driver.execute_script("Object.defineProperty(navigator, 'webdriver', {get: () => undefined})")
    
    return driver

# Kliknięcie przycisku "Allow all cookies"
def click_allow_cookies(driver):
    wait = WebDriverWait(driver, 15)
    try:
        allow_cookies_button = wait.until(EC.element_to_be_clickable((By.XPATH, "//button[@data-cookiebanner='accept_button']")))
        allow_cookies_button.click()
        print("Kliknięto 'Allow all cookies'")
    except TimeoutException:
        print("Nie znaleziono przycisku 'Allow all cookies', przechodzę dalej")

# Logowanie do Facebooka
def login_to_facebook(driver, email, password):
    wait = WebDriverWait(driver, 15)
    # Czekaj na załadowanie pól logowania
    try:
        email_field = wait.until(EC.presence_of_element_located((By.ID, "email")))
        password_field = driver.find_element(By.ID, "pass")
        print("Pola logowania załadowane")
    except TimeoutException:
        print("Strona logowania się nie załadowała")
        driver.quit()
        exit()
        
    # Wprowadź dane logowania
    email_field.send_keys(email)
    password_field.send_keys(password)
    
    # Kliknij przycisk logowania
    login_button = driver.find_element(By.NAME, "login")
    login_button.click()
    print("Przycisk logowania kliknięty")
    
    # Czekaj na zalogowanie
    time.sleep(5)

# Przejście do strony z listą znajomych
def go_to_friends_list(driver, FRIENDS_URL):
    driver.get(FRIENDS_URL)
    # Czekaj na załadowanie strony znajomych
    time.sleep(5)

# Przewijanie strony do dołu
def scroll_to_bottom(driver):
    # Skroluj do samego dołu, aby załadować wszystkich znajomych
    scroll_pause_time = 2
    last_height = driver.execute_script("return document.body.scrollHeight")
    
    while True:
        # Przewiń do dołu
        driver.execute_script("window.scrollTo(0, document.body.scrollHeight);")
        
        # Poczekaj na załadowanie nowej zawartości
        time.sleep(scroll_pause_time)
        
        # Oblicz nową wysokość strony po przewinięciu
        new_height = driver.execute_script("return document.body.scrollHeight")
        
        if new_height == last_height:
            # Osiągnięto dół strony
            break
        last_height = new_height

# Pobranie i wypisanie listy znajomych
def get_friends_list(driver):
    # Znajdź elementy reprezentujące znajomych
    try:
        friend_elements = driver.find_elements(By.XPATH, "//div[@data-visualcompletion='ignore-dynamic']//a[contains(@href, 'facebook.com') and @role='link']/span")
        friend_names = [friend.text for friend in friend_elements if friend.text]
        print("Lista znajomych:")
        for name in friend_names:
            print(name)
    except Exception as e:
        print("Nie udało się pobrać listy znajomych:", e)

# Wysłanie wiadomości na Messengerze
def send_message(driver, message_url, message_text):
    driver.get(message_url)
    wait = WebDriverWait(driver, 15)
    # Czekaj na załadowanie strony wiadomości
    time.sleep(5)
    # Wprowadź treść wiadomości i wyślij
    try:
        message_box = wait.until(EC.presence_of_element_located((By.XPATH, "//div[@aria-label='Wiadomość']")))
        message_box.click()
        actions = ActionChains(driver)
        actions.send_keys(message_text)
        actions.send_keys(Keys.ENTER)
        actions.perform()
        print("Wiadomość wysłana")
    except TimeoutException:
        print("Nie udało się znaleźć pola do wpisania wiadomości")
    except Exception as e:
        print("Błąd podczas wysyłania wiadomości:", e)

if __name__ == "__main__":
    EMAIL = ""  # Wpisz swój email
    PASSWORD = ""  # Wpisz swoje hasło
    MESSAGE_URL = "https://www.facebook.com/messages/e2ee/t/7517691988297238"
    MESSAGE_TEXT = "ok"

    FRIENDS_URL = "https://www.facebook.com/profile.php?id=xxxxxxxxxxx&sk=friends"

    driver = initialize_browser()
    driver.get("https://www.facebook.com")
    
    click_allow_cookies(driver)
    login_to_facebook(driver, EMAIL, PASSWORD)
    go_to_friends_list(driver, FRIENDS_URL)
    scroll_to_bottom(driver)
    get_friends_list(driver)
    send_message(driver, MESSAGE_URL, MESSAGE_TEXT)
    
    # Poczekaj chwilę i zamknij przeglądarkę
    time.sleep(10)
    driver.quit()
