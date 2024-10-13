# 新竹景點人數統計

程式介面:

![image.png](image.png)

使用了`PyQt5`，`sys`，`matplotlib`，`pandas` ，`folium`五種函式庫

因為`tkinter`無法顯示google地圖，所以改用`PyQt5`撰寫GUI介面

# 資料來源

**政府資料開放平台 - 新竹市重要遊憩據點遊客人次統計**

[新竹市重要遊憩據點遊客人次統計 ｜ 政府資料開放平臺](https://data.gov.tw/dataset/99374)

# 功能介紹

①資料顯示：依照選擇年份和月份，將資料加總，繪製直條圖

![image.png](18de78af-b228-4222-813c-a97d49d6374f.png)

②地圖標示：將地點標示於地圖上，並顯示地名和加總後的人數

![image.png](image%201.png)

③輸出直條圖：將直條圖存成檔案於資料夾中

![image.png](image%202.png)

# 程式介紹

程式流程圖

![image.png](image%203.png)

年：讀取Excel裡的年份資料並新增加入名為’全部’的選項

![image.png](8f523d3a-b050-468c-9ff7-06a3498a6b8d.png)

月：依照’年’所選擇的結果抓取月份的資料並新增加入名為’全年’的選項

![image.png](image%204.png)

顯示直條圖：直條圖的標題依照所選條件做改變，顏色和地點名稱做綁定

![image.png](image%205.png)

輸出直條圖：將直條圖存入資料夾中，檔名依照所選條件做改變

![image.png](image%206.png)

地圖：將地點加入地圖，並加入名稱和人數

![image.png](defb9a14-5dd0-42f2-a89e-f89909784713.png)

顯示結果

![image.png](image%207.png)