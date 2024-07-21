import requests
from bs4 import BeautifulSoup
from selenium import webdriver
from datetime import datetime as dtime


# 動態網頁爬蟲
url = "https://www.cwa.gov.tw/V8/C/W/OBS_Map.html"
driver = webdriver.Chrome()
driver.get(url)
soup = BeautifulSoup(driver.page_source, "html.parser")

# 時間資訊
data_time = soup.find("span", id="preestimate").text      # 資料時間

# 天氣資訊
city_weather = {}
for i in [63, 65]:  # 台北、新北
    city = soup.find("a", id = i)   # 天氣資訊(地點+溫度)
    weather_src = "https://www.cwa.gov.tw" + city.find("img").get("src")    # 天氣狀況(src)
    city_weather[city.text.split()[1]] = [city.text.split()[0] +
                                          "°C "] + [city.find("img").get("alt")] + [weather_src]
    # 完整內容 - {地點 : 溫度 + 天氣 + 天氣狀況src}

# 內容轉字串
city_weather_str = f"{'':.<51}"
for i in city_weather:
    city_weather_str += f"\n> {i} {city_weather[i][0]} {city_weather[i][1]}"
# print(city_weather_str)

driver.close()


# ------------------------------------
# 動態網頁爬蟲2

url = ["https://www.cwa.gov.tw/V8/C/W/County/County.html?CID=63",
       "https://www.cwa.gov.tw/V8/C/W/County/County.html?CID=65"]

# 現在時間
# now_time = "現在時間：{:%m/%d %H:%M}".format(dtime.now())
# print(now_time)

weather_str = {}
for i in url:
    driver = webdriver.Chrome()
    driver.get(i)
    soup = BeautifulSoup(driver.page_source, "html.parser")

    # 地點
    city = soup.find("h2", class_="main-title").text[-3:]
    # print(f"{city}")

    str = f"{city}\n"   # 字串+地點
    all_weather = soup.select("div.d-xl-none.d-block ul.to-to li")   # 完整天氣資訊
    for i in all_weather:
        time = i.find("span", class_="title").get("title")  # 時間
        time_str = i.find("span").text   # 時間2
        weather = i.find("img").get("title")   # 天氣
        temp = i.find("span", class_="tem-C is-active").text + "°C"   # 溫度
        rain = i.find("span", class_="rain").text   # 降雨機率
        text = i.find("span", class_="text").text   # 舒適度
        str += f"\n{time_str:.^40}\n{time[:13]} {time[-5:]}\n"
        str += f"> {temp}  {weather}\n"
        str += f"> {rain[:-3]} {rain[-3:]}\n"
        str += f"> {text}\n"
            
    weather_str[city] = str

# for i in weather_str:
#     print(weather_str[i])
    
driver.close()


#%% Line Notify

def notify(token, msg, image):
    url = "https://notify-api.line.me/api/notify"
    header = {"Authorization": "Bearer " + token}
    payload = {"message": msg,
               "stickerPackageId": "",
               "stickerId": ""}
    imageFile = "" #{"imageFile": image}
    requests.post(url, headers=header, params=payload, files=imageFile)

# ------------------------------------

# token = "41hF4UDuJbS5pL099yf2dCTsBNybY6ecru7ZUawCr2d" #個人
# token = "3ggLP45OVB9MI3IXaKvH6UNPYxgIfDrCBDEVPVIhHCq" #群組
token= ["3ggLP45OVB9MI3IXaKvH6UNPYxgIfDrCBDEVPVIhHCq"]

now_time = "現在時間：{:%m/%d %H:%M}".format(dtime.now())  # 現在時間
for i in range(len(token)):
    msg = f"天氣\n{now_time}\n{data_time}\n"
    msg += f"{city_weather_str}"
    # img_path = r"C:\Users\User\Desktop\Notify\Pic\14.png"
    img = "" #open(img_path, "rb")
    notify(token[i], msg, img)

for i in range(len(token)):
    for j in weather_str:
        msg = weather_str[j]
        # img_path = r"C:\Users\User\Desktop\Notify\Pic\14.png"
        img = ""  #open(img_path, "rb")
        notify(token[i], msg, img)

# 貼圖--https://developers.line.biz/en/docs/messaging-api/sticker-list/


