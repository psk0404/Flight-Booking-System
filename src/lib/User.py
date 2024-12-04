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

    @staticmethod
    def save_slide():
        with open('slide_values.json', 'w') as f:
            json.dump(share.slide, f)

    # 从文件加载 slide
    @staticmethod
    def load_slide():
        try:
            with open('slide_values.json', 'r') as f:
                share.slide = json.load(f)
        except FileNotFoundError:
            share.slide = [0, 0, 0]  # 如果文件不存在，使用默认值

# 在程序启动时调用 load_slide()
share.load_slide()
# 在程序退出时调用 save_slide()
share.save_slide()
