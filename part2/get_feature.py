import pandas as pd
import numpy as np

data_MDA = pd.read_csv('./processed data/association matrix.csv',header = None)
data_M = pd.read_csv('./processed data/miRNA similarity Network.csv',header = None)
data_D = pd.read_csv('./processed data/disease similarity Network.csv',header = None)

Headers_984 = np.arange(984)+1
Headers_1207 = np.arange(1207)+1

data_MDA.columns , data_MDA.index = Headers_1207, Headers_984
data_M.columns, data_M.index = Headers_1207, Headers_1207
data_D.columns, data_D.index = Headers_984, Headers_984

print(data_MDA)
print(data_M)
print(data_D)

# labeled feature
data_label_feature = pd.DataFrame(columns = np.arange(2191)+1, index = np.arange(18733)+1)
# for storing positions of lncRNA and disease in feature set
# [j,i] j for disease , i for lncRNA
data_label_feature_position = pd.DataFrame(columns = np.arange(2)+1, index = np.arange(18733)+1)
count = 1
for i in range(1,1208):
    for j in range(1,985):
        if data_MDA[i][j] != 0:
            data_label_feature.loc[count] = (data_M[i].append(data_D[j])).to_numpy()
            data_label_feature_position.loc[count] = [j,i]
            count += 1

data_label_feature.to_csv('./feature result/data_label_feature.csv',header = None,index = None)
data_label_feature_position.to_csv('./feature result/data_label_feature_position.csv',header = None, index = None)

print(data_label_feature)

# unlabeled fearure
data_unlabel_feature = pd.DataFrame(columns = np.arange(2191)+1, index = np.arange(1168955)+1)
# for storing positions of lncRNA and disease in feature set
# [j,i] j for disease , i for lncRNA
data_unlabel_feature_position = pd.DataFrame(columns = np.arange(2)+1, index = np.arange(1168955)+1)
count = 1
for i in range(1,1208):
    for j in range(1,985):
        if data_MDA[i][j] == 0:
            data_unlabel_feature.loc[count] = (data_M[i].append(data_D[j])).to_numpy()
            data_unlabel_feature_position.loc[count] = [j,i]
            count += 1

data_unlabel_feature.to_csv('./feature result/data_unlabel_feature.csv',header = None,index = None)
data_unlabel_feature_position.to_csv('./feature result/data_unlabel_feature_position.csv',header = None, index= None)
print(data_unlabel_feature)
