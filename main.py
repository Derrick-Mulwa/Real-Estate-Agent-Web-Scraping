import pandas as pd
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.support.wait import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
import time
import random
import requests
import io
from PIL import Image

# Lets define the url where we will scrape and the path of our chromedriver
url = "https://www.homes.com/real-estate-agents/boston-ma/p2/"
PATH = "C:\Program Files (x86)\chromedriver.exe"

driver = webdriver.Chrome(executable_path=PATH)
# Maximize the window
driver.maximize_window()

# Go to the website
driver.get(url)

top_100_cities_usa = [
    "New York, NY", "Los Angeles, CA", "Chicago, IL", "Houston, TX", "Phoenix, AZ",
    "Philadelphia, PA", "San Antonio, TX", "San Diego, CA", "Dallas, TX", "San Jose, CA",
    "Austin, TX", "Jacksonville, FL", "Fort Worth, TX", "Columbus, OH", "Charlotte, NC",
    "San Francisco, CA", "Indianapolis, IN", "Seattle, WA", "Denver, CO", "Washington, DC",
    "Boston, MA", "El Paso, TX", "Nashville, TN", "Detroit, MI", "Oklahoma City, OK",
    "Portland, OR", "Las Vegas, NV", "Memphis, TN", "Louisville, KY", "Baltimore, MD",
    "Milwaukee, WI", "Albuquerque, NM", "Tucson, AZ", "Fresno, CA", "Sacramento, CA",
    "Kansas City, MO", "Long Beach, CA", "Mesa, AZ", "Atlanta, GA", "Colorado Springs, CO",
    "Virginia Beach, VA", "Raleigh, NC", "Omaha, NE", "Miami, FL", "Oakland, CA",
    "Minneapolis, MN", "Tulsa, OK", "Bakersfield, CA", "Wichita, KS", "Arlington, TX",
    "Aurora, CO", "Tampa, FL", "New Orleans, LA", "Cleveland, OH", "Anaheim, CA",
    "Henderson, NV", "Honolulu, HI", "Riverside, CA", "Santa Ana, CA", "Corpus Christi, TX",
    "Lexington, KY", "Stockton, CA", "Saint Paul, MN", "Cincinnati, OH", "Pittsburgh, PA",
    "Anchorage, AK", "Greensboro, NC", "Plano, TX", "Lincoln, NE", "Orlando, FL",
    "Irvine, CA", "Newark, NJ", "Toledo, OH", "Durham, NC", "Chula Vista, CA",
    "Fort Wayne, IN", "Jersey City, NJ", "St. Petersburg, FL", "Laredo, TX", "Madison, WI",
    "Chandler, AZ", "Buffalo, NY", "Lubbock, TX", "Scottsdale, AZ", "Reno, NV",
    "Glendale, AZ", "Gilbert, AZ", "Winston-Salem, NC", "North Las Vegas, NV", "Norfolk, VA",
    "Chesapeake, VA", "Garland, TX", "Irving, TX", "Hialeah, FL", "Fremont, CA",
    "Boise, ID", "Richmond, VA", "Baton Rouge, LA", "Spokane, WA", "Des Moines, IA"
]

Agent_Profile_link_list = []
Deals_in_agents_location_list = []
Price_range_in_agents_location_list = []

main_df = pd.DataFrame({
    "Agent_Name": [],
    "Agent_Image_Link": [],
    'Agent_Profile_link': [],
    "Agent_Location": [],
    "Office_Name": [],
    "Star_Ratings": [],
    "Number_Of_Reviews": [],
    'Deals_in_agents_location': [],
    'Price_range_in_agents_location': [],
    "Closed_Sales": [],
    "Total_Value": [],
    "Price_Range": [],
    "Average_Price": [],
    'Bio':[],
    "Home_Types": [],
    "Languages_Spoken": [],
    "Years_Of_Experience": [],
    "Agent_Website_Link": [],
    "Agent_Facebook_Link": [],
    "Agent_Linkedin_Link": [],
    "Agent_Twitter_Link": [],
    "Agent_Pinterest_Link": [],
    "Agent_Instagram_Link": [],
    "Agent_Youtube_Link": [],
    "Agent_Tiktok_Link": [],
    "Agent_Other_Link": [],
    "Phone_Number": [],
    "Transaction_History_Duration": [],
    "Seller_Deals_Total": [],
    "Seller_Deals_Total_Value": [],
    "Seller_Deals_Average_Sale_Price": [],
    "Seller_Deals_Price_Range": [],
    "Buyer_Deals_Total": [],
    "Buyer_Deals_Total_Value": [],
    "Buyer_Deals_Average_Sale_Price": [],
    "Buyer_Deals_Price_Range": [],
    "Other_Experiences": [],
    "Agent_Licence": [],
    "Awards_And_Designations": []
})

