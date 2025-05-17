import time
import json
import csv
import sys
import os
from selenium import webdriver
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.common.exceptions import TimeoutException, NoSuchElementException
from webdriver_manager.chrome import ChromeDriverManager

def scrape_olx_car_covers(pages=3):
    """
    Scrape car cover listings from OLX India using Selenium
    and save to CSV and JSON files.
    
    Args:
        pages: Number of pages to scrape (default: 3)
    
    Returns:
        List of dictionaries containing car cover listings data
    """
    print("Setting up Chrome WebDriver...")
    

    chrome_options = Options()
    chrome_options.add_argument("--headless")  
    chrome_options.add_argument("--disable-gpu")
    chrome_options.add_argument("--window-size=1920,1080")
    chrome_options.add_argument("--disable-dev-shm-usage")
    chrome_options.add_argument("--no-sandbox")
    chrome_options.add_argument("--disable-notifications")
    chrome_options.add_argument("--disable-popup-blocking")
    chrome_options.add_argument("--user-agent=Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/98.0.4758.102 Safari/537.36")
    

    try:
        driver = webdriver.Chrome(service=Service(ChromeDriverManager().install()), options=chrome_options)
    except Exception as e:
        print(f"Error setting up Chrome driver: {e}")
        print("Attempting to use local Chrome driver...")
        try:
            driver = webdriver.Chrome(options=chrome_options)
        except Exception as e:
            print(f"Error using local Chrome driver: {e}")
            print("Please install Chrome and chromedriver manually.")
            return []
    
    base_url = "https://www.olx.in/items/q-car-cover"
    all_listings = []
    
    try:
        for page in range(1, pages + 1):
            url = f"{base_url}?page={page}" if page > 1 else base_url
            print(f"\nScraping page {page} at URL: {url}")
            
            driver.get(url)
            print("Waiting for page to load...")
            
            try:
                WebDriverWait(driver, 20).until(
                    EC.presence_of_element_located((By.TAG_NAME, "body"))
                )
                print("Page loaded successfully")
            except TimeoutException:
                print("Timeout waiting for page to load. Continuing anyway...")
            
            screenshot_path = f"olx_page_{page}.png"
            driver.save_screenshot(screenshot_path)
            print(f"Screenshot saved to {screenshot_path}")
            
            html_path = f"olx_page_{page}.html"
            with open(html_path, "w", encoding="utf-8") as f:
                f.write(driver.page_source)
            print(f"HTML source saved to {html_path}")
            
            time.sleep(5)
            
            possible_selectors = [
                "//li[contains(@class, '_1DNjI')]",
                "//div[contains(@class, 'IKo3_')]",
                "//li[contains(@class, 'EIR5N')]",
                "//div[contains(@data-aut-id, 'itemBox')]",
                "//li[@data-aut-id='itemCard']",
                "//div[contains(@class, 'a5112')]",
                "//a[contains(@class, 'fhlkh')]"
            ]
            
            listing_elements = []
            successful_selector = None
            
            for selector in possible_selectors:
                try:
                    print(f"Trying selector: {selector}")
                    elems = driver.find_elements(By.XPATH, selector)
                    if elems and len(elems) > 0:
                        listing_elements = elems
                        successful_selector = selector
                        print(f"Found {len(listing_elements)} listings with selector: {selector}")
                        break
                except Exception as e:
                    print(f"Error with selector {selector}: {e}")
            
            if not listing_elements:
                print("No listings found with specific selectors. Trying generic approach...")
                try:
                    listing_elements = driver.find_elements(By.XPATH, 
                        "//li[.//span[contains(@class, 'price')] or .//span[contains(text(), '₹')]]")
                    
                    if not listing_elements:
                        listing_elements = driver.find_elements(By.XPATH, 
                            "//div[.//span[contains(@class, 'price')] or .//span[contains(text(), '₹')]]")
                    
                    print(f"Found {len(listing_elements)} listings with generic approach")
                except Exception as e:
                    print(f"Error with generic approach: {e}")
            
            if not listing_elements:
                print("Warning: No listings found on this page.")
                print("Website structure might have changed or anti-scraping measures in place.")
                continue
            
            print(f"Processing {len(listing_elements)} listings from page {page}...")
            
            for i, listing in enumerate(listing_elements):
                try:
                    listing_data = {
                        'title': "No Title",
                        'price': "No Price",
                        'location': "No Location",
                        'date': "No Date",
                        'link': "No Link",
                        'image_url': "No Image"
                    }
                    
                    try:
                        title_xpath_options = [
                            ".//span[contains(@class, '_2poNJ')]",
                            ".//span[contains(@class, 'a5112')]",
                            ".//div[contains(@class, '_69EjX')]",
                            ".//span[@data-aut-id='itemTitle']",
                            ".//div[contains(@class, 'heading')]",
                            ".//h2"
                        ]
                        
                        for xpath in title_xpath_options:
                            try:
                                title_elem = listing.find_element(By.XPATH, xpath)
                                if title_elem and title_elem.text.strip():
                                    listing_data['title'] = title_elem.text.strip()
                                    break
                            except NoSuchElementException:
                                continue
                            
                        if listing_data['title'] == "No Title":
                            try:
                                any_text = listing.text
                                if any_text:
                                    lines = [line.strip() for line in any_text.split('\n') if line.strip()]
                                    if lines:
                                        listing_data['title'] = lines[0]  
                            except:
                                pass
                    except Exception as e:
                        print(f"Error extracting title: {e}")
                    
                    try:
                        price_xpath_options = [
                            ".//span[contains(@class, '_2Ks63')]",
                            ".//span[contains(@class, '_89yzn')]",
                            ".//span[@data-aut-id='itemPrice']",
                            ".//span[contains(text(), '₹')]",
                            ".//span[contains(text(), 'Rs')]"
                        ]
                        
                        for xpath in price_xpath_options:
                            try:
                                price_elem = listing.find_element(By.XPATH, xpath)
                                if price_elem and price_elem.text.strip():
                                    listing_data['price'] = price_elem.text.strip()
                                    break
                            except NoSuchElementException:
                                continue
                    except Exception as e:
                        print(f"Error extracting price: {e}")
                    
                    try:
                        location_xpath_options = [
                            ".//span[contains(@class, '_2vNpt')]",
                            ".//span[contains(@class, '_1KOFM')]",
                            ".//span[@data-aut-id='item-location']"
                        ]
                        
                        for xpath in location_xpath_options:
                            try:
                                location_elem = listing.find_element(By.XPATH, xpath)
                                if location_elem and location_elem.text.strip():
                                    listing_data['location'] = location_elem.text.strip()
                                    break
                            except NoSuchElementException:
                                continue
                    except Exception as e:
                        print(f"Error extracting location: {e}")
                    
                    try:
                        date_xpath_options = [
                            ".//span[contains(@class, 'zLvFQ')]",
                            ".//span[contains(@class, '_2DGqt')]",
                            ".//span[@data-aut-id='item-date']"
                        ]
                        
                        for xpath in date_xpath_options:
                            try:
                                date_elem = listing.find_element(By.XPATH, xpath)
                                if date_elem and date_elem.text.strip():
                                    listing_data['date'] = date_elem.text.strip()
                                    break
                            except NoSuchElementException:
                                continue
                    except Exception as e:
                        print(f"Error extracting date: {e}")
                    
                    try:
                        link_elem = listing.find_element(By.XPATH, ".//a")
                        if link_elem and link_elem.get_attribute("href"):
                            listing_data['link'] = link_elem.get_attribute("href")
                    except Exception as e:
                        try:
                            if listing.tag_name == 'a' and listing.get_attribute("href"):
                                listing_data['link'] = listing.get_attribute("href")
                        except:
                            pass
                    
                    try:
                        img_elem = listing.find_element(By.XPATH, ".//img")
                        if img_elem:
                            for attr in ['src', 'data-src', 'srcset']:
                                img_url = img_elem.get_attribute(attr)
                                if img_url:
                                    if attr == 'srcset' and ' ' in img_url:
                                        img_url = img_url.split(' ')[0]
                                    listing_data['image_url'] = img_url
                                    break
                    except Exception as e:
                        print(f"Error extracting image: {e}")
                    
                    print(f"Processed listing {i+1}: {listing_data['title']}")
                    all_listings.append(listing_data)
                    
                except Exception as e:
                    print(f"Error processing listing {i+1}: {e}")
            
            print(f"Finished processing page {page}. Found {len(listing_elements)} listings.")
            
            if page < pages:
                delay = 5  
                print(f"Waiting {delay} seconds before next page...")
                time.sleep(delay)
    
    except Exception as e:
        print(f"Unexpected error during scraping: {e}")
        import traceback
        traceback.print_exc()
    
    finally:
        print("Closing browser...")
        driver.quit()
    
    print(f"\nTotal listings collected: {len(all_listings)}")
    
    if not all_listings:
        print("No listings were found.")
        return []
    
    try:
        with open('car_covers_olx.csv', 'w', newline='', encoding='utf-8') as csvfile:
            fieldnames = ['title', 'price', 'location', 'date', 'link', 'image_url']
            writer = csv.DictWriter(csvfile, fieldnames=fieldnames)
            
            writer.writeheader()
            for listing in all_listings:
                writer.writerow(listing)
        print("Data saved to 'car_covers_olx.csv'")
    except Exception as e:
        print(f"Error saving CSV file: {e}")
    
    try:
        with open('car_covers_olx.json', 'w', encoding='utf-8') as jsonfile:
            json.dump(all_listings, jsonfile, ensure_ascii=False, indent=4)
        print("Data saved to 'car_covers_olx.json'")
    except Exception as e:
        print(f"Error saving JSON file: {e}")
    
    return all_listings

