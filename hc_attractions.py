from PyQt5 import QtWidgets, QtGui, QtCore, QtWebEngineWidgets
from PyQt5.QtCore import Qt
import sys
import pandas as pd
import folium
from folium import Marker
import matplotlib as mpl
import matplotlib.pyplot as plt

#======================================================================
#按鈕動作
def btn_map():
    # 直條圖
    new_data = data.copy()
    new_data = new_data.drop(columns=['民國年月'])  # 欄位很多可以用drop來刪除欄位比較方便
    new_data = new_data.set_index(["年", "月"])

    mpl.rc('font', family='Microsoft JhengHei')  # 中文字型
    Accent = mpl.colormaps['Accent']
    new_Accent = [Accent(n) for n in range(8)]  # 顏色產生字典檔
    color_dict = dict(zip(new_data.columns, new_Accent))

    fig, ax = plt.subplots(nrows=1, ncols=1, constrained_layout=True, figsize=(12, 6))

    if year_box.currentText() == '全部':
        y_label = new_data.sum().sort_values(ascending=0)
        fig.suptitle('新竹市重要遊憩據點遊客人次統計', fontsize=30, fontweight='bold')
        ax.set_yticks([n for n in range(0,100000001,5000000)],[str(n) for n in range(0,10001,500)], fontsize=15,fontweight='bold') #位置和名稱，對應標籤 rotation=角度

    elif moon_box.currentText() == '全年':
        y_label = new_data.loc[year_box.currentText(), :].sum().sort_values(ascending=0)
        fig.suptitle(f'新竹市重要遊憩據點{year_box.currentText()}年遊客人次統計', fontsize=30, fontweight='bold')
        ax.set_yticks([n for n in range(0,20000001,1000000)],[str(n) for n in range(0,2001,100)], fontsize=15,fontweight='bold') #位置和名稱，對應標籤 rotation=角度
    else:
        y_label = new_data.loc[(year_box.currentText(), moon_box.currentText()), :].sort_values(ascending=0)
        fig.suptitle(f'新竹市重要遊憩據點{year_box.currentText()}年{moon_box.currentText()}月遊客人次統計', fontsize=30,fontweight='bold')
        ax.set_yticks([n for n in range(0,2000001,50000)],[str(n) for n in range(0,201,5)], fontsize=15,fontweight='bold') #位置和名稱，對應標籤 rotation=角度

    value=ax.bar(y_label.index, y_label,color=[color_dict[n] for n in y_label.index]) #color=(r.g.b.透明度) 顏色給不夠會循環
    ax.bar_label(value, fmt='%10d', fontsize=15, fontweight='bold', padding=3)
    ax.set_xlabel('新竹據點', fontsize=25,fontweight='bold')  # x軸說明
    ax.set_ylabel('人數(萬)', fontsize=25,fontweight='bold')  # 益y軸說明
    # ax.bar_label(fmt='%10d', padding=3)
    ax.set_xticks(range(len(y_label.index)), y_label.index, fontsize=15, fontweight='bold')  # 位置，對應標籤 rotation=角度

    plt.savefig("./data/photo.jpg")
    scene.clear()
    img = QtGui.QPixmap('./data/photo.jpg')
    img = img.scaled(600, 300)  # 圖片大小調整
    scene.addPixmap(img)  # 將圖片加入 scene
    grview.setScene(scene)  # 設定 QGraphicsView 的場景為 scene

    #===============================================================================
    #地圖更新
    y_label.name = 'people'
    hc_df = pd.read_csv('./data/地點.csv', encoding="Big5")
    hc_df= hc_df.set_index(["station"])
    hc_df=pd.concat([y_label, hc_df], axis=1)
    hc_df=hc_df.reset_index()
    hc_map = folium.Map(location=[24.807146129155797, 120.96874785749327], tiles='openstreetmap', zoom_start=14)
    for idx, row in hc_df.iterrows():
        station=row['index']
        people=row['people']
        Marker(location=[row['lat'], row['lng']], popup=f'<span style="font-size: 15px;">{station}\n{people}人</span>', icon=folium.Icon(color="green")).add_to(hc_map)
    hc_map.save("./data/map.html")
    widget.load(QtCore.QUrl("file:///./data/map.html"))


def bar_photo():
    if year_box.currentText() == '全部':
        name=f'新竹市重要遊憩據點遊客人次統計'
    elif moon_box.currentText() == '全年':
        name=f'新竹市重要遊憩據點{year_box.currentText()}年遊客人次統計'
    else:
        name=f'新竹市重要遊憩據點{year_box.currentText()}年{moon_box.currentText()}月遊客人次統計'
    plt.savefig(f"{name}.jpg")

