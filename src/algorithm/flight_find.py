from path_find import *
from src.algorithm.data_manager import data_loader
from src.lib.share import *
from ceshi import *


class Flight_Info:
    def __init__(self, loader):
        self.loader = loader  # 存储数据加载器的实例

    def get_flights_for_paths(self, paths):
        all_flight_info = []
        for path in paths:
            flight_info = self.get_flights_between_cities(path)  # 获取航班信息
            all_flight_info.append(flight_info)  # 添加每条路径的航班信息

        return all_flight_info

    def get_flights_between_cities(self, path):
        all_flights = []  # 用于存储该路径下的所有航班信息
        # all_flights.extend([1])
        for i in range(len(path) - 1):
            city_A = path[i]
            city_B = path[i + 1]

            # 获取所有航班信息
            if city_A in self.loader.flights and city_B in self.loader.flights[city_A]:
                flights = self.loader.flights[city_A][city_B]
                all_flights.extend(flights)  # 添加航班信息
                all_flights.extend([1])

        return all_flights  # 返回所有航班信息


class Info:
    def __init__(self, loader, a, b):
        self.graph = None
        self.loader = loader  # 存储数据加载器的实例
        self.flight_info = Flight_Info(loader)  # 实例化航班信息类
        self.total = []
        self.a = a
        self.b = b
        self.compute(a, b)  # 在初始化时计算路径
        self.sort()  # 在初始化时排序路径
        self.find()  # 在初始化时输出路径及其航班信息

    def compute(self, a, b):
        self.graph = Graph(a, b)

    def sort(self):
        self.graph.backup.sort(key=lambda path: (len(path), path))

    def find(self):
        for res in self.graph.backup:
            flight_info_for_path = self.flight_info.get_flights_for_paths([res])

            # 存储当前部分的航班信息
            total_flights = []
            single_flights = []
            current_flights = []

            if flight_info_for_path:
                for flights in flight_info_for_path:
                    for flight in flights:
                        if flight == 1:  # 遇到1，输出并清空当前部分
                            for f in current_flights:
                                dep_time = f[0]
                                arr_time = f[3]
                                a1, a2 = dep_time.hour, dep_time.minute
                                b1, b2 = arr_time.hour, arr_time.minute
                                example = [60 * a1 + a2, 60 * b1 + b2]
                                single_flights.append(example)

                            total_flights.append(single_flights.copy())
                            single_flights.clear()  # 清空 single_flights
                            current_flights.clear()  # 清空当前部分
                        else:
                            # 存储航班信息
                            current_flights.append(flight)

                if len(res) == 2:
                    self.findelse2(total_flights, res)
                else:
                    self.findelse(total_flights, res)

    def findelse(self, total_flight, res):
        cunchures2 = []
        for i in range(len(total_flight) - 1):
            cunchures1 = []  # 在每次外层循环开始时初始化
            for j in range(len(total_flight[i])):
                for k in range(len(total_flight[i + 1])):
                    if total_flight[i + 1][k][0] - total_flight[i][j][1] >= 60:
                        cunchures1.append([i, i + 1, j, k])
            cunchures2.append(cunchures1)  # 将当前的 cunchures1 添加到 cunchures2

        has_empty_list = any(len(sublist) == 0 for sublist in cunchures2)
        if not has_empty_list:
            result = find_valid_routes(cunchures2)
            # if result:
            #     print(res)
            thisinfo = []
            for route in result:
                for i in range(len(route)):
                    a, b = route[i][0], route[i][2]
                    c, d = route[i][1], route[i][3]
                    f1, f2 = res[a], res[a + 1]
                    f3, f4 = res[c], res[c + 1]
                    if [f1, f2, b] not in thisinfo:
                        thisinfo.append([f1, f2, b])
                    if [f3, f4, d] not in thisinfo:
                        thisinfo.append([f3, f4, d])
                self.total.append(thisinfo.copy())
                thisinfo.clear()

    def findelse2(self, total_flight, res):
        # print(res)
        thisinfo2 = []
        for i in range(len(total_flight[0])):
            a, b = res[0], res[1]
            thisinfo2.append([a, b, i])
            self.total.append(thisinfo2.copy())
            thisinfo2.clear()

    def outputs(self):
        print(self.total)


if __name__ == "__main__":
    directory = share.directory  # 替换为你的目录
    loader = data_loader(directory)  # 创建数据加载器实例
    loader.load_flights_info()  # 加载航班信息

    info = Info(loader, 11, 3)  # 创建 Info 实例，并传入数据加载器和路径参数
    info.outputs()  # 输出存储的航班信息
