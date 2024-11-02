import os
import pandas as pd

from src.lib.share import *


class data_loader:
    def __init__(self, directory):
        self.directory = directory
        self.flights = {}
        self.city_mapping = {
            1: "巴黎",
            2: "柏林",
            3: "北京",
            4: "成都",
            5: "长春",
            6: "东京",
            7: "洛杉矶",
            8: "曼谷",
            9: "南京",
            10: "厦门",
            11: "上海",
            12: "深圳",
            13: "首尔",
            14: "乌鲁木齐",
            15: "武汉",
            16: "西安"
        }


    def get_city_number(self, city_name):
        """根据城市名称获取对应的城市编号"""
        for number, name in self.city_mapping.items():
            if name == city_name:
                return number

        raise ValueError(f"未找到城市 {city_name}")

    def load_flights_info(self):
        # 遍历目录中的 .xlsx 文件
        for filename in os.listdir(self.directory):
            if filename.endswith(".xlsx"):
                # 文件名格式为 "城市A-城市B.xlsx"
                cities = filename.replace(".xlsx", "").split("-")
                if len(cities) == 2:
                    city_A, city_B = cities[0], cities[1]

                    # 获取城市的编号
                    city_A_num = self.get_city_number(city_A)
                    city_B_num = self.get_city_number(city_B)

                    # 读取 Excel 文件中的数据
                    file_path = os.path.join(self.directory, filename)
                    df = pd.read_excel(file_path)

                    # 去除列名的空格
                    df.columns = df.columns.str.strip()

                    # 将该航线的信息存储到字典中
                    if city_A_num not in self.flights:
                        self.flights[city_A_num] = {}

                    # 初始化从城市A到城市B的航班信息列表
                    if city_B_num not in self.flights[city_A_num]:
                        self.flights[city_A_num][city_B_num] = []  # 初始化为一个包含空列表的列表

                    for _, row in df.iterrows():
                        # 创建航班信息列表
                        flights_info = [

                            row["出发时间"],
                            row["出发机场"],
                            row["行程时间"],
                            row["抵达时间"],
                            row["抵达机场"],
                            row["航空信息"],
                            row["机票价格"]
                        ]
                        # 将航班信息添加到列表中，索引从 1 开始
                        self.flights[city_A_num][city_B_num].append(flights_info)

    def get_flight_info_all(self, numA, numB, index):
        """获取从城市A到城市B的第index个航班信息"""
        try:
            flight_info = self.flights[numA][numB][index]
            return flight_info

        except KeyError:
            return f"没有找到从 {numA} 到 {numB} 的航班信息。"
        except IndexError:
            return f"从 {numA} 到 {numB} 的航班列表中没有第 {index} 个航班。"
        except Exception as e:
            return str(e)

    def get_flight_info_single(self, numA, numB, index, column_index):
        """获取从城市A到城市B的第index个航班的指定列信息"""
        try:
            flight_info = self.flights[numA][numB][index]
            # 返回指定列的信息
            return flight_info[column_index]

        except KeyError:
            return f"没有找到从 {numA} 到 {numB} 的航班信息。"
        except IndexError:
            return f"从 {numA} 到 {numB} 的航班列表中没有第 {index} 个航班。"
        except Exception as e:
            return str(e)


if __name__ == "__main__":
    loader = data_loader(share.directory)  # 替换为你的目录
    loader.load_flights_info()  # 加载航班信息

    # 输出第一个航班信息
    flight_info = loader.get_flight_info_single(3, 11, 1, 0)
    print(flight_info)



