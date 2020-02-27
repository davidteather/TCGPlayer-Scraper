from selenium import webdriver
import xlsxwriter
import io
import requests
import time
import shutil
import os

driver = webdriver.Chrome()

workbook = xlsxwriter.Workbook('output.xls') 
worksheet = workbook.add_worksheet() 

worksheet.set_column('A:A', 10)
worksheet.set_column('B:B', 20)
worksheet.set_column('C:C', 50)
worksheet.set_column('D:E', 10)

worksheet.write("A1", "Link")
worksheet.write("B1", "Thumbnail Photo")
worksheet.write("C1", "Photo Title")
worksheet.write("D1", "Listing URL")
worksheet.write("E1", "Link to thumbnail")
worksheet.write("F1", "Price")

if not os.path.isdir("tmp"):
    os.mkdir("tmp")


global rowCount
rowCount = 2

def scrapeURL(url):
    global rowCount
    driver.get(url)
    time.sleep(3)

    driver.execute_script("scrollTo(0, 1500);")
    time.sleep(2)

    driver.find_element_by_xpath("//button[@data-toggle='show-filters']").click()
    time.sleep(2)

    for selection in driver.find_elements_by_xpath("//li[@class='filter-facet__item ']"):
        if selection.text.strip() == "Listings With Photos":
            selection.click()

    time.sleep(5)

    driver.find_element_by_xpath("//button[@data-toggle='hide-filters']").click()

    time.sleep(2)

    pageNum = 1
    contin = True
    while contin:
        time.sleep(5)
        loops = 0
        for listing in driver.find_elements_by_xpath("//section[@class='product-listings']/div"):
            photoUrl = driver.find_elements_by_xpath("//section[@class='product-listings']/div/a/figure/img")[loops].get_attribute("src")
            title = driver.find_elements_by_xpath("//section[@class='product-listings']/div/div[@class='product-listing__condition']/a[@class='product-listing__photo-title']")[loops].text.strip()
            listingUrl = driver.find_elements_by_xpath("//section[@class='product-listings']/div/a")[loops].get_attribute("href")
            price = driver.find_elements_by_xpath("//section[@class='product-listings']/div/div[@class='product-listing__pricing']/span[@class='product-listing__price']")[loops].text.strip()

            r = requests.get(photoUrl)

            

            with open("tmp/tmp" + str(rowCount) + ".png", 'wb') as obj:
                obj.write(r.content)

            worksheet.set_row(rowCount-1, 150)
            worksheet.write('B' + str(rowCount), '.')
            worksheet.insert_image('B' + str(rowCount), 'tmp/tmp' + str(rowCount) + '.png')

            

            worksheet.write("A" + str(rowCount), url)
            worksheet.write("C" + str(rowCount), title)
            worksheet.write("D" + str(rowCount), listingUrl)
            worksheet.write("E" + str(rowCount), photoUrl)
            worksheet.write("F" + str(rowCount), price)

            rowCount += 1

            loops += 1

        try:
            action = webdriver.common.action_chains.ActionChains(driver)
            height = driver.find_element_by_xpath("//a[@class=' nextPage']").location
            driver.execute_script("scrollTo(0, " + str(height["y"]) + ");")
            action.move_to_element(driver.find_element_by_xpath("//a[@class=' nextPage']")).click().perform()
    
        except:
            contin = False

    


with open("searchUrls.txt", 'r') as obj:
    urls = obj.readlines()

for url in urls:
    scrapeURL(url.replace("\n", ""))


workbook.close()
driver.quit()

shutil.rmtree("tmp")