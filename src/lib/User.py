import atexit
import json

class share:
    loginWin = None
    mainWin = None
    queryWin = None
    directory = 'C:\\Users\\Lenovo\\PycharmProjects\\BJUT_dsc\\data\\air_info'
    win_login_ui = r'C:\Users\Lenovo\PycharmProjects\BJUT_dsc\QT\login.ui'
    querywindow_ui = r'C:\Users\Lenovo\PycharmProjects\BJUT_dsc\QT\QueryWindow.ui'
    MainSyetem_ui = r'C:\Users\Lenovo\PycharmProjects\BJUT_dsc\QT\MainSystem.ui'
    BuyWindow_ui = r'C:\Users\Lenovo\PycharmProjects\BJUT_dsc\QT\buy.ui'
    UserInfo_ui = r'C:\Users\Lenovo\PycharmProjects\BJUT_dsc\QT\info.ui'
    change_ui = r'C:\Users\Lenovo\PycharmProjects\BJUT_dsc\QT\change.ui'
    num = 0
    condition = 0
    num_flights = []
    user_flights = []
    line_flights = []
    slide = []
    service = []
    food_order = []
    value = [1, 1, 1]

    @staticmethod
    def save_slide():
        data = {
            'slide': share.slide,
            'value': share.value
        }
        with open('save.json', 'w') as f:
            json.dump(data, f)

    @staticmethod
    def load_slide():
        try:
            # 尝试加载文件中的数据
            with open('save.json', 'r') as f:
                data = json.load(f)

                share.slide = data.get('slide', share.slide)  # 使用文件中保存的值，若没有则使用当前值
                share.value = data.get('value', share.value)  # 同上
        except FileNotFoundError:
            # 文件不存在时，使用默认值
            share.slide = [50, 50, 50]
            share.value = [1, 1, 1]

# 在程序启动时调用 load_slide()
share.load_slide()

# 注册 save_slide 在程序退出时调用
atexit.register(share.save_slide)