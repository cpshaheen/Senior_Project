import os
import bs4
import requests
import time
import urllib.request
from urllib.request import build_opener, HTTPError, HTTPCookieProcessor, Request
from bs4 import BeautifulSoup as bsoup
from http.cookiejar import CookieJar
from random import seed
from random import randint

OUTER_DIR = "/clothing_classes"

def make_dir(path_from_cwd):
    cwd = os.getcwd()
    x_imgs_folder = cwd+path_from_cwd
    if(not os.path.exists(x_imgs_folder)):
        os.mkdir(x_imgs_folder)
    return cwd+path_from_cwd

def make_outer_dir():
    # this is the folder that will hold the outer directory
    cwd = os.getcwd()
    clothing_imgs_folder = cwd+OUTER_DIR
    if(not os.path.exists(clothing_imgs_folder)):
        os.mkdir(clothing_imgs_folder)

def scrape_macys_all(page_num):
    # this is the folder that will hold the images

    clothing_imgs_folder = make_dir(OUTER_DIR+"/clothing_images")
    items_and_img_links = scrape_macys_men_cat(
            "https://www.macys.com/shop/mens-clothing/all-mens-clothing/Pageindex/",
            "?id=197651",
            page_num)


    print(items_and_img_links)
    print(len(items_and_img_links))

    # this loop will save all the images with the item titles as their image name
    for item in items_and_img_links:
        item_img_name = item[0].replace("/", "") +".jpg"
        urllib.request.urlretrieve(item[1], clothing_imgs_folder+"/"+item_img_name)

# refactoring 
#function to scrape a specific men's macys category 
def scrape_macys_men_cat(url_1,url_2,numpgs):
    # these two strings are used in the for loop with the iterator variable to specifiy each page#
    main_url_pt1 = url_1
    main_url_pt2 = url_2
    print(main_url_pt1+main_url_pt2)

    # this array/list is to hold tuples of item names and their image urls
    items_and_img_links = []

    seed(1)
    for i in range(1,numpgs+1):
        time.sleep(randint(1,10))
        print("page#"+str(i))
        url = main_url_pt1 + str(i) + main_url_pt2
        response = requests.get(url, headers={"User-Agent":"Mozilla/5.0"}, timeout=5)
        # the following line gets the html page
        content = bsoup(response.content, "html.parser")
        # this line searches for the "li" items which correspond to the actual clothing items
        containers = content.findAll("li",{"class":"cell productThumbnailItem"})
        # this loops over all the items and extracts their names and the src link to their image
        # and then appends the tuple of both to 'items_and_img_links'
        for item in containers:
            item_title = item.div.div.a["title"]
            item_img_link = item.div.div.a.img["src"]
            item_img_link = item_img_link[:item_img_link.index('$')]
            items_and_img_links.append((item_title,item_img_link))

    print(items_and_img_links)
    print(len(items_and_img_links))
    return items_and_img_links


def scrape_macys_blazers_and_sports_coats(page_num):
    sport_coat_imgs_folder = make_dir(OUTER_DIR+"/sport_coats")
    blazer_imgs_folder = make_dir(OUTER_DIR+"/blazers")

    # these two strings are the split up sweatshirts category
    # these two are used in the for loop with the iterator variable to specifiy each page#
    items_and_img_links = scrape_macys_men_cat(
            "https://www.macys.com/shop/mens-clothing/mens-blazers-sports-coats/Pageindex,Sortby/",
            ",BEST_SELLERS?id=16499",
            page_num)

    # this loop will save all the images with the item titles as their image name
    for item in items_and_img_links:
        item_img_name = item[0].replace("/", "") +".jpg"
        if("Sport Coat" in item_img_name):
            urllib.request.urlretrieve(item[1], sport_coat_imgs_folder+"/"+item_img_name)
        if("Blazer" in item_img_name):
            urllib.request.urlretrieve(item[1], blazer_imgs_folder+"/"+item_img_name)

def scrape_macys_pants(page_num):
    sweatpants_imgs_folder = make_dir(OUTER_DIR+"/sweatpants")
    pants_imgs_folder = make_dir(OUTER_DIR+"/pants")

    # these two strings are the split up sweatshirts category
    # these two are used in the for loop with the iterator variable to specifiy each page#
    items_and_img_links = scrape_macys_men_cat(
            "https://www.macys.com/shop/mens-clothing/mens-pants/Pageindex,Sortby/",
            ",BEST_SELLERS?id=89",
            page_num)

    # this loop will save all the images with the item titles as their image name
    for item in items_and_img_links:
        item_img_name = item[0].replace("/", "") +".jpg"
        if("sweat" in item_img_name.lower() or "jog" in item_img_name.lower()):
            urllib.request.urlretrieve(item[1], sweatpants_imgs_folder+"/"+item_img_name)
        else:
            urllib.request.urlretrieve(item[1], pants_imgs_folder+"/"+item_img_name)


