from selenium import webdriver
from selenium.webdriver.common.by import By
# Remove ChromeService and ChromeDriverManager
# from selenium.webdriver.chrome.service import Service as ChromeService
# from webdriver_manager.chrome import ChromeDriverManager
from selenium.webdriver.chrome.options import Options
from bs4 import BeautifulSoup
import time 

# --- 1. Selenium-WebDriverin alustus ---
# Käytä webdriver_manageria asentamaan ja hallitsemaan Chromedriveria automaattisesti
# Jos haluat Firefoxin, käytä FirefoxService ja GeckoDriverManager
def run_scraper(url):
    try:
        # Use ChromeOptions to enable headless mode, which is important for Docker
        chrome_options = Options()
        chrome_options.add_argument("--headless")
        chrome_options.add_argument("--no-sandbox")
        chrome_options.add_argument("--disable-dev-shm-usage")

        # Create a new WebDriver session without a service object
        # It will automatically find the pre-installed driver.
        driver = webdriver.Chrome(options=chrome_options)
        
        print("WebDriver initialized successfully.")
        print(f"Navigating to: {url}")
        # --- 2. Navigointi sivulle ja JavaScript-sisällön latauksen odottaminen ---
        
        print(f"Navigating to: {url}")
        driver.get(url)        
        
        time.sleep(5) # Odota 5 sekuntia, että sivu ja sen sisältö varmasti latautuu
        # webdriver.support.ui.WebDriverWait ja expected_conditions ovat parempia dynaamiseen odotteluun
        # from selenium.webdriver.support.ui import WebDriverWait
        # from selenium.webdriver.support import expected_conditions as EC
        # WebDriverWait(driver, 10).until(EC.presence_of_element_located((By.CSS_SELECTOR, ".list-item-area")))
        print("Page loaded (or waited for content).")
    
        # --- 3. Koko renderoidun HTML:n haku Seleniumilta ---
        html_content = driver.page_source
        print(f"Fetched HTML content. Length: {len(html_content)} characters.")

        # --- 4. HTML:n jäsentäminen Beautiful Soupilla ---
        soup = BeautifulSoup(html_content, 'html.parser')
        print("HTML parsed by Beautiful Soup.")

        # --- 5. Tietojen poiminta Beautiful Soupilla ---    
        print("\n--- Scraping data ---")
        apartments = soup.find_all('div', class_='kfALKRz') # Etsi div-elementit tietyllä luokalla

        if not apartments:
            print("No apartment listings found with the specified selector. Please check the CSS selector.")

        scraped_apartments = []

        for apartment in apartments:
            target_text = "Uusi"
            
            # Tarkista, sisältääkö koko ilmoituksen teksti halutun merkkijonon.
            # get_text() poimii tekstin kaikista sisäkkäisistä elementeistä.
            normalized_text = ' '.join(apartment.get_text(strip=True).split())
            if target_text in normalized_text:
                try:
                    # Etsi asunnon nimi/osoite
                    address_element = apartment.select_one('h3.e1tdergc0.mui-style-jit781') # Etsi linkki tietyllä luokalla
                    address = address_element.get_text(strip=True) if address_element else 'N/A'

                    # Etsi hinta
                    price_element = apartment.select_one('.MuiGrid-grid-xs-4.mui-style-j3iqgs span') # Etsi hinnan sisältävä div
                    price = price_element.get_text(strip=True) if price_element else 'N/A'

                    # Etsi linkki asuntoon
                    link_element = apartment.select_one('a.mui-style-d75blp.e1ywucm62')
                    link = link_element.get('href') if link_element else 'N/A'
                    full_link = f"https://www.etuovi.com{link}" if link != 'N/A' else 'N/A'

                    scraped_apartments.append(
                        {
                            'Address': address,
                            'Price': price,
                            'Link': full_link
                        }
                    )
                    #print(f"Address: {address}, Price: {price}, Link: {full_link}")
                except Exception as e:
                    print(f"Error processing an apartment listing: {e}")
                    
        # --- 6. Selaimen sulkeminen ---
        driver.quit()   
        #print(scraped_apartments) 
        return scraped_apartments
    
    except Exception as e:
        # --- 4. Virheen palautus ---
        print(f"A major error occurred during scraping: {e}")
        try:
            driver.quit() # Sulje selain, vaikka virhe tapahtuikin
        except:
            pass
        return {'error': str(e)}