from selenium import webdriver
import time
import pandas as pd

def features():
    driver = webdriver.Chrome(r"C:\Users\mkart\OneDrive\Documents\Python\Mysore_Real_Estate_Price\chromedriver_win32\chromedriver.exe")
    location_list = []
    area_list = []
    price_list = []
    beds_list = []
    driver.get('https://www.99acres.com/property-in-mysore-ffid?property_type=1,4,2,5')
    time.sleep(2)
    total_pages_element = driver.find_element_by_class_name('Pagination__srpPagination')
    print(total_pages_element)
    print(total_pages_element.text)
    total_pages = total_pages_element.text
    total_pages = total_pages.split('\n')[0]
    total_pages = total_pages.split('of')[1]
    

    for n in range(len(total_pages)):
        driver.get(f'https://www.99acres.com/property-in-mysore-ffid-page-{n+1}?property_type=1,4,2,5')
        time.sleep(4)
        location = driver.find_elements_by_class_name('srpTuple__propertyName') # returns all the elements that corresponds to the class name as a list
        price = driver.find_elements_by_id('srp_tuple_price')
        beds = driver.find_elements_by_id('srp_tuple_bedroom')
        area = driver.find_elements_by_id('srp_tuple_primary_area')

        if len(location) == len(price) == len(beds) == len(area): # Just making sure if the row values matches with the corresponsing row-column data

            for i in range(len(price)):
                location_list.append(location[i].text)
                beds_list.append(beds[i].text)
                price_list.append(price[i].text)
                area_list.append(area[i].text)
            
    return location_list,area_list,beds_list,price_list


if __name__ == __main__:

    location_list,area_list,beds_list,price_list = features()
    # Creates a dictionary of the lists generated to create a Pandas DataFrame and then save it to CSV
    data_dict = {}
    data_dict['location'] = location_list
    data_dict['beds'] = beds_list
    data_dict['price'] = price_list
    data_dict['area'] = area_list
    df1 = pd.DataFrame(data_dict)
    data_combined.to_csv('data.csv',index=False)

