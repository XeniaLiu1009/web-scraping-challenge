from splinter import Browser
from bs4 import BeautifulSoup
import time
from webdriver_manager.chrome import ChromeDriverManager
import pandas as pd


def scrape():
    # Set up Splinter
    executable_path = {'executable_path': ChromeDriverManager().install()}
    browser = Browser('chrome', **executable_path, headless=False)

    # Visit visitcostarica.herokuapp.com
    url = "https://redplanetscience.com"
    browser.visit(url)

    # Scrape page into Soup
    html = browser.html
    soup = BeautifulSoup(html,'html.parser')


    url2 = "https://spaceimages-mars.com"
    browser.visit(url2)

    # Scrape page into Soup
    html2 = browser.html
    soup2 = BeautifulSoup(html2,'html.parser')

    url3 = "https://galaxyfacts-mars.com"
    tables = pd.read_html(url3)

    url4 = "https://marshemispheres.com"
    browser.visit(url4)

    time.sleep(1)

    # Scrape page into Soup
    html4 = browser.html
    soup4 = BeautifulSoup(html4,'html.parser')

    #########################  NASA Mars News ############################

    # collect the latest news title
    new_title = soup.find_all("div",class_="content_title")[0].text
    # collect the latest news paragraph
    new_p = soup.find_all("div",class_="article_teaser_body")[0].text


    ################ JPL Mars Space Images - Featured Image ##############

    # collect the latest image
    picture = soup2.find_all("img",class_="thumbimg")[0]["src"]
    featured_imaged_url = 'https://spaceimages-mars.com/' + picture

    ###########################  Mars Facts ###############################
    
    # collect the table
    data_df = tables[0]
    # set header
    new_header = ["","Mars","Earth"] 
    data_df.columns = new_header
    # add the first row
    data_df = pd.DataFrame([["Description","",""]], columns=data_df.columns).append(data_df)
    # drop the index
    data_df = data_df.reset_index(drop=True)
    # save as HTML
    html_table = data_df.to_html()
    html_table = html_table.replace('\n','')
    # data_df.to_html('table.html',index = False, header = True)
    saved_html_string = data_df.to_html(index = False, header = True)
    
    #########################  Mars Hemispheres ##############################

    # collect the title and img_url
    queries = soup4.find_all("div",class_ = "item")
    titles = []
    img_urls = []
    for i in range(len(queries)):
        titles.append(queries[i].h3.text)
        img_urls.append("https://marshemispheres.com/" + queries[i].img["src"])

    hemisphere_image_urls = []
    for title, img_url in zip(titles,img_urls):
        hemisphere_image_url = {'title':title,'img_url':img_url}
        hemisphere_image_urls.append(hemisphere_image_url)


    mars_data = {
        "new_title" : new_title,
        "new_p" : new_p,
        "featured_imaged_url" : featured_imaged_url,
        "hemisphere_image_urls" : hemisphere_image_urls
        # "saved_html_string" : saved_html_string
    }

    # print(mars_data["featured_imaged_url"])
    # Close the browser after scraping
    browser.quit()

    # Return results
    return mars_data