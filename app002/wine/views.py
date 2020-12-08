from django.shortcuts import render, redirect
from django.views.decorators.csrf import csrf_exempt
import numpy as np
import pandas as pd
from sklearn.neighbors import KNeighborsClassifier
from wine.models import Winenara_temp, Wine21_temp

import pymysql
from sqlalchemy import create_engine

engine = create_engine('mysql://root:12345@localhost/wine1?charset=utf8', encoding = 'utf-8')
conn = engine.connect()
    
winenaradf = pd.read_sql_table('wine_winenara', conn)

conn.close()




def home(request):
    return render(request, 'main.html') 

def createtemp1(df):
    engine = create_engine('mysql://root:12345@localhost/wine1?charset=utf8', encoding = 'utf-8')
    conn = engine.connect()
    df.to_sql(name='wine_winenara_temp', con=engine,if_exists='replace') 
    conn.close()
    dto = Winenara_temp.objects.order_by('idx') 
    return dto

    
     

@csrf_exempt
def winenara_search(request):
    
    x = int(request.POST['dang'])
    y = int(request.POST['san'])
    z = int(request.POST['body'])
    price = request.POST['price']
     
    if price =='a':
        select_price=winenaradf.loc[winenaradf.price<=30000]
    elif price =='b':
        select_price=winenaradf.loc[(winenaradf.price>=30000) & (winenaradf.price<=70000)]
    elif price =='c':
        select_price=winenaradf.loc[(winenaradf.price>=70000) & (winenaradf.price<=130000)]
    elif price =='d':
        select_price=winenaradf.loc[(winenaradf.price>=130000) & (winenaradf.price<=200000)]
    elif price =='e':
        select_price=winenaradf.loc[(winenaradf.price>=200000) & (winenaradf.price<=300000)]
    elif price =='f':
        select_price=winenaradf.loc[winenaradf.price>=300000]
          
    y_data=select_price['name']
    x_data=select_price.iloc[:,8:11]
    knn = KNeighborsClassifier(n_neighbors=1).fit(x_data, y_data)
         
    X_new = np.array([[x, y, z]])
    prediction = knn.predict(X_new)
    result=select_price[select_price['name']==prediction[0]]
  
    spsan=int(result.san)
    spdang=int(result.dang)
    spbody=int(result.body)
     
    test_data=select_price.loc[(select_price.san==spsan) & (select_price.dang==spdang) & (select_price.body==spbody)]
    
    dto=createtemp1(test_data)
 
    return render(request, 'list.html', {'dto':dto})


engine = create_engine('mysql://root:12345@localhost/wine1?charset=utf8', encoding = 'utf-8')
conn = engine.connect()
    
wine21df = pd.read_sql_table('wine_wine21', conn)

conn.close()




def createtemp2(df):
    engine = create_engine('mysql://root:12345@localhost/wine1?charset=utf8', encoding = 'utf-8')
    conn = engine.connect()
    df.to_sql(name='wine_wine21_temp', con=engine,if_exists='replace') 
    conn.close()
    dto = Wine21_temp.objects.order_by('idx') 
    return dto





@csrf_exempt
def wine21_search(request): 

    x = int(request.POST['dang'])
    y = int(request.POST['san'])
    z = int(request.POST['body'])
    t = int(request.POST['tannin'])
    price = request.POST['price']
    
    if price =='a':
        select_price=wine21df.loc[wine21df.price<=30000]
    elif price =='b':
        select_price=wine21df.loc[(wine21df.price>=30000) & (wine21df.price<=70000)]
    elif price =='c':
        select_price=wine21df.loc[(wine21df.price>=70000) & (wine21df.price<=130000)]
    elif price =='d':
        select_price=wine21df.loc[(wine21df.price>=130000) & (wine21df.price<=200000)]
    elif price =='e':
        select_price=wine21df.loc[(wine21df.price>=200000) & (wine21df.price<=350000)]
    elif price =='f':
        select_price=wine21df.loc[wine21df.price>=350000]
        
    y_data=select_price['name']
    x_data=select_price.loc[:,['dang','san','body','tannin']]
    
    knn = KNeighborsClassifier(n_neighbors=1).fit(x_data, y_data)
    
    X_new = np.array([[x, y, z,t]])
    prediction = knn.predict(X_new)
    result=select_price[select_price['name']==prediction[0]]
    
    spsan=int(result.san)
    spdang=int(result.dang)
    spbody=int(result.body)
    sptannin=int(result.tannin)
    
    test_data=select_price.loc[(select_price.san==spsan) & (select_price.dang==spdang) & (select_price.body==spbody) & (select_price.tannin==sptannin)]
    
    dto=createtemp2(test_data)
    
    return render(request, 'list2.html', {'dto':dto})

import os
import subprocess;

engine = create_engine('mysql://root:12345@localhost/wine1?charset=utf8', encoding = 'utf-8')
conn = engine.connect()
    
winenaradf = pd.read_sql_table('wine_winenara', conn)

conn.close()


UPLOAD_DIR1 = 'D:/lec502/07.django/app002/wine/static/imageFinder2/image/'

def label_search(request):
    fname = ""
    fsize=0
    if 'file' in request.FILES:
        file=request.FILES['file']
        fname=file._name
        fsize=file.size 
    if fname=="" : 
        return redirect("/")
    fp = open("%s%s" % (UPLOAD_DIR1, fname), "wb")
    for chunk in file.chunks():
        fp.write(chunk)
    fp.close()
   
    subprocess.check_call(['D:/lec502/07.django/app002/wine/static/imageFinder2/MushroomCooker.exe']);

    f=open('D:/lec502/07.django/app002/wine/static/imageFinder2/output.txt','r', encoding='utf-8')
    line1=f.readline()
    line2=f.readline()
    line3=f.readline()
    line4=f.readline()
    f.close()
    numberidx1=int(line1)
    numberidx2=int(line2)
    numberidx3=int(line3)
    numberidx4=int(line4)
    os.unlink("%s%s" % (UPLOAD_DIR1, fname))
    
    return render(request, 'label.html', {'numberidx1':numberidx1, 'numberidx2':numberidx2, 'numberidx3':numberidx3, 'numberidx4':numberidx4})


 
    