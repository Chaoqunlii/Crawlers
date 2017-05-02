import pandas as pd
import os
import lianjia
import matplotlib.pyplot as plt
from sklearn.cluster import KMeans

def check_file(filename):
    if os.path.exists(filename):
        print('data file has already existed')
        house_data = pd.read_csv(filename, encoding='gbk', sep=',')
        return house_data
    else:
        print('file does not exist, now run the crawler to get information')
        lianjia.main()
        house_data = pd.read_csv(filename, encoding='gbk', sep=',')

def data_info(data_set):
    print('data primary information')
    data_set.info()
    print('preview data\n', data_set.head())

def data_adj(area_data, str):
    if str in area_data:
        return float(area_data[0: area_data.find(str)])
    else:
        return None

def main():
    filename = 'D:/lianjia_old.csv'
    house_data = check_file(filename)
    data_info(house_data)
    house_data['area_adj'] = house_data['house_area'].apply(data_adj, str='平米')
    house_data['interest_adj'] =  house_data['house_interest'].apply(data_adj,str = '人')  
    #画图时显示中文和负号    
    plt.rcParams['font.sans-serif'] = ['SimHei']    
    plt.rcParams['axes.unicode_minus'] = False

    fig, ax1 = plt.subplots(1,1)
    type_interest_group = house_data['interest_adj'].groupby(house_data['house_type']).agg([('户型', 'count'), ('关注人数', 'sum')])    
    #取户型>50的数据进行可视化
    ti_sort = type_interest_group[type_interest_group['户型'] > 50].sort_values(by='户型')    
    ti_sort.plot(kind='barh', alpha=0.7, grid=True, ax=ax1)    
    plt.title('二手房户型和关注人数分布')    
    plt.ylabel('户型') 
    plt.show()

    '''面积分布'''    
    fig,ax2 = plt.subplots(1,1)    
    area_level = [0, 50, 100, 150, 200, 250, 300, 500]    
    label_level = ['小于50', '50-100', '100-150', '150-200', '200-250', '250-300', '300-350']    
    area_cut = pd.cut(house_data['area_adj'], area_level, labels=label_level)        
    area_cut.value_counts().plot(kind='bar', rot=30, alpha=0.4, grid=True, fontsize='small', ax=ax2)    
    plt.title('二手房面积分布')    
    plt.xlabel('面积')    
    plt.legend(['数量'])    
    plt.show()



    print('-----开始聚类分析-----')    
    # 缺失值处理:直接将缺失值去掉    
    cluster_data = house_data[['interest_adj','area_adj','house_price']].dropna()    
    #将簇数设为3    
    K_model = KMeans(n_clusters=3)    
    alg = K_model.fit(cluster_data)    
    print('------聚类中心------')    
    center = pd.DataFrame(alg.cluster_centers_, columns=['关注人数','面积','房价'])    
    cluster_data['label'] = alg.labels_    
    print(center)



if __name__ == '__main__':
    main()