def scrape_macys_coats_and_jackets(num_pgs):
    coats_imgs_folder = make_dir(OUTER_DIR+"/coats")
    jackets_imgs_folder = make_dir(OUTER_DIR+"/jackets")
    items_and_img_links = scrape_macys_men_cat("https://www.macys.com/shop/mens-clothing/mens-jackets-coats/Pageindex,Sortby/",
                                                ",BEST_SELLERS?id=3763",
                                                num_pgs)

    # this loop will save all the images with the item titles as their image name
    for item in items_and_img_links:
        item_img_name = item[0].replace("/", "") +".jpg"
        if("coat" in item_img_name.lower()):
            urllib.request.urlretrieve(item[1], coats_imgs_folder+"/"+item_img_name)
        if("jacket" in item_img_name.lower()):
            urllib.request.urlretrieve(item[1], jackets_imgs_folder+"/"+item_img_name)


def scrape_macys_sweatshirts_and_hoodies(num_pgs):
    sweatshirt_imgs_folder = make_dir(OUTER_DIR+"/sweatshirts")
    hoodie_imgs_folder = make_dir(OUTER_DIR+"/hoodies")
    items_and_img_links = scrape_macys_men_cat("https://www.macys.com/shop/mens-clothing/hoodies-for-men/Pageindex,Sortby/",
                                                ",BEST_SELLERS?id=25995",
                                                num_pgs)

    # this loop will save all the images with the item titles as their image name
    for item in items_and_img_links:
        item_img_name = item[0].replace("/", "") +".jpg"
        if("Hood" in item_img_name):
            urllib.request.urlretrieve(item[1], hoodie_imgs_folder+"/"+item_img_name)
        else:
            urllib.request.urlretrieve(item[1], sweatshirt_imgs_folder+"/"+item_img_name)

def scrape_macys_jeans(num_pgs):
    jeans_imgs_folder = make_dir(OUTER_DIR+"/jeans")
    items_and_img_links = scrape_macys_men_cat("https://www.macys.com/shop/mens-clothing/mens-clothing/Pageindex,Sortby/",
                                                ",BEST_SELLERS?id=11221",
                                                num_pgs)

    # this loop will save all the images with the item titles as their image name
    for item in items_and_img_links:
        item_img_name = item[0].replace("/", "") +".jpg"
        urllib.request.urlretrieve(item[1], jeans_imgs_folder+"/"+item_img_name)

def scrape_macys_tshirts(num_pgs):
    tshirt_imgs_folder = make_dir(OUTER_DIR+"/tshirts")
    longsleeve_imgs_folder = make_dir(OUTER_DIR+"/longsleeve_tshirts")
    items_and_img_links = scrape_macys_men_cat("https://www.macys.com/shop/mens-clothing/mens-t-shirts/Pageindex,Sortby/",
                                                ",BEST_SELLERS?id=30423",
                                                num_pgs)
    for item in items_and_img_links:
        item_img_name = item[0].replace("/", "") +".jpg"
        if(("t-shirt" in item_img_name.lower())
            and (not("long" in item_img_name.lower())) 
            and (not("hood" in item_img_name.lower()))):
            
            urllib.request.urlretrieve(item[1], tshirt_imgs_folder+"/"+item_img_name)

        elif("long" in item_img_name.lower() and (not ("hood" in item_img_name.lower()))):
            urllib.request.urlretrieve(item[1], longsleeve_imgs_folder+"/"+item_img_name)


def scrape_macys_shortsleeve_button_ups(num_pgs):
    button_up_imgs_folder = make_dir(OUTER_DIR+"/short_sleeve_button_ups")
    items_and_img_links = scrape_macys_men_cat("https://www.macys.com/shop/mens-clothing/mens-shirts/Mens_product_type,Sleeve_length,Pageindex/Casual%20Shirts%7CDress%20Shirts,Short%20Sleeve,", 
        "?id=20626",
        num_pgs)
    
    for item in items_and_img_links:
        item_img_name = item[0].replace("/", "") +".jpg"
        if(not("t-shirt" in item_img_name.lower())):
            urllib.request.urlretrieve(item[1], button_up_imgs_folder+"/"+item_img_name)
    
def scrape_macys_longsleeve_button_ups(num_pgs):
    button_up_imgs_folder = make_dir(OUTER_DIR+"/long_sleeve_button_ups")
    items_and_img_links = scrape_macys_men_cat("https://www.macys.com/shop/mens-clothing/mens-shirts/Mens_product_type,Sleeve_length,Pageindex,Sortby/Casual%20Shirts%7CDress%20Shirts,Long%20Sleeve,",
        ",BEST_SELLERS?id=20626",
        num_pgs)
    
    for item in items_and_img_links:
        item_img_name = item[0].replace("/", "") +".jpg"
        if(not("t-shirt" in item_img_name.lower())):
            urllib.request.urlretrieve(item[1], button_up_imgs_folder+"/"+item_img_name)