def y_box():
    # 下拉選單連動
    if year_box.currentText() == '全部':
        moon_box.clear()
        moon_box.addItem('全年')
    else:
        moon_box.clear()
        list = data.groupby('年').get_group(year_box.currentText())
        moon_box.addItems(list["月"])
        moon_box.addItem('全年')

#======================================================================
#資料載入
data=pd.read_csv('./data/新竹遊客人數.csv')
data=data.drop(columns=['Countycode','YYYMM']) #欄位很多可以用drop來刪除欄位比較方便
data.columns=[data.columns[i].strip('人次') for i in range(len(data.columns))]
data=data.astype('int32') # 將dyype轉成整數 型態轉換
data['民國年月']= data['民國年月'].astype('str') # 將dyype轉成字串
data['年']=data['民國年月'].str[:3] #年分開
data['月']=data['民國年月'].str[3:5] #月分開

year_list=[data["年"].unique()[i] for i in range(data["年"].unique().size)]
year_list.append("全部")

#======================================================================
# 視窗
app = QtWidgets.QApplication(sys.argv) # 視窗程式開始

Form = QtWidgets.QWidget()
Form.setWindowTitle('新竹景點人數')
Form.resize(800, 800)

#標籤
year_label = QtWidgets.QLabel(Form)     # 在 Form 裡加入 label
year_label.move(10,10)                  # 設定位置
year_label.setText('年:')
moon_label = QtWidgets.QLabel(Form)     # 在 Form 裡加入 label
moon_label.move(100,10)                 # 設定位置
moon_label.setText('月:')
#出處
label = QtWidgets.QLabel(Form)     # 在 Form 裡加入 label
label.move(360,10)                  # 設定位置
label.setText('by: <a href="https://github.com/fpdkeoo/hc_attractions">點擊這裡訪問 fpdkeoo github</a>')
label.setOpenExternalLinks(True)

#下拉式選單
year_box = QtWidgets.QComboBox(Form)   # 加入下拉選單
year_box.addItems(year_list)   # 加入四個選項
year_box.setGeometry(27,5,70,20)       # 設定位置與大小

moon_list = data.groupby('年').get_group(year_box.currentText())
moon_box = QtWidgets.QComboBox(Form)  # 加入下拉選單
moon_box.addItems(moon_list["月"])  # 加入四個選項
moon_box.addItem('全年')
moon_box.setGeometry(117, 5, 70, 20)  # 設定位置與大小

#更改年的下拉式選單
year_box.currentIndexChanged.connect(y_box)

#按鈕
btn = QtWidgets.QPushButton(Form)       # 在 Form 中加入一個 QPushButton
btn.setText('確定')                     # 按鈕文字
btn.move(195,5)                         #位置
btn.clicked.connect(btn_map)            # 點擊時執行函式
bar_btn = QtWidgets.QPushButton(Form)   # 在 Form 中加入一個 QPushButton
bar_btn.setText('輸出直條圖')           # 按鈕文字
bar_btn.move(275,5)                     #位置
bar_btn.clicked.connect(bar_photo)            # 點擊時執行函式

#直條圖圖片
grview = QtWidgets.QGraphicsView(Form)  # 加入 QGraphicsView
grview.setGeometry(5, 35, 600, 300)    # 設定 QGraphicsView 位置與大小
scene = QtWidgets.QGraphicsScene()      # 加入 QGraphicsScene
scene.setSceneRect(0, 0, 600, 300)      # 設定 QGraphicsScene 位置與大小
grview.setVerticalScrollBarPolicy(Qt.ScrollBarAlwaysOff)
grview.setHorizontalScrollBarPolicy(Qt.ScrollBarAlwaysOff)
img = QtGui.QPixmap('./data/logo.jpg')         # 加入圖片
img = img.scaled(600,300)               #圖片大小調整
scene.addPixmap(img)                    # 將圖片加入 scene
grview.setScene(scene)                  # 設定 QGraphicsView 的場景為 scene

#地圖
hc_map = folium.Map(location=[24.807146129155797, 120.96874785749327], tiles='openstreetmap', zoom_start=14)
hc_map.save("./data/map.html")
widget = QtWebEngineWidgets.QWebEngineView(Form)  # 建立網頁顯示元件
widget.move(5,340)                                #地圖位置
widget.resize(790, 455)                           #地圖大小
widget.load(QtCore.QUrl("file:///./data/map.html"))    # 載入網頁

Form.show()   # 顯示元件
sys.exit(app.exec_())