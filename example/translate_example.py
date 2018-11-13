import json
import urllib.request as urllib2
import hashlib

def md5(str):#生成md5
    m = hashlib.md5()
    m.update(str)
    return m.hexdigest()

def en_to_zh(src):#英译中
    ApiKey = "20180822000197654"
    pwd = "vO7s3NHf0My7tmAkZFbs"
    salt = "1435660288"
    all = ApiKey + src + salt + pwd
    sign = md5(all)
    src=src.replace(' ','+')#生成sign前不能替换
    url = "http://api.fanyi.baidu.com/api/trans/vip/translate?q="\
          + src + "&from=en&to=zh&appid=" + ApiKey + \
          "&salt=" + salt + "&sign=" + sign
    try:
        req = urllib2.Request(url)
        con = urllib2.urlopen(req)
        res = json.load(con)
        if 'error_code' in res:
            print('error:', res['error_code'])
            return res['error_msg']
        else:
            dst = res['trans_result'][0]['dst']
            return dst
    except:
        return "出错了"

def zh_to_en(src):#中译英
    ApiKey = "20180822000197654"
    pwd = "vO7s3NHf0My7tmAkZFbs"
    salt = "1435660288"
    all = ApiKey + src + salt + pwd
    sign = md5(all)
    src=src.replace(' ','+')#生成sign前不能替换
    url = "http://api.fanyi.baidu.com/api/trans/vip/translate?q="\
          + src + "&from=zh&to=en&appid=" + ApiKey + \
          "&salt=" + salt + "&sign=" + sign
    try:
        req = urllib2.Request(url)
        con = urllib2.urlopen(req)
        res = json.load(con)
        return res['trans_result'][0]['dst']
    except:
        return "出错了"

def main():
    choice = input("English to Chinese:Enter 1 \n"
                      "Chinese to English:Enter 2 \n"
                      "Enter:")
    if choice == "1":
        while True:
            word = input("Input the word you want to search:")
            print("translate......")
            target = en_to_zh(word)
            print(target)
    else:
        while True:
            word = input("Input the word you want to search:")
            print("translate......")
            target = zh_to_en(word)
            print(target)

if __name__ == '__main__':
    main()