def scrape_macys_polos(num_pgs):
    polo_imgs_folder = make_dir(OUTER_DIR + "/polos")
    items_and_img_links = scrape_macys_men_cat(
        "https://www.macys.com/shop/mens-clothing/mens-polo-shirts/Pageindex,Sortby/",
        ",BEST_SELLERS?id=20640",
        num_pgs)

    for item in items_and_img_links:
        item_img_name = item[0].replace("/", "") +".jpg"
        urllib.request.urlretrieve(item[1], polo_imgs_folder+"/"+item_img_name)

def scrape_macys_active_shorts(num_pgs):
    active_shorts_imgs_folder = make_dir(OUTER_DIR + "/active_shorts")
    items_and_img_links = scrape_macys_men_cat("https://www.macys.com/shop/mens-clothing/mens-shorts/Short_style,Pageindex,Sortby/Active%7CSweat%20Shorts,",
        ",BEST_SELLERS?id=3310",
        num_pgs)

    for item in items_and_img_links:
        item_img_name = item[0].replace("/", "") +".jpg"
        urllib.request.urlretrieve(item[1], active_shorts_imgs_folder+"/"+item_img_name)

def scrape_macys_shorts(num_pgs):
    shorts_imgs_folder = make_dir(OUTER_DIR + "/shorts")
    items_and_img_links = scrape_macys_men_cat(
        "https://www.macys.com/shop/mens-clothing/mens-shorts/Short_style,Pageindex,Sortby/Cargo%7CChino%7CDenim%7CHybrid,",
        ",BEST_SELLERS?id=3310",
        num_pgs)

    for item in items_and_img_links:
        item_img_name = item[0].replace("/","") + ".jpg"
        urllib.request.urlretrieve(item[1], shorts_imgs_folder+"/"+item_img_name)

def scrape_macys_tuxs_and_suits(num_pgs):
    tuxs_img_folder = make_dir(OUTER_DIR + "/tuxedos")
    suits_img_folder = make_dir(OUTER_DIR + "/suits")
    suit_jacket_img_folder = make_dir(OUTER_DIR + "/suit_jackets")
    suit_pant_img_folder = make_dir(OUTER_DIR + "/suit_pants")

    items_and_img_links = scrape_macys_men_cat(
        "https://www.macys.com/shop/mens-clothing/mens-suits/Pageindex/", 
        "?id=17788",
        num_pgs)
    
    for item in items_and_img_links:
        item_img_name = item[0].replace("/","") + ".jpg"
        if("tux" in item_img_name.lower()):
            urllib.request.urlretrieve(item[1], tuxs_img_folder+"/"+item_img_name)
        elif("pants" in item_img_name.lower() or "bottom" in item_img_name.lower()):
            urllib.request.urlretrieve(item[1], suit_pant_img_folder+"/"+item_img_name)
        elif("jacket" in item_img_name.lower() or "top" in item_img_name.lower()):
            urllib.request.urlretrieve(item[1], suit_jacket_img_folder+"/"+item_img_name)
        elif("suit" in item_img_name.lower()):
            urllib.request.urlretrieve(item[1], suits_img_folder+"/"+item_img_name)

def scrape_macys_sweaters(num_pgs):
    sweater_img_folder = make_dir(OUTER_DIR + "/sweater")
    hoodie_img_folder = make_dir(OUTER_DIR + "/hoodies")

    items_and_img_links = scrape_macys_men_cat(
        "https://www.macys.com/shop/mens-clothing/mens-sweaters/Pageindex/",
        "?id=4286",
        num_pgs)

    for item in items_and_img_links:
        item_img_name = item[0].replace("/","") + ".jpg"
        if("hood" in item_img_name.lower()):
            urllib.request.urlretrieve(item[1], hoodie_img_folder+"/"+item_img_name)
        else:
            urllib.request.urlretrieve(item[1], sweater_img_folder+"/"+item_img_name)

def main():
    make_dir(OUTER_DIR)
    scrape_macys_coats_and_jackets(2) # max pg num is 26
    # scrape_macys_sweatshirts_and_hoodies(2) # max pg num is 24
    # scrape_macys_blazers_and_sports_coats(2) # max pg num is 11
    # scrape_macys_jeans(2) # max pg num is 11
    # scrape_macys_pants(2) # max pg num is 23
    # scrape_macys_longsleeve_button_ups(23) #max pg num is 23
    # scrape_macys_shortsleeve_button_ups(11) # max pg num is 11
    # scrape_macys_tshirts(2) # max pg num is 93
    # scrape_macys_polos(2) # max pg num is 11
    # scrape_macys_active_shorts(2) # max pg num is 5
    # scrape_macys_shorts(2) # max pg num is 2
    # scrape_macys_tuxs_and_suits(2) # max pg num is 16
    # scrape_macys_sweaters(2) # max pg num is 10

main()