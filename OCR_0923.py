import pytesseract
import numpy as np
from PIL import Image
from Levenshtein import distance as lev
import os
import re

#輸出OCR文檔
def ocr(img_path):
    """
    img_path:image file direction
    """
    img_list=os.listdir(img_path)
    for i in img_list:
        img = Image.open(f"{img_path}{i}")
        img_big = img.resize([img.width*2,img.height*2])
        res = pytesseract.image_to_string(img_big)
        file_num= re.search("\d\d*",i).group()
        with open(f"./ocrtext/OCR{file_num}.txt","w",encoding="utf8") as f:
            f.write(res)

#單字層級：單字正確率+平均最小編輯距離(Levenshtein Distance)
def word_check(x,y):
    """
    input: 
    - x: origin text split list
    - y: OCR text split list
    """
    newline="\n"
    corr=0  #紀錄正確數
    wrong=0   #紀錄錯誤數
    arr=[]  #記錄最小編輯距離
    wrong_meg=[]
    for i in range(len(x)):
        try:
            if x[i]==y[i]:
                corr+=1
                arr.append(0)
            else:
                wrong+=1
                arr.append(lev(x[i],y[i]))
                wrong_meg.append(f"第{i}個單字轉換錯誤。原文:{x[i]}，OCR:{y[i]}，最小編輯距離為{arr[i]}{newline}")      
        except IndexError:
            print("轉換單字數無法匹配")
            break
    return(corr,wrong,arr,wrong_meg)

#文檔比對
def ocr_measure(ocr_path,text_path):
    """
    text_path: origin text direction
    ocr_path: ocr text direction
    """
    text_list=os.listdir(text_path)
    ocr_list=os.listdir(ocr_path)
    newline="\n"
    p_corr=0
    p_wrong=0
    p_arr=[]
    p_worng_meg=[]
    for i,j in zip(text_list,ocr_list):
        with open(f"{text_path}{i}", encoding='utf8') as t:
            txt=t.read()
        with open(f"{ocr_path}{j}", encoding='utf8') as o:
            ocr=o.read()
        ori_text=txt.split()
        ocr_text=ocr.split()
        w_corr, w_wrong, w_arr, w_wrong_meg = word_check(ori_text,ocr_text)  #取得文章正確單字數、錯誤單字數、最小編輯距離列表、翻譯錯誤訊息
        file_num= re.search("\d\d*",i).group()          #取得文章編號
        with open("wordmeasure_log.txt","a+",encoding="utf8") as f: #輸出檢測結果
            f.write(f"第{file_num}篇文檔{newline}{newline}")
            f.writelines(w_wrong_meg)
            f.write(f"{newline}共計 {len(ori_text)} 個字，正確 {w_corr} 個字，錯誤 {w_wrong} 個字；{newline}")
            f.write(f"正確率： {w_corr/len(ori_text)*100:.4f}%；{newline}")
            f.write(f"平均最小編輯距離：{np.average(w_arr)}{newline}")
            f.write("--------------------------------------------------------------\n")
        if w_wrong == 0 :
            p_corr+=1
        else:
            p_wrong+=1
            p_arr.append(sum(w_arr))
            p_worng_meg.append(f"第{file_num}篇文檔翻譯錯誤{newline}")
    with open("paragraphmeasure_log.txt","a+",encoding="utf8") as f: #輸出檢測結果
        f.write(f"共{len(text_list)}段文章，其中{newline}{newline}")
        f.writelines(p_worng_meg)
        f.write(f"{newline}總計正確 {p_corr} 篇文章，錯誤 {p_wrong} 篇文章；{newline}")
        f.write(f"正確率： {p_corr/len(text_list)*100:.4f}%；{newline}")
        f.write(f"平均最小編輯距離：{np.average(p_arr)}")



ocr("./data/image/")
ocr_measure("./ocrtext/","./data/text/")



    
    
    
    