def find_valid_routes(segments, path=[], index=0):
    if index == len(segments):  # 如果到达最后一段，返回当前路径
        return [path]

    valid_routes = []
    for flight in segments[index]:
        if not path or (path[-1][-1] == flight[-2]):  # 检查匹配条件
            valid_routes += find_valid_routes(segments, path + [flight], index + 1)  # 递归调用

    return valid_routes


if __name__ == "__main__":
    segments = [

        [[0, 1, 0, 2], [0, 1, 0, 3], [0, 1, 0, 4], [0, 1, 0, 5], [0, 1, 1, 5], [0, 1, 2, 5], [0, 1, 3, 5]],
        [[1, 2, 0, 2], [1, 2, 0, 3], [1, 2, 0, 4], [1, 2, 0, 5], [1, 2, 1, 3], [1, 2, 1, 4], [1, 2, 1, 5], [1, 2, 2, 5],
         [1, 2, 3, 5], [1, 2, 4, 5]]
    ]

    # 调用函数并打印结果
    result = find_valid_routes(segments)
    for route in result:
        print(route)