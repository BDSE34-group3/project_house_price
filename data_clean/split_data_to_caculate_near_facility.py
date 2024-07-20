# 執行 command 的時候用的
import os
from time import sleep, time

import lib.corcoordinate_caculate as cc
import pandas as pd

# 創建檔案放置的資料夾(預設就是創建在主程式的跟目錄底下)
folderPath = "./csv_near_fac_data/"
if not os.path.exists(folderPath):
    os.makedirs(folderPath)

# 暫存有問題的檔案，但應該還是要重跑(可以看一下哪邊出錯)
folderPath2 = "./Error_stash/"
if not os.path.exists(folderPath2):
    os.makedirs(folderPath2)

# 讀取資料夾下的所有檔案
dirPath = r"D:\WORKING_DIR\BDSE34期末專題_房價\project_house_price\data_clean\main_data_piece_1000"
file_list = os.listdir(dirPath)

# 使用字典製造dataframe對應的變數(以key, value: pd.DataFrame)的形式
test_dict = {}
for index, i in enumerate(file_list):
    key = i.split(".")[0]

    test_dict[key] = pd.read_csv(
        f"{dirPath}/{i}"
    )  # 注意一個值若要多個地方要更改，盡量寫成變數、甚至是function

# 比鄰資料表
near_fac = pd.read_csv("../../all_data/near_fac_corrected.csv")
cc.convert_lat_lon_to_tuple(near_fac, "Latitude", "Longitude")
type_list = list(near_fac["類型"].unique())

try:
    # 每個dataframe(1000筆資料一個)與比鄰資料表計算distance並將計算完的欄位合併到df上
    for key in test_dict:
        try:
            house_df = test_dict[key]
            cc.convert_lat_lon_to_tuple(house_df, "latitude", "longitude")
            for fac_type in type_list:
                start_time = time()
                near_fac_df = near_fac[near_fac["類型"] == fac_type]
                print(f"{fac_type} started")
                cc.distance_caculate_and_cat_counts(
                    house_df, near_fac_df, fac_type, [250, 500, 750]
                )
                # 只是存個檔避免當中有錯誤
                # house_df.to_csv(f"./csv_near_fac_data/near_facility_combine_{fac_type}.csv")
                print(f"{fac_type} finish")
                print(f"{fac_type}:{time() - start_time}")
            house_df.to_csv(f"./csv_near_fac_data/near_facility_combine_{key}.csv")
        except Exception as e:
            print(f"{key} have something to do with")
except Exception as e:
    print(f"something wrong or {e}")
finally:
    # 只是確保一下? 這邊除了自己中斷以外應該是不太可能會發生
    house_df.to_csv(f"./Error_stash/stach_{key}_but_have_some_problem.csv")
