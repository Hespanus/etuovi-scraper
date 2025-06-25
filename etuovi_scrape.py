from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.chrome.service import Service as ChromeService
from webdriver_manager.chrome import ChromeDriverManager
from bs4 import BeautifulSoup
import time # Tarvitaan odotteluun, esim. sivun latautumista varten

# --- 1. Selenium-WebDriverin alustus ---
# Käytä webdriver_manageria asentamaan ja hallitsemaan Chromedriveria automaattisesti
# Jos haluat Firefoxin, käytä FirefoxService ja GeckoDriverManager
try:
    service = ChromeService(ChromeDriverManager().install())
    driver = webdriver.Chrome(service=service)
    print("WebDriver initialized successfully.")
except Exception as e:
    print(f"Error initializing WebDriver: {e}")
    print("Please ensure you have Google Chrome installed.")
    exit()

# --- 2. Navigointi sivulle ja JavaScript-sisällön latauksen odottaminen ---
url = "https://www.etuovi.com/myytavat-asunnot/lahti?haku=M2265566761"
print(f"Navigating to: {url}")
driver.get(url)

# Odotetaan dynaamisen sisällön latautumista. Tämä on kriittistä JavaScript-sivuilla.
# Voit odottaa tietyn elementin ilmestymistä (paras tapa) tai kiinteän ajan.
# Esimerkiksi odotetaan, että jokin asuntojen listauselementti ilmestyy.
# (Tarkista tarkka CSS-selektori Etuovi.comista kehittäjätyökaluilla!)
try:
    # Esimerkki: Odota, että elementti, jolla on luokka 'list-item-area' (tai vastaava) ilmestyy
    # Tätä voi joutua muokkaamaan Etuovi.comin rakenteen mukaan
    time.sleep(5) # Odota 5 sekuntia, että sivu ja sen sisältö varmasti latautuu
    # webdriver.support.ui.WebDriverWait ja expected_conditions ovat parempia dynaamiseen odotteluun
    # from selenium.webdriver.support.ui import WebDriverWait
    # from selenium.webdriver.support import expected_conditions as EC
    # WebDriverWait(driver, 10).until(EC.presence_of_element_located((By.CSS_SELECTOR, ".list-item-area")))
    print("Page loaded (or waited for content).")
except Exception as e:
    print(f"Could not find expected element on page or page did not load in time: {e}")
    driver.quit()
    exit()

# --- 3. Koko renderoidun HTML:n haku Seleniumilta ---
html_content = driver.page_source
print(f"Fetched HTML content. Length: {len(html_content)} characters.")

# --- 4. HTML:n jäsentäminen Beautiful Soupilla ---
soup = BeautifulSoup(html_content, 'html.parser')
print("HTML parsed by Beautiful Soup.")

# --- 5. Tietojen poiminta Beautiful Soupilla ---
# Nämä selektorit ovat vain esimerkkejä ja ne TÄYTYY tarkistaa
# Etuovi.comin sivun rakenne kehittäjätyökaluilla!
print("\n--- Scraping data ---")
apartments = soup.find_all('div', class_='kfALKRz') # Etsi div-elementit tietyllä luokalla

if not apartments:
    print("No apartment listings found with the specified selector. Please check the CSS selector.")

for apartment in apartments:
    target_text = "Uusi 24 h"
    
    # Tarkista, sisältääkö koko ilmoituksen teksti halutun merkkijonon.
    # get_text() poimii tekstin kaikista sisäkkäisistä elementeistä.
    normalized_text = ' '.join(apartment.get_text(strip=True).split())
    if target_text in normalized_text:
        try:
            # Etsi asunnon nimi/osoite
            address_element = apartment.select_one('h4.MuiTypography-root.MuiTypography-body1.e3qdyeq9.e1tdergc0.mui-style-jit781') # Etsi linkki tietyllä luokalla
            address = address_element.get_text(strip=True) if address_element else 'N/A'

            # Etsi hinta
            price_element = apartment.select_one('.MuiGrid-grid-xs-4.mui-style-j3iqgs span') # Etsi hinnan sisältävä div
            price = price_element.get_text(strip=True) if price_element else 'N/A'

            # Etsi linkki asuntoon
            link_element = apartment.select_one('a.mui-style-1hvv1xy.e3qdyeq2')
            link = link_element.get('href') if link_element else 'N/A'
            full_link = f"https://www.etuovi.com{link}" if link != 'N/A' else 'N/A'

            print(f"Address: {address}, Price: {price}, Link: {full_link}")
        except Exception as e:
            print(f"Error processing an apartment listing: {e}")
            # Voit tulostaa koko elementin tarkempaa debuggausta varten
            # print(apartment.prettify())

# --- 6. Selaimen sulkeminen ---
driver.quit()
print("\nBrowser closed. Script finished.")