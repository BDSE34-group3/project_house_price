import os

import lib.df_combine_and_re_duplicated as dfc

# 這邊是資料夾下還有資料夾所以要這樣寫
parent_target_dir = "./all_target_dir/"
allFileList = os.listdir(parent_target_dir)
for tmp_dir in allFileList:
    print(tmp_dir)
    dfc.combine_file_under_dir(
        f"{parent_target_dir}{tmp_dir}/", f"./tmp_combine/tmp_{tmp_dir}.csv"
    )

f_target_dir = "./tmp_combine/"
dfc.combine_file_under_dir(f_target_dir, f"./final_loss_little.csv")
