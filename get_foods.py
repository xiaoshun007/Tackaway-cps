#coding:utf-8

# 目标网页 https://www.meishij.net/zuofa/nongjiaxiaochaorou_59.html

import json
import random
import sys
import urllib.request
from bs4 import BeautifulSoup 

categories = ["家常菜", "快手菜", "下饭菜"]
time_zone = ["午餐", "晚餐", "夜宵"]
likes = ["明目"]
url = "https://www.meishij.net/shiliao.php?st=3&cid=212&sortby=update&page="

def down(url):
    return  urllib.request.urlopen(url).read()#读取全部网页


def extract(content, food_id):
    try:
        food = {}
        soup = BeautifulSoup(content, "html.parser")
        
        food["_id"] = str(food_id)
        food["id"] = str(food_id)
        food["desc"] = soup.select(".author_words")[0].select("p")[0].text
        food["title"] = soup.select(".recipe_title")[0].text
        food["category"] = [food["title"], categories[random.randint(0, len(categories)-1)], time_zone[random.randint(0, len(time_zone)-1)], likes[random.randint(0, len(likes)-1)]]
        food["count"] = random.randint(100, 1000)

        # 展示图
        food["albums"] = []
        for album in soup.select(".recipe_topimgw")[0].select("img"):
            food["albums"].append(album.get("src"))

        # 步骤
        steps = soup.select("#app > div.main > div.main_left > div.recipe_step_box > div.recipe_step")
        print(len(steps))
        food["steps"] = []
        for i in range(0, len(steps)):
            step_content = "#app > div.main > div.main_left > div.recipe_step_box > div:nth-child(" + str(i + 1) + ") > div.step_content > p"
            print("step:" + step_content)
            print(soup.select("#app > div.main > div.main_left > div.recipe_step_box > div:nth-child(1) > div.step_content > p"))
            step_img = "#app > div.main > div.main_left > div.recipe_step_box > div:nth-child(" + str(i + 1) + ") > div.step_content > img"
            print(soup.select(step_img)[0].get("src"))
            step_dict = {
                "step": soup.select(step_content)[0].text,
                "img": soup.select(step_img)[0].get("src")
            }

            food["steps"].append(step_dict)

        # 主料
        food["ingredients"] = ""
        ingredients = soup.select("#app > div.recipe_header > div > div.recipe_header_info > div.recipe_ingredientsw > div:nth-child(1) > div.right > strong")
        for i in range(0, len(ingredients)):
            ingredient = "#app > div.recipe_header > div > div.recipe_header_info > div.recipe_ingredientsw > div:nth-child(1) > div.right > strong:nth-child(" + str(i + 1) + ")"
            ingredient_name = soup.select(ingredient)[0].text
            food["ingredients"] = food["ingredients"] + ingredient_name + ";"

        # 辅料
        food["burden"] = ""
        burdens = soup.select("#app > div.recipe_header > div > div.recipe_header_info > div.recipe_ingredientsw > div.recipe_ingredients.recipe_ingredients1 > div.right > strong")
        for i in range(0, len(burdens)):
            burden = "#app > div.recipe_header > div > div.recipe_header_info > div.recipe_ingredientsw > div.recipe_ingredients.recipe_ingredients1 > div.right > strong:nth-child(" + str(i + 1) + ")"
            burden_usage = soup.select(burden)[0].text
            food["burden"] = food["burden"] + burden_usage + ";"
    except Exception as ex:
        print(ex)
    return food


def get_detail_url(url):
    soup = BeautifulSoup(down(url), "html.parser")
    detail_urls = []
    for a in soup.select(".listtyle1"):
        detail_urls.append(a.select("a")[0].get("href"))
    return detail_urls

def write2file(path, food):
    f = open(path, 'a')
    f.write('\n' + food)
    f.close()



# 起始id
food_id = 312
page = 1
for i in range(1, page + 1):
    detail_urls = get_detail_url(url + str(i))
    for detail_url in detail_urls:
        food_id += 1
        print(detail_url)
        print(food_id)
        try:
            write2file("/Users/san/githubDownload/pythoncrawler/foods_mingmu.json", json.dumps(extract(down(detail_url), food_id), ensure_ascii=False))
        except Exception as ex:
            print(ex)
            continue







