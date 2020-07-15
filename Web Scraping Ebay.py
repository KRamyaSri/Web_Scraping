#importing required libraries
import requests
from bs4 import BeautifulSoup
import pandas as pd

def web_scraping(pageno):
    #declaration of headers variable
    headers = {"User-Agent":"Mozilla/5.0 (Windows NT 10.0; Win64;     x64; rv:66.0) Gecko/20100101 Firefox/66.0", "Accept-Encoding":"gzip, deflate",     "Accept":"text/html,application/xhtml+xml,application/xml;q=0.9,*/*;q=0.8", "DNT":"1","Connection":"close", "Upgrade-Insecure-Requests":"1"}

    #creating url variable which gets the feedback link
    url = requests.get("https://www.ebay.com/fdbk/feedback_profile/littlekitty0103?filter=feedback_page:All&page_id="+str(pageno)+"&limit=200",headers=headers)
    #extracting content from the url variable
    content = url.content
    #creating soup object for the content 
    soup = BeautifulSoup(content,features="html.parser")

    #getting feedbacks and products data from the site by calling feedbacks_and_products_data(soup) function
    feedbacks_and_products_data(soup)
    #getting seller data from site by calling seller_data(soup) function
    seller_data(soup)
    #getting prices data from site by calling prices_data(soup) function
    prices_data(soup)

def feedbacks_and_products_data(soup):
    '''this loop here will get all the feedbacks along with product names
    the parent tag is <div class='card__feedback-container'> for both feedback and product
    the child tag for feedback is <div class='card__comment'>
    the child tag for product is <div class='card__item'>'''
    for tags in soup.findAll('div', attrs={'class':'card__feedback-container'}):
        feedback = tags.find('div', attrs={'class':'card__comment'})
        product = tags.find('div', attrs={'class':'card__item'})
        if feedback is not None:
            feedbacks.append(feedback.text)
        else:
            feedbacks.append("feedback-not-given")
        if product is not None:
            products.append(product.text)
        else:
            products.append('product-name-not-known')

def seller_data(soup):
    '''the loop below helps us to get all the seller names from the site
    the parent tag is <td>
    the child tag is <div class='card__from'>'''
    for tags in soup.findAll('td'):
        #price = d.find('div', attrs={'class':'card__price'})
        seller = tags.find('div', attrs={'class':'card__from'})
        if seller is not None:
            sellers.append(seller.text)

def prices_data(soup):
    #getting all tr tags
    trTags=soup.findAll('tr')
    #getting required tr tags for the extraction of prices
    #we dont need first 9 tags and last 2 tags
    trTags=trTags[9:]
    trTags=trTags[:-2]

    '''loop for extracting prices from the site
    the parent tag is <tr>
    the child tag is <div class='card__price'>
    we have some extra rows which need to be ignored
        the tags of these unwanted rows are <span data-test-id='card-notice-info'> and <div class='reply__container'>
    '''    
    for tags in trTags:
        if tags.find('span', attrs={'data-test-id':'card-notice-info'}) or tags.find('div', attrs={'class':'reply__container'}):
            continue
        price=tags.find('div', attrs={'class':'card__price'})
        if price is not None:
            prices.append(price.text)
        else:
            prices.append("price-not-given")

if __name__=='__main__':
    #declaring lists for stoting extracted data
    feedbacks=[]
    prices=[]
    sellers=[]
    products=[]

    '''we need to get data of 7 pages in the site.
    so we will call the web-scraping function 7 times
    the url page-no will be given as a parameter'''
    page_numbers=[1,2,3,4,5,6,7]
    for page_number in page_numbers:
        web_scraping(pageno=page_number)

    #exporting the data as csv file
    #combining lists into a dataframe
    dataFrame = pd.DataFrame({'Feedback':feedbacks, 'Product':products, 'Price':prices, 'Seller':sellers}) 
    #exporting dataframe as a csv file
    dataFrame.to_csv('ebay.csv', index=False, encoding='utf-8')