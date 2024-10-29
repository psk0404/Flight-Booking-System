import os
import pandas as pd
import re


class FlightManager:
    def __init__(self, directory):
        self.directory = directory
        self.flights = {}

    def load_flights(self):
        """读取指定目录下的所有 Excel 文件并存储航班信息"""
        # 遍历.xlsx
        for filename in os.listdir(self.directory):
            if filename.endswith(".xlsx"):
                # 解析文件名，假设文件名格式为 "城市A-城市B.xlsx"
                cities = filename.replace(".xlsx", "").split("-")
                if len(cities) == 2:
                    city_A, city_B = cities[0], cities[1]

                    # 读取 Excel 文件中的数据
                    file_path = os.path.join(self.directory, filename)

                    df = pd.read_excel(file_path)

                    df.columns = df.columns.str.strip()

                    # 将该航线的信息存储到字典中
                    flights_from_A_to_B = []

                    for _, row in df.iterrows():
                        flight_info = {
                            "出发时间": row["出发时间"],
                            "出发机场": row["出发机场"],
                            "行程时间": row["行程时间"],
                            "抵达时间": row["抵达时间"],
                            "抵达机场": row["抵达机场"],
                            "航空信息": row["航空信息"],
                            "机票价格": row["机票价格"]
                        }
                        flights_from_A_to_B.append(flight_info)

                    # 将航班信息加入到嵌套字典中
                    if city_A not in self.flights:
                        self.flights[city_A] = {}
                    self.flights[city_A][city_B] = flights_from_A_to_B

    def get_flights(self, city_A, city_B):
        """获取从 city_A 到 city_B 的航班信息"""
        if city_A in self.flights and city_B in self.flights[city_A]:
            return self.flights[city_A][city_B]
        else:
            return None

    def get_flight(self, city_A, city_B, i, info):
        if city_A in self.flights and city_B in self.flights[city_A]:
            return self.flights[city_A][city_B][i][info]
        else:
            return None

    def display_flights(self, city_A, city_B, i):
        """显示从 city_A 到 city_B 的航班信息"""
        flights_info = self.get_flights(city_A, city_B)
        if flights_info:
            print(f"从 {city_A} 到 {city_B} 的航班信息:")
            flight = flights_info[i]
            print(f"  出发时间: {flight['出发时间']}")
            print(f"  出发机场: {flight['出发机场']}")
            print(f"  行程时间: {flight['行程时间']}")
            print(f"  抵达时间: {flight['抵达时间']}")
            print(f"  抵达机场: {flight['抵达机场']}")
            print(f"  航空信息: {flight['航空信息']}")
            print(f"  机票价格: {flight['机票价格']}")
            print()
        else:
            print(f"没有从 {city_A} 到 {city_B} 的航班信息。")

    def get_cheapest_flight(self, city_A, city_B):
        """获取从 city_A 到 city_B 费用最少的航班"""
        flights_info = self.get_flights(city_A, city_B)
        if flights_info:
            # 按机票价格排序并返回最便宜的航班
            cheapest_flight = min(flights_info, key=lambda x: x['机票价格'])
            return cheapest_flight
        else:
            return None

    def get_shortest_flight(self, city_A, city_B):
        """获取从 city_A 到 city_B 时间最短的航班"""
        flights_info = self.get_flights(city_A, city_B)
        if flights_info:
            # 按行程时间排序并返回时间最短的航班
            shortest_flight = min(flights_info, key=lambda x: self.extract_duration(x['行程时间']))
            return shortest_flight
        else:
            return None

    def extract_duration(self, duration_string):

        cleaned_duration_string = duration_string.replace('行程时间：', '').strip()
        # 使用正则表达式提取小时和分钟
        match = re.search(r'(\d+)\s*小时\s*(\d+)?\s*分钟', cleaned_duration_string)
        if match:
            hours = int(match.group(1))  # 获取小时
            minutes = int(match.group(2)) if match.group(2) else 0  # 获取分钟，若未提供则为0
            total_minutes = hours * 60 + minutes  # 转换为总分钟数
            return total_minutes
        else:
            raise ValueError("未能解析时间字符串")