if __name__ == "__main__":
    try:
        print("OLX Car Cover Scraper (Selenium Version)")
        print("---------------------------------------")
        print(f"Python version: {sys.version}")
        

        if not os.path.exists("setup_complete.txt"):
            print("\nFIRST RUN SETUP:")
            print("This script requires the following Python packages:")
            print("- selenium")
            print("- webdriver-manager")
            print("\nInstall them with:")
            print("pip install selenium webdriver-manager")
            print("\nYou also need Chrome browser installed.")
            print("The script will attempt to automatically download the appropriate ChromeDriver.")
            print("\nAfter installing dependencies, run this script again.")
            
            with open("setup_complete.txt", "w") as f:
                f.write("Setup instructions displayed")
            
            choice = input("\nWould you like to attempt to run anyway? (y/n): ")
            if choice.lower() != 'y':
                sys.exit(0)
        
        pages = 3
        if len(sys.argv) > 1:
            try:
                pages = int(sys.argv[1])
                print(f"Will scrape {pages} pages")
            except ValueError:
                print(f"Invalid number of pages: {sys.argv[1]}. Using default: {pages}")
        
        scrape_olx_car_covers(pages=pages)
    except KeyboardInterrupt:
        print("\nScraping interrupted by user")
    except Exception as e:
        print(f"Unexpected error: {e}")
        import traceback
        traceback.print_exc()

