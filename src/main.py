from src.algorithm.data_manager import *
from lib.share import *

if __name__ == "__main__":
    directory = share.directory
    flight_manager = FlightManager(directory)

    flight_manager.load_flights()  # 加载航班信息

    # 查找从 "北京" 到 "上海" 费用最少的航班
    cheapest_flight = flight_manager.get_cheapest_flight("北京", "上海")
    if cheapest_flight:
        print("费用最少的航班信息:")
        print(cheapest_flight)
    else:
        print("没有找到从 北京 到 上海 的航班")

    # 查找从 "北京" 到 "上海" 时间最短的航班
    shortest_flight = flight_manager.get_shortest_flight("北京", "上海")
    if shortest_flight:
        print("时间最短的航班信息:")
        print(shortest_flight)
    else:
        print("没有找到从 北京 到 上海 的航班")


