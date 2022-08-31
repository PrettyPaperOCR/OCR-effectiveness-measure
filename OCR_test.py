import pytesseract
import numpy as np
from PIL import Image
import os

#單字正確率
def ocr_check(x,y):
    cor=0
    err=0
    for i in range(len(x)):
        try:
            if x[i]==y[i]:
                cor+=1
            else:
                print(f"第{i}個字發生錯誤。原文:{x[i]}，OCR:{y[i]}")
                err+=1
        except IndexError:
            print(f"第{i}個無法匹配")  
    print(f"共計 {len(x)} 個字，正確 {cor} 個字，錯誤 {err} 個字")     
    print(f"正確率： {cor/len(x)*100:.4f}%")

img_path="./data/image/"
img_list=os.listdir(img_path)
text_path="./data/text/"
text_list=os.listdir(text_path)

for i,j in zip(img_list,text_list):
    img = Image.open(f"./data/image/{i}")
    img_big = img.resize([img.width*2,img.height*2])
    with open(f"./data/text/{j}", encoding='utf8') as f:
        txt=f.read()
    res = pytesseract.image_to_string(img_big)
    x=txt.split()
    y=res.split()
    ocr_check(x,y)

#平均最小編輯距離(Levenshtein Distance)
from Levenshtein import distance as lev

img=Image.open("./data/image/img1.Jpg")
img_big=img.resize([img.width*2,img.height*2])
with open(f"./data/text/text1.txt", encoding='utf8') as f:
    txt=f.read()
res = pytesseract.image_to_string(img_big)
x=txt.split()
y=res.split()

arr=[]
for i,j in zip(x,y):
    arr.append(lev(i,j))
np.average(arr)



