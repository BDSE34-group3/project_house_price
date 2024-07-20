import multiprocessing as mp
from time import time

import lib.corcoordinate_caculate as cc
import pandas as pd


def process_fac_type(fac_type, house_df, near_fac):
    start_time = time()
    near_fac_df = near_fac[near_fac["類型"] == fac_type]
    print(f"{fac_type} started")
    cc.distance_caculate_and_cat_counts(
        house_df, near_fac_df, fac_type, [250, 500, 750]
    )
    # 只是存個檔避免當中有錯誤
    house_df.to_csv(f"./near_facility_combine_{fac_type}.csv")
    print(f"{fac_type} finish")
    print(time() - start_time)


def main():

    near_fac = pd.read_csv("../../all_data/near_fac_corrected.csv")
    # 一定要當場生cor的tuple欄位如果事先把它寫在表格當中他會無法辨認出來....
    cc.convert_lat_lon_to_tuple(near_fac, "Latitude", "Longitude")

    house_df = pd.read_csv(
        "../../all_data/內政部實價登錄_data/台北市_10101_11303_房價data.csv"
    )
    house_df = house_df.head(100)

    cc.convert_lat_lon_to_tuple(house_df, "latitude", "longitude")

    type_list = list(near_fac["類型"].unique())

    processes = []
    for fac_type in type_list:
        p = mp.Process(target=process_fac_type, args=(fac_type, house_df, near_fac))
        processes.append(p)
        p.start()

    for p in processes:
        p.join()


if __name__ == "__main__":
    main()
