import pandas as pd

# 读取Excel文件
df = pd.read_excel(r'C:\Users\Lenovo\PycharmProjects\BJUT_dsc\data\Web_Scraper\航班信息上海-北京.xlsx')

def split_content(cell_content):
    lines = cell_content.split('\n')

    result = []

    for line in lines:
        result.append(line.strip())

    return result


# 新建DataFrame以存储结果
results = []

for index, row in df.iterrows():
    if index > 0:  # 跳过标题行
        split_data = split_content(row[0])  # 处理第一列
        results.append(split_data)


max_length = max(len(item) for item in results)
new_df = pd.DataFrame(results, columns=[f' ' for i in range(max_length)])

# print(new_df)

# 定义保存路径
output_path = r'/data/air_info/上海-北京.xlsx'
# save
new_df.to_excel(output_path, index=False)