def download_image(image_url, filename):
    try:
        headers = {
            'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/126.0.0.0 Safari/537.36'
        }

        response = requests.get(image_url, headers=headers, timeout=5)
        if response.status_code == 200:
            image_content = response.content
            image_file = io.BytesIO(image_content)
            image = Image.open(image_file)

            with open(f'images/{filename}.jpg', 'wb') as f:
                image.save(f, 'JPEG')

        else:
            print(f'Response error {response.status_code}')
    except:
        print('Error connecting to the internet')

try:
    for city in top_100_cities_usa:
        try:
            clear_searchbox_button = WebDriverWait(driver, 10).until(
                EC.presence_of_element_located((By.CLASS_NAME, 'btn-clear'))
            )
            clear_searchbox_button = driver.find_element_by_class_name('btn-clear')
            time.sleep(0.5)

            clear_searchbox_button.click()

            time.sleep(1)
            searchbox = driver.find_element_by_class_name('multiselect-search')
            time.sleep(1)
            # Send keys slowly to avoid detection
            searchbox.send_keys(Keys.CLEAR)
            time.sleep(0.2)
            searchbox.send_keys(' ')

            for letter in city:
                time.sleep(round(random.uniform(0.1, 0.30), 2))
                searchbox.send_keys(letter)

            time.sleep(3)
            searchbox.send_keys(Keys.ENTER)
            time.sleep(5)

            page_being_scrapped_number = 1
            try:
                for page_being_scraped in range(5):
                    Agent_Profile_link_list = []
                    Deals_in_agents_location_list = []
                    Price_range_in_agents_location_list = []
                    agent_names_list = []
                    agent_image_link_list = []
                    agent_location_list = []
                    office_name_list = []
                    star_ratings_list = []
                    number_of_reviews_list = []
                    closed_sales_list = []
                    total_value_list = []
                    price_range_list = []
                    average_price_list = []
                    bio_list = []
                    home_types_list = []
                    languages_spoken_list = []
                    years_of_experience_list = []
                    agent_website_link_list = []
                    agent_facebook_link_list = []
                    agent_linkedin_link_list = []
                    agent_twitter_link_list = []
                    agent_pinterest_link_list = []
                    agent_instagram_link_list = []
                    agent_youtube_link_list = []
                    agent_tiktok_link_list = []
                    agent_other_link_list = []
                    phone_number_list = []
                    transaction_history_duration_list = []
                    seller_deals_total_list = []
                    seller_deals_total_value_list = []
                    seller_deals_average_sale_price_list = []
                    seller_deals_price_range_list = []
                    buyer_deals_total_list = []
                    buyer_deals_total_value_list = []
                    buyer_deals_average_sale_price_list = []
                    buyer_deals_price_range_list = []
                    other_experiences_list = []
                    agent_licence_list = []
                    awards_and_designations_list = []

                    agents_details = driver.find_elements_by_class_name('agent-results-item')
                    for agent in agents_details:
                        try:
                            Agent_Profile_link = agent.find_element_by_tag_name('a').get_attribute('href')
                            Deals_in_agents_location = agent.find_element_by_class_name('deals-area').find_element_by_tag_name('span').text
                            Price_range_in_agents_location = agent.find_element_by_class_name('price-range').find_element_by_tag_name('span').text


                            driver.execute_script(f"window.open('{Agent_Profile_link}', '_blank');")
                            driver.switch_to.window(driver.window_handles[-1])

                            try:
                                wait_image = WebDriverWait(driver, 10).until(
                                    EC.presence_of_element_located((By.CLASS_NAME, 'image-item-0'))
                                )
                                agent_image_url = \
                                driver.find_elements_by_class_name('image-item-0')[0].find_elements_by_tag_name('img')[0].get_attribute(
                                    'src')
                            except:
                                agent_image_url = ''

                            try:
                                agent_name = driver.find_element_by_class_name('name-container').find_element_by_tag_name('span').text
                            except:
                                agent_name = ''

                            try:
                                agent_location = driver.find_element_by_class_name('details-container-left').find_element_by_class_name(
                                    'location').text
                            except:
                                agent_location = ''

                            try:
                                agent_office_name = driver.find_element_by_class_name(
                                    'details-container-left').find_element_by_class_name('office-name').text
                            except:
                                agent_office_name = ''

                            try:
                                agent_star_rating = driver.find_element_by_class_name(
                                    'details-container-left').find_element_by_class_name('rating-container'). \
                                    find_element_by_class_name('item-rating').text.replace('\nstars,', '')

                                agent_number_of_reviews = driver.find_element_by_class_name(
                                    'details-container-left').find_element_by_class_name('rating-container'). \
                                    find_element_by_class_name('text-only').text.replace('Reviews', '').replace('Review', '')
                            except:
                                agent_star_rating = ''
                                agent_number_of_reviews = ''

                            try:
                                stats_container = driver.find_element_by_class_name('stats-container').find_elements_by_class_name(
                                    'stat-item')
                                closed_sales = stats_container[0].find_element_by_class_name('info-bold').text
                                total_value = stats_container[1].find_element_by_class_name('info-bold').text
                                price_range = stats_container[2].find_element_by_class_name('info-bold').text
                                average_price = stats_container[3].find_element_by_class_name('info-bold').text
                            except:
                                closed_sales = ''
                                total_value = ''
                                price_range = ''
                                average_price = ''

                            try:
                                bio = driver.find_element_by_class_name('bio-text').text
                            except:
                                bio = ''

                            try:
                                quick_info_container = driver.find_element_by_class_name(
                                    'quick-info-container').find_elements_by_class_name('info-bold')

                                home_types = ''
                                languages_spoken = ''
                                years_of_experience = ''

                                for each_quick_info in quick_info_container:
                                    if 'Home Types:' in each_quick_info.text:
                                        home_types = each_quick_info.text.replace('Home Types:', '').strip()
                                    elif 'Languages Spoken:' in each_quick_info.text:
                                        languages_spoken = each_quick_info.text.replace('Languages Spoken:', '').strip()
                                    elif 'Years of Experience:' in each_quick_info.text:
                                        years_of_experience = each_quick_info.text.replace('Years of Experience:', '').strip()
                            except:
                                home_types = ''
                                languages_spoken = ''
                                years_of_experience = ''

                            try:
                                agent_website_link = ''
                                agent_facebook_link = ''
                                agent_linkedin_link = ''
                                agent_twitter_link = ''
                                agent_pinterest_link = ''
                                agent_instagram_link = ''
                                agent_youtube_link = ''
                                agent_tiktok_link = ''
                                agent_other_links = ''

                                socials = driver.find_element_by_class_name('social-container').find_elements_by_tag_name('a')
                                for social in socials:
                                    social_title = social.get_attribute('title')
                                    social_link = social.get_attribute('href')
                                    if social_title == 'Link to Agent Website':
                                        agent_website_link = social_link

                                    elif social_title == 'Link to Facebook':
                                        agent_facebook_link = social_link

                                    elif social_title == 'Link to Linked In':
                                        agent_linkedin_link = social_link

                                    elif social_title == 'Link to Twitter':
                                        agent_twitter_link = social_link

                                    elif social_title == 'Link to Pinterest':
                                        agent_pinterest_link = social_link

                                    elif social_title == 'Link to Instagram':
                                        agent_instagram_link = social_link

                                    elif social_title == 'Link to TikTok':
                                        agent_tiktok_link = social_link

                                    else:
                                        agent_other_links = social_link

                            except:
                                agent_website_link = ''
                                agent_facebook_link = ''
                                agent_linkedin_link = ''
                                agent_twitter_link = ''
                                agent_pinterest_link = ''
                                agent_instagram_link = ''
                                agent_youtube_link = ''
                                agent_tiktok_link = ''
                                agent_other_links = ''

                            try:
                                phone_number = driver.find_element_by_id('adp-contact-box-details-container').find_element_by_tag_name(
                                    'a').text
                            except:
                                phone_number = ''

                            try:
                                deals_history_length = driver.find_element_by_id('transaction-history-tabs').find_elements_by_tag_name(
                                    'li')
                                deals_history_length = \
                                [i.text for i in deals_history_length if i.get_attribute('aria-selected') == 'true'][0].replace(' Year',
                                                                                                                                '')
                            except:
                                deals_history_length = ''

                            try:
                                deals_details = driver.find_element_by_id('transaction-history-panels')
                                transaction_history = deals_details.find_element_by_id(
                                    f'{deals_history_length}-year-panel').find_elements_by_class_name('detail-table-container')

                                seller_deals_total = ''
                                seller_deals_total_value = ''
                                seller_deals_average_sale_price = ''
                                seller_deals_price_range = ''

                                buyer_deals_total = ''
                                buyer_deals_total_value = ''
                                buyer_deals_average_sale_price = ''
                                buyer_deals_price_range = ''

                                for deal_details in transaction_history:
                                    deal_type = deal_details.find_element_by_tag_name('h3')
                                    deal_data = deal_details.find_elements_by_class_name('detail-table-row-content')

                                    if deal_type.text == 'Seller Deals':
                                        for deal_detail in deal_data:
                                            label = deal_detail.find_element_by_class_name('detail-table-data-label').text.strip()
                                            value = deal_detail.find_element_by_class_name('detail-table-data-value').text.strip()
                                            if label == 'Total Deals':
                                                seller_deals_total = value
                                            elif label == 'Total Value':
                                                seller_deals_total_value = value
                                            elif label == 'Average Sale Price':
                                                seller_deals_average_sale_price = value
                                            elif label == 'Price Range':
                                                seller_deals_price_range = value

                                    elif deal_type.text == 'Buyer Deals':
                                        for deal_detail in deal_data:
                                            label = deal_detail.find_element_by_class_name('detail-table-data-label').text.strip()
                                            value = deal_detail.find_element_by_class_name('detail-table-data-value').text.strip()
                                            if label == 'Total Deals':
                                                buyer_deals_total = value
                                            elif label == 'Total Value':
                                                buyer_deals_total_value = value
                                            elif label == 'Average Sale Price':
                                                buyer_deals_average_sale_price = value
                                            elif label == 'Price Range':
                                                buyer_deals_price_range = value

                            except:
                                seller_deals_total = ''
                                seller_deals_total_value = ''
                                seller_deals_average_sale_price = ''
                                seller_deals_price_range = ''

                                buyer_deals_total = ''
                                buyer_deals_total_value = ''
                                buyer_deals_average_sale_price = ''
                                buyer_deals_price_range = ''

                            try:
                                other_experiences = driver.find_element_by_class_name('other-experience-text').text
                            except:
                                other_experiences = ''

                            try:
                                agent_licence = driver.find_element_by_class_name('license-text').text.replace('Agent License',
                                                                                                               '').strip()
                            except:
                                agent_licence = ''

                            try:
                                awards_and_designations = driver.find_element_by_class_name(
                                    'adp-awards-designations-container').find_elements_by_tag_name('li')
                                awards_and_designations = '| '.join(i.text for i in awards_and_designations)
                            except:
                                awards_and_designations = ''

                            agent_names_list.append(agent_name)
                            agent_image_link_list.append(agent_image_url)
                            agent_location_list.append(agent_location)
                            office_name_list.append(agent_office_name)
                            star_ratings_list.append(agent_star_rating)
                            number_of_reviews_list.append(agent_number_of_reviews)
                            closed_sales_list.append(closed_sales)
                            total_value_list.append(total_value)
                            price_range_list.append(price_range)
                            average_price_list.append(average_price)
                            bio_list.append(bio)
                            home_types_list.append(home_types)
                            languages_spoken_list.append(languages_spoken)
                            years_of_experience_list.append(years_of_experience)
                            agent_website_link_list.append(agent_website_link)
                            agent_facebook_link_list.append(agent_facebook_link)
                            agent_linkedin_link_list.append(agent_linkedin_link)
                            agent_twitter_link_list.append(agent_twitter_link)
                            agent_pinterest_link_list.append(agent_pinterest_link)
                            agent_instagram_link_list.append(agent_instagram_link)
                            agent_youtube_link_list.append(agent_youtube_link)
                            agent_tiktok_link_list.append(agent_tiktok_link)
                            agent_other_link_list.append(agent_other_links)
                            phone_number_list.append(phone_number)
                            transaction_history_duration_list.append(deals_history_length)
                            seller_deals_total_list.append(seller_deals_total)
                            seller_deals_total_value_list.append(seller_deals_total_value)
                            seller_deals_average_sale_price_list.append(seller_deals_average_sale_price)
                            seller_deals_price_range_list.append(seller_deals_price_range)
                            buyer_deals_total_list.append(buyer_deals_total)
                            buyer_deals_total_value_list.append(buyer_deals_total_value)
                            buyer_deals_average_sale_price_list.append(buyer_deals_average_sale_price)
                            buyer_deals_price_range_list.append(buyer_deals_price_range)
                            other_experiences_list.append(other_experiences)
                            agent_licence_list.append(agent_licence)
                            awards_and_designations_list.append(awards_and_designations)
                            Agent_Profile_link_list.append(Agent_Profile_link)
                            Deals_in_agents_location_list.append(Deals_in_agents_location)
                            Price_range_in_agents_location_list.append(Price_range_in_agents_location)

                            driver.close()
                            driver.switch_to.window(driver.window_handles[0])
                            print(f'Extracted {city} | Page num {page_being_scrapped_number} | Agent {agent_name}')

                        except:
                            print(f'Error extracting {city} | Page num {page_being_scrapped_number} | Agent {agent_name} or next agent!!!')
                            time.sleep(4)

                    page_data_df = pd.DataFrame({
                        "Agent_Name": agent_names_list,
                        "Agent_Image_Link": agent_image_link_list,
                        'Agent_Profile_link': Agent_Profile_link_list,
                        "Agent_Location": agent_location_list,
                        "Office_Name": office_name_list,
                        "Star_Ratings": star_ratings_list,
                        "Number_Of_Reviews": number_of_reviews_list,
                        'Deals_in_agents_location': Deals_in_agents_location_list,
                        'Price_range_in_agents_location': Price_range_in_agents_location_list,
                        "Closed_Sales": closed_sales_list,
                        "Total_Value": total_value_list,
                        "Price_Range": price_range_list,
                        "Average_Price": average_price_list,
                        'Bio':bio_list,
                        "Home_Types": home_types_list,
                        "Languages_Spoken": languages_spoken_list,
                        "Years_Of_Experience": years_of_experience_list,
                        "Agent_Website_Link": agent_website_link_list,
                        "Agent_Facebook_Link": agent_facebook_link_list,
                        "Agent_Linkedin_Link": agent_linkedin_link_list,
                        "Agent_Twitter_Link": agent_twitter_link_list,
                        "Agent_Pinterest_Link": agent_pinterest_link_list,
                        "Agent_Instagram_Link": agent_instagram_link_list,
                        "Agent_Youtube_Link": agent_youtube_link_list,
                        "Agent_Tiktok_Link": agent_tiktok_link_list,
                        "Agent_Other_Link": agent_other_link_list,
                        "Phone_Number": phone_number_list,
                        "Transaction_History_Duration": transaction_history_duration_list,
                        "Seller_Deals_Total": seller_deals_total_list,
                        "Seller_Deals_Total_Value": seller_deals_total_value_list,
                        "Seller_Deals_Average_Sale_Price": seller_deals_average_sale_price_list,
                        "Seller_Deals_Price_Range": seller_deals_price_range_list,
                        "Buyer_Deals_Total": buyer_deals_total_list,
                        "Buyer_Deals_Total_Value": buyer_deals_total_value_list,
                        "Buyer_Deals_Average_Sale_Price": buyer_deals_average_sale_price_list,
                        "Buyer_Deals_Price_Range": buyer_deals_price_range_list,
                        "Other_Experiences": other_experiences_list,
                        "Agent_Licence": agent_licence_list,
                        "Awards_And_Designations": awards_and_designations_list})

                    main_df = pd.concat([main_df, page_data_df])

                    main_df.to_csv('data.csv', index=False)

                    next_page_button = driver.find_element_by_class_name('next')
                    next_page_button.click()
                    page_being_scrapped_number += 1
                    time.sleep(4)
            except:
                print(f'Error scraping page {page_being_scrapped_number} in {city}')
                time.sleep(4)
        except:
            print(f'Error scraping {city}')
            time.sleep(4)

except:
    print('Error running the program.')
    time.sleep(4)

time.sleep(50)
driver.quit()
