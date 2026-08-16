import hashlib
import os
import random
import socket
import sys
import time
import tkinter.messagebox as box
import tkinter.simpledialog as enter_box
from datetime import datetime
import easygui
import requests
from colorama import Fore, Back, Style
from pythonping import ping

if sys.version_info.major != 3:
    print("Not Support Python 2!")
    sys.exit(1)
morse_codes = {
    "test": ".-",
    "b": "-...",
    "c": "-.-.",
    "d": "-..",
    "e": ".",
    "f": "..-.",
    "g": ".-",
    "h": "....",
    "i": "..",
    "j": ".---",
    "k": "-.-",
    "l": ".-..",
    "m": "--",
    "n": "-.",
    "o": "---",
    "p": ".--.",
    "q": "--.-",
    "r": ".-.",
    "s": "...",
    "t": "-",
    "u": "..-",
    "v": "...-",
    "w": ".--",
    "x": "-..-",
    "y": "-.--",
    "z": "--.."
}
username = "Not Logged in!"
userpath = None
userpath_win = None
logged = False
def Login():
    global logged, username, userpath, userpath_win
    while not logged:
        LoginChoice = easygui.buttonbox( "你是否已经注册过？", "登录选项", ["是", "否，我要注册"])
        if LoginChoice == "是":
            enteredUsername = enter_box.askstring("输入", "输入用户名：")
            enteredPasswd = enter_box.askstring("输入", "输入密码：")
            try:
                PasswdFile=open(f"./UserFiles/{enteredUsername}/password.txt", "r")
                # ---开始计算enteredPwdHash---
                ePwdHashMD5 = hashlib.md5()
                ePwdHashMD5.update(enteredPasswd.encode("utf-8"))
                ePwdHash = ePwdHashMD5.hexdigest()
                # ---结束---
                # ---开始比较ePwdHash和已有的rPasswdHash---
                rPwdHash = PasswdFile.read()
                PasswdFile.close()
                # ---结束---
            except FileNotFoundError:
                if not os.path.isdir(f"./UserFiles/{enteredUsername}/"):
                    box.showerror("Unknown Username", "用户名不存在！")
                else:
                    resetpwd = box.askyesno("PasswdFile 404!", "注意：你的密码文件丢失了，你需要重新设置密码，你的用户数据将会丢失"
                                                    "确定吗？")
                    if resetpwd:
                        os.system(f"md .\\UserFiles\\{enteredUsername}")
                        os.system(f"md .\\UserFiles\\{enteredUsername}\\GuessFist")
                        os.system(f"md .\\UserFiles\\{enteredUsername}\\GuessNumbers")
                        os.system(f"md .\\UserFiles\\{enteredUsername}\\BMI")
                        os.system(f"copy .\\UserFiles\\template\\BMI .\\UserFiles\\{enteredUsername}\\BMI\\")
                        os.system(f"copy .\\UserFiles\\template\\GuessNumbers .\\UserFiles\\{enteredUsername}\\GuessNumbers\\")
                        os.system(f"copy .\\UserFiles\\template\\GuessFist .\\UserFiles\\{enteredUsername}\\GuessFist\\")
                        nPasswd = enter_box.askstring("新密码", "新密码：")
                        nPasswdMD5 = hashlib.md5()
                        nPasswdMD5.update(nPasswd.encode("utf-8"))
                        nPasswdHash = nPasswdMD5.hexdigest()
                        nPasswdFile = open(f"./UserFiles/{enteredUsername}/password.txt", "w")
                        nPasswdFile.write(nPasswdHash)
                        nPasswdFile.close()
                        continue
                    else:
                        continue
            if (ePwdHash == rPwdHash):
                box.showinfo("欢迎", f"欢迎登录:{enteredUsername}")
                logged = True
                username = enteredUsername
                userpath = f"./UserFiles/{enteredUsername}"
                userpath_win = f".\\UserFiles\\{enteredUsername}"
                break
            else:
                box.showerror("密码错误","密码错误，请重试。")
                continue
        elif LoginChoice == "否，我要注册":
            enteredUsername = enter_box.askstring("输入", "输入用户名：")
            enteredPasswd = enter_box.askstring("输入", "输入密码：")
            SignUp(enteredUsername, enteredPasswd)
        elif LoginChoice is None:
            box.showwarning("注意！", "你已以游客身份登录。")
            logged = False
            break


def SignUp(Username, Password):
    global username, userpath, logged
    if not os.path.isdir(f"./UserFiles/{Username}"):
        os.system(f"md .\\UserFiles\\{Username}")
        os.system(f"type nul>./UserFiles/{Username}/Password.txt")
        username = Username
        userpath = f"./UserFiles/{Username}"
        userpath_win = f".\\UserFiles\\{Username}"
        passwdFile = open(f"./UserFiles/{Username}/Password.txt", "w")

        nPwdHashMD5 = hashlib.md5()
        nPwdHashMD5.update(Password.encode("utf-8"))
        nPwdHash = nPwdHashMD5.hexdigest()

        passwdFile.write(nPwdHash)
        passwdFile.close()
        initUserData(Username, Password)
        box.showinfo("通知", "请重新登录！")
    else:
        box.showerror("用户名存在", "用户名已经存在了！")

def initUserData(Username, Password):
    ePasswdMD5 = hashlib.md5()
    ePasswdMD5.update(Password.encode("utf-8"))
    ePasswdHash = ePasswdMD5.hexdigest()
    rPwdHashFile = open(f"./UserFiles/{Username}/password.txt", "r")
    rPwd= rPwdHashFile.read()
    rPwdHashFile.close()
    if ePasswdHash == rPwd:
        try:
            os.system(f"md .\\UserFiles\\{Username}")
            # os.system(f"rd /q /s \\UserFiles\\{Username}\\GuessFist")
            # os.system(f"rd /q /s \\UserFiles\\{Username}\\GuessNumbers")
            # os.system(f"rd /q /s \\UserFiles\\{Username}\\BMI")
            os.system(f"md .\\UserFiles\\{Username}\\GuessFist")
            os.system(f"md .\\UserFiles\\{Username}\\GuessNumbers")
            os.system(f"md .\\UserFiles\\{Username}\\BMI")
            os.system(f"copy .\\UserFiles\\template\\BMI .\\UserFiles\\{Username}\\BMI\\")
            os.system(f"copy .\\UserFiles\\template\\GuessNumbers .\\UserFiles\\{Username}\\GuessNumbers\\")
            os.system(f"copy .\\UserFiles\\template\\GuessFist .\\UserFiles\\{Username}\\GuessFist\\")
            os.system('cls')
        except:
            pass
    else:
        box.showerror("Password Wrong", "错误的密码，操作失败！")

default_message = '欢迎来到App.py，请你选择一个功能'
will_shutdown = False
shutdown_time = None
message = '欢迎来到App.py，请你选择一个功能'
print(Fore.BLUE + '*:这是输出区，在使用Ping等功能时，返回结果将显示在这里。')
print(Style.RESET_ALL)
Login()
while True:
    version = f'NiceProgram App VERSION 2.5.1\n用户名：{username}'
    if will_shutdown:
        message = f"""{default_message}
请注意，在{int(shutdown_time)}秒后，你的电脑将会关机，你可以在>定时关机>取消在当前计算机上的关机计划中取消。如果无法取消请尽快在\
cmd、PowerShell、终端窗口或运行窗口中执行命令：
shutdown -test
如果已经执行shutdown -test，请忽略此消息！"""
    else:
        message = default_message[:]
    if logged:
        HomeChoices = ['猜数字', '中英互译机', 'Ping', '石头剪刀布', '进制转换', '让你的设备蓝屏'
            , '摩斯密码转换器', '计算正确率', '计算平均数', 'Talk out', '恶搞', '读心术',
                       '计算鸡兔同笼问题', 'Collatz数列', '激活Windows(需要管理员权限)', '九九乘法表',
                       'BMI检测', '凑钱数', '按升/降排序数列', '定时关机', '反馈问题', '更新日志',
                       '批量创建文件', '账户相关', '关于']
    else:
        HomeChoices = ['猜数字', '中英互译机', 'Ping', '石头剪刀布', '进制转换', '让你的设备蓝屏'
                                                , '摩斯密码转换器', '计算正确率', '计算平均数', 'Talk out', '恶搞', '读心术',
                                             '计算鸡兔同笼问题', 'Collatz数列', '激活Windows(需要管理员权限)', '九九乘法表',
                                             'BMI检测', '凑钱数', '按升/降排序数列', '定时关机', '反馈问题', '更新日志',
                                             '批量创建文件', '关于']

    Home_Choice = easygui.buttonbox(message, '主页',
                                    HomeChoices)
    if Home_Choice == '猜数字':
        scope = enter_box.askstring('输入范围', '输入范围，中间用“~”分隔')
        find_to = scope.find('~')
        try:
            start = int(scope[:find_to])
            end = int(scope[find_to + 1:])
        except ValueError:
            box.showerror('数值错误', '你输入的不是整数！')
        else:
            right = random.randint(start, end)
            Error_frequency = 0
            while True:
                Guess_numbers_Enter = enter_box.askstring('输入', f"""计算机已经创建了{start}~{end}中的数字，尽你的能力猜到它！
输入exit退出
输入empty清空所有数据""")
                if Guess_numbers_Enter != 'exit' and Guess_numbers_Enter != 'empty':
                    if not Guess_numbers_Enter.isdecimal():
                        box.showerror('数值错误', '你输入的不是数字')
                        continue
                    Guess_numbers_Enter = int(Guess_numbers_Enter)
                    if start <= Guess_numbers_Enter <= end:
                        if Guess_numbers_Enter == right:
                            box.showinfo('猜对了！', f'恭喜你猜对了数字：{right}，你一共用了{Error_frequency}次。')
                            if logged:
                                try:
                                    file_guessNumber = open(f'{userpath}/GuessNumbers/GuessNumbers.txt', 'a')
                                except FileNotFoundError:
                                    box.showerror('找不到文件', 'App找不到指定文件')
                                    break
                                except Exception as error:
                                    box.showerror('错误', f'进行文件写入时发生了未知错误:{error}')
                                    break
                                else:
                                    file_guessNumber.write('\n')
                                    file_guessNumber.write(f"""错误次数：{str(Error_frequency)}
正确数字：{right}
日期：{datetime.today()}
范围：{str(start)}~{str(end)}
---------""")
                                    file_guessNumber.close()
                                    break
                        elif Guess_numbers_Enter > right:
                            Error_frequency += 1
                            box.showinfo('回答错误', '猜大了！')
                            continue
                        elif Guess_numbers_Enter < right:
                            Error_frequency += 1
                            box.showinfo('回答错误', '猜小了！')
                    else:
                        box.showerror('超出范围', '输入的数值超出范围！')
                        continue
                elif Guess_numbers_Enter == 'exit':
                    break
                elif Guess_numbers_Enter == 'empty':
                    if logged:
                        file_guessNumber = open(f'{userpath}/GuessNumbers/GuessNumbers.txt', 'w')
                        file_guessNumber.write('GuessNumber FREQUENCY')
                        file_guessNumber.close()
                        box.showinfo('成功', '清除成功！')
                        break
                    else:
                        box.showerror("失败", "你暂未登录！此操作无效")
    elif Home_Choice == '中英互译机':
        string = enter_box.askstring('翻译', '输入翻译内容')
        data = {
            'doctype': 'json',
            'type': 'AUTO',
            'i': string
        }
        try:
            translate_url = 'https://cn.bing.com/translator/?h_text=msn_ctxt&setlang=zh-cn'
            r = requests.get(translate_url, params=data)
            result = r.json()
            translate_result = result['translateResult'][0][0]["tgt"]
            box.showinfo('翻译结果', translate_result)
        except Exception:
            box.showerror('错误', '爬虫被阻止')
    elif Home_Choice == 'Ping':
        Ping_Choice = easygui.buttonbox('选择方式', 'Ping',
                                        ['使用系统Ping(仅限Windows，其它系统使用会报错)', '使用Python Ping'])
        if Ping_Choice == '使用系统Ping(仅限Windows，其它系统使用会报错)':
            System_url = enter_box.askstring('输入', '请输入网址')
            try:
                System_Ping = os.system(f'Ping {System_url}')
                print(System_Ping)
                print('结束')
            except Exception:
                box.showerror('错误',
                              '调用系统Ping时错误，请检查系统是否是Windows(或者Windows版本低于Windows 98)，或者是Ping时\
发生其他错误')
        elif Ping_Choice == '使用Python Ping':
            Python_ping_url = enter_box.askstring('输入', '请输入网址')
            Python_ping = str(ping(Python_ping_url))
            print(Python_ping)
            print('结束')
    elif Home_Choice == '石头剪刀布':

        def show_state(now_state):
            if now_state == 'win':
                box.showinfo('NICE!', '你赢了！牛逼！')
            elif now_state == 'lose':
                box.showinfo('再接再厉！', '你输了。再接再厉！')
            elif now_state == 'tie':
                box.showinfo('打平了', '打平了，旗鼓相当。')


        win = 0
        lose = 0
        tie = 0
        while True:
            FingerGuessing_list = ['石头', '剪刀', '布']
            if win == 0 and lose == 0 and tie == 0:
                message = f"""选择一个选项
当前状态：
待开始游戏......"""
            else:
                message = f"""选择一个选项
当前状态：
赢:{str(win)} 输:{str(lose)} 平局:{str(tie)}"""
            Your_Choice = easygui.buttonbox(message, '选择', FingerGuessing_list)
            System_Choice = random.choice(FingerGuessing_list)
            if Your_Choice == '石头':
                if System_Choice == '石头':
                    show_state('tie')
                    tie += 1
                    continue
                elif System_Choice == '剪刀':
                    show_state('win')
                    win += 1
                    continue
                elif System_Choice == '布':
                    show_state('lose')
                    lose += 1
                    continue
            elif Your_Choice == '剪刀':
                if System_Choice == '石头':
                    show_state('lose')
                    lose += 1
                    continue
                elif System_Choice == '剪刀':
                    show_state('tie')
                    tie += 1
                    continue
                elif System_Choice == '布':
                    show_state('win')
                    win += 1
                    continue
            elif Your_Choice == '布':
                if System_Choice == '石头':
                    show_state('win')
                    win += 1
                    continue
                elif System_Choice == '剪刀':
                    show_state('lose')
                    lose += 1
                    continue
                elif System_Choice == '布':
                    show_state('tie')
                    tie += 1
                    continue
            elif Your_Choice is None:
                if win == 0 and lose == 0 and tie == 0:
                    break
                else:
                    if win > lose:
                        state = '赢'
                    elif win == lose:
                        state = '平局'
                    elif win < lose:
                        state = '输'
                    if logged:
                        try:
                            GuessFist_file = open(f'{userpath}/GuessFist/GuessFist.txt', 'a')
                        except FileNotFoundError:
                            box.showerror('保存失败', f'没有找到文{userpath}/GuessFist/GuessFist.txt件。')
                        else:
                            GuessFist_file.write('\n')
                            GuessFist_file.write(f"赢:{win}\n输:{lose}\n平局:{tie}\n综合:{state}\n时间：{datetime.today()}")
                            GuessFist_file.write('\n----------------')
                            GuessFist_file.close()
                            break
                    else:
                        print("File Not Saved!")
                        break
    elif Home_Choice == '进制转换':
        JinZhi_Choice = easygui.buttonbox('选择一个选项', '进制转换', ['十进制转二进制', '几进制转十进制'])
        if JinZhi_Choice == '十进制转二进制':
            while True:
                num = enter_box.askstring('输入数字', '请输入一个十进制数字')
                if num.isdecimal():
                    binary = bin(int(num))
                    binary = str(binary)
                    binary = binary.replace('0b', '')
                    box.showinfo('结果', f'此二进制数是：{binary}')
                    break
                else:
                    restart = box.askyesno('重新输入？', '你输入的不是数字，你想要重新输入吗？')
                    if restart:
                        continue
                    else:
                        break
        elif JinZhi_Choice == '几进制转十进制':
            while True:
                num = enter_box.askstring('输入数字', '输入一个任意进制的数字')
                what_JinZhi = enter_box.askstring('输入进制', '请输入你刚刚输入的数字的进制(用阿拉伯数字)')
                try:
                    what_JinZhi = int(what_JinZhi)
                    result = int(num, what_JinZhi)
                    box.showinfo('结果', str(result))
                    break
                except ValueError:
                    restart = box.askyesno('重新输入？', '你输入的不是数字，你想要重新输入吗？')
                    if restart:
                        continue
                    else:
                        break
    elif Home_Choice == '让你的设备蓝屏':
        box.showwarning('警告', """仅限Windows !
这可不是开玩笑，此功能真的会让Windows 蓝屏！！！
Windows 11加了保护措施，不能蓝屏......""")
        continue_choice = box.askyesno('继续？', '真的要继续吗？')
        if continue_choice:
            continue_enter = enter_box.askstring('验证', """如需继续，请输入“yes”
输入yes后如需取消，请按下Ctrl(Command)+C。""")
            if continue_enter == 'yes':
                try:
                    print(Back.RED + Fore.GREEN + '3')
                    time.sleep(1)
                    print(2)
                    time.sleep(1)
                    print(1)
                    print(Style.RESET_ALL)
                    time.sleep(1)
                    os.system('Powershell.exe wininit')
                except KeyboardInterrupt:
                    print('紧急取消完成。' + Style.RESET_ALL)
            else:
                pass
        else:
            pass
    elif Home_Choice == '摩斯密码转换器':
        while True:
            letter_enter = enter_box.askstring('Enter', '''输入要转换成摩斯密码的字母，只能输入小写！否则程序将不返回大写字母、特殊符号
输入“EXIT退出”''')
            if letter_enter != 'EXIT':
                length = len(letter_enter)
                morse_code = ''
                for i in range(length):
                    if letter_enter[i] in morse_codes.keys():
                        morse_code = morse_code + '   ' + morse_codes.get(letter_enter[i])
                box.showinfo('result', f'转换完成！结果：{morse_code}')
            elif letter_enter == 'EXIT':
                break
    elif Home_Choice == '计算正确率':
        all_question = enter_box.askinteger('计算正确率', '输入题目总数', minvalue=1)
        right_questions = enter_box.askinteger('计算正确率', '输入正确题目总数', minvalue=0,
                                               maxvalue=all_question)
        accuracy = right_questions / all_question * 100
        accuracy = str(right_questions / all_question * 100) + '%'
        box.showinfo('正确率', f'正确率：{accuracy}')
    elif Home_Choice == '计算平均数':
        numbers = []
        set_del_max_min = True
        while True:
            if set_del_max_min:
                del_max_min = box.askyesno('去除值', '你想要去除列表中的最大值和最小值吗？')
                set_del_max_min = False
            number = enter_box.askstring('计算平均数', '请输入一个数字，输入"start"开始计算，输入"exit"退出')
            if number == 'exit':
                numbers = []
                break
            elif numbers == [] and number == 'start':
                box.showerror('错误', '请输入数字！')
                set_del_max_min = False
                continue
            elif number != 'exit' and number != 'start':
                if number.isdecimal():
                    number = int(number)
                    numbers.append(number)
                else:
                    box.showwarning('错误', '请输入整数！输入小数将去小数点及小数！')
                    set_del_max_min = False
                    continue
            elif len(numbers) > 0 and number != 'exit' and number == 'start':
                if del_max_min:
                    max_value = max(numbers)
                    frequency = numbers.count(max_value)
                    for cycle in range(frequency):
                        numbers.remove(max_value)
                    min_value = min(numbers)
                    frequency = numbers.count(min_value)
                    for cycle in range(frequency):
                        numbers.remove(min_value)
                    print(f'已经去除最大、小值，去除完的结果为：{numbers}\n')
                number_sum = sum(numbers)
                average = number_sum / len(numbers)
                box.showinfo('平均数', f'它们的平均数为：{average}')
                numbers = []
                set_del_max_min = True
    elif Home_Choice == 'Talk out':
        help_words = """If you are happy,you can enter "EXIT" to exit.
Enter "CLEAN" to clean the enter area.
Enter "HELP" to print the help words."""
        print(f"""Talk out:
{help_words}""")
        while True:
            talk_out = input()
            if talk_out == 'EXIT':
                os.system('cls')
                yes = input('Do you want exit?(Enter "yes" or "no".)')
                if yes == 'yes':
                    os.system('cls')
                    break
                else:
                    os.system('cls')
                    continue
            elif talk_out == 'CLEAN':
                os.system('cls')
            elif talk_out == 'HELP':
                print(help_words)
    elif Home_Choice == '恶搞':
        os.system('taskkill -im explorer.exe -f')
        os.system('Shutdown -s -t 60 -c 你的电脑将会在60秒后关机，哈哈哈！想恢复就点击确定，在弹出的窗口中输入密码！！！')
        while True:
            password = enter_box.askstring('Password', '快输密码！')
            if password == 'Twb20131023':
                os.system('Shutdown -a')
                os.system('Explorer.exe')
                break
            else:
                box.showerror('错误', '密码错误！')
    elif Home_Choice == '读心术':
        box.showinfo('欢迎', '请你想一个1~31的数字，开始吧！！！')
        right = []
        _pow_ = 1
        result = 0
        for i in range(1, 33):
            temp = i
            a = ['0' for _ in range(6)]
            j = 0
            while temp >= 1:
                a[j] = str(temp % 2)
                j = j + 1
                temp = temp // 2
            right.append(a)
        for j in range(0, 5):
            res = []
            for i in range(0, 32):
                if int(right[i][j]) == 1:
                    res.append(i + 1)
            tmp = []
            for ite in res:
                tmp.append(ite)
            tmp_str = str(tmp) + "\n\n如果你想的数字在上面出现了，请输入 1，如果没有出现，请输入 0。\n\n请输入数字 0 或 1:  "
            a = enter_box.askinteger('info', tmp_str, minvalue=0, maxvalue=1)
            result = _pow_ * int(a) + result
            _pow_ *= 2
        tmp_result = "你想的数是:" + str(result)
        box.showinfo('结果', tmp_result)
    elif Home_Choice == '计算鸡兔同笼问题':
        NORMAL, CUSTOMIZE = '普通(鸡2条腿、兔4条腿)', '自定义，如自行车与三轮车'
        mode = easygui.buttonbox('请选择模式', '鸡兔同笼', [NORMAL, CUSTOMIZE])
        THINGS = {}


        def main(head, feet):
            if mode == NORMAL:
                try:
                    chickens = ((head * 4) - feet) / (4 - 2)
                    rabbits = head - chickens
                    if (chickens < 0 or chickens > feet) or (rabbits < 0 or rabbits > feet):
                        box.showerror('错误！', '该问题无解。')
                        return None
                    box.showinfo('计算结果', f'鸡有{int(chickens)}只，兔有{int(rabbits)}只')
                except ZeroDivisionError:
                    box.showerror('错误！', '该问题无解。')
                    return None
                except Exception:
                    box.showerror('错误！', '程序发生未知错误！你可以联系atwbspare@163.com或github.com\
                        /TanWeibo/Projects 反馈问题。')
                    return None
            elif mode == CUSTOMIZE:
                bugwarning = box.askyesno('BUG!!!!', '请注意！当前自定义功能有严重bug。继续运行吗？')
                if bugwarning:
                    a_name = enter_box.askstring('鸡兔同笼', '请输入a物品的名字')
                    a_feet = enter_box.askinteger('鸡兔同笼', '请输入a物品的脚数')
                    b_name = enter_box.askstring('鸡兔同笼', '请输入b物品的名字')
                    b_feet = enter_box.askinteger('鸡兔同笼', '请输入b物品的脚数')
                    feet_sum = a_feet + b_feet
                    head_sum = enter_box.askinteger('鸡兔同笼', '请输入头数总和')

                    try:
                        a_heads = ((b_feet * head_sum) - feet_sum) / (b_feet - a_feet)
                        b_heads = head_sum - a_heads
                        if ((a_heads < 0) or (a_heads > feet_sum)) or ((b_heads < 0) or (b_heads > 0)):
                            box.showerror('错误！', '该问题无解。')
                            return None
                        box.showinfo('鸡兔同笼-结果', f'{a_name}有{a_heads}个(只)、{b_name}有{b_heads}个(只)')
                    except ZeroDivisionError:
                        box.showerror('错误！', '该问题无解。')
                        return None
                    except Exception:
                        box.showerror('错误！', '程序发生未知错误！\
                            /TanWeibo/Projects 反馈问题。')
                        return None
                else:
                    return None


        if mode == NORMAL:
            enter_head = enter_box.askinteger('鸡兔同笼', '请输入头的数量')
            enter_feet = enter_box.askinteger('鸡兔同笼', '请输入脚的数量', minvalue=enter_head)
            main(enter_head, enter_feet)
        elif mode == CUSTOMIZE:
            main(None, None)
    elif Home_Choice == 'Collatz数列':
        def collatz(num):
            print('-----计a算开始-----')
            print(f'初始值：{num}')
            while True:
                if num != 1:
                    if num % 2 == 0:
                        if num == 1:
                            sys.exit(7)
                        else:
                            num = num // 2
                            print(num)
                    elif num % 2 == 1:
                        if num == 1:
                            sys.exit(9)
                        else:
                            num = 3 * num + 1
                            print(num)
                else:
                    print('-----计算结束-----')
                    break


        enter_num = enter_box.askinteger('输入', """输入一个数字。程序将会以Collatz数列计算的方式计算该数字。""",
                                         minvalue=1)
        collatz(enter_num)
    elif Home_Choice == '激活Windows(需要管理员权限)':
        box.showwarning('注意事项', """按下确定后几秒钟会弹出一个窗口。
在那个窗口中：
按下1:永久激活当前版本Windows
按下2:把Windows激活到2038年
按下3:把Windows和Office激活到180天后""")
        os.system('start ActiveScript.bat')
    elif Home_Choice == '九九乘法表':
        box.showinfo('info', '乘法表将会在输出区内输出')
        print('九九乘法表：')
        for i in range(1, 10):
            for j in range(1, i + 1):
                print(f'{j}x{i}={i * j}', end='\t')
            print()
    elif Home_Choice == 'BMI检测':
        if logged:
            bmiFile = open(f'{userpath}/BMI/BMI Log.log', 'a')
            high = enter_box.askfloat('输入', '输入身高(m)', minvalue=0.1, maxvalue=2.0)
            weight = enter_box.askfloat('输入', '输入体重(kg)', minvalue=2.5, maxvalue=640.0)
            bmi = weight / (high ** 2)
            bmiFile.write(f"""\n时间:{datetime.today()}
你的身高：{high}m
你的体重：{weight}kg
BMI:{str(int(bmi))}""")
        if bmi <= 18.4:
            box.showinfo('BMI', f'你的BMI值：{bmi} 温馨提示：你的体型偏瘦，要注意营养哦~')
            bmiFile.write('\n温馨提示：你的体型偏瘦，要注意营养哦~')
        elif 18.4 < bmi <= 23.9:
            box.showinfo('BMI', f'你的BMI值：{bmi} 温馨提示：标准体型，继续保持哦~')
            bmiFile.write('\n温馨提示：标准体型，继续保持哦~')
        elif 24 <= bmi <= 27.9:
            box.showinfo('BMI', f'你的BMI值：{bmi} 温馨提示：你的体型过胖，要注意身体哦~')
            bmiFile.write('\n温馨提示：你的体型过胖，要注意身体哦~')
        elif bmi >= 28:
            box.showinfo('BMI', f'你的BMI值：{bmi} 温馨提示：你的体型肥胖，要注意饮食哦~')
            bmiFile.write('\n温馨提示：你的体型肥胖，要注意饮食哦~')
        bmiFile.write('\n---------')
        bmiFile.close()
    elif Home_Choice == '凑钱数':
        all_manner = 0


        def compute_money(all_money):
            global all_manner
            print('计算中...')
            one = all_money // 1
            two = all_money // 2
            five = all_money // 5
            for compute_one in range(0, one + 1):
                for compute_two in range(0, two + 1):
                    for compute_five in range(0, five + 1):
                        if compute_one + compute_two * 2 + compute_five * 5 == all_money:
                            all_manner += 1
            print('计算成功')
            return all_manner


        box.showinfo('info', '该功能可以算出1、2、5元凑成指定钱数有几种可能。')
        compute_money(enter_box.askinteger('money', '输入钱数', minvalue=1))
        box.showinfo('result', f'结果：{all_manner}')
    elif Home_Choice == '按升/降排序数列':
        while True:
            sort_by = easygui.buttonbox('选择排序方式', '排序', ['升序', '降序'])
            if sort_by is None:
                break
            nums = enter_box.askstring('排序', '请输入序列，确保用空格分开，否则可能无法排序或报错！')
            try:
                nums = nums.split(' ')
                for i in range(0, len(nums)):
                    nums[i] = int(nums[i])
            except ValueError:
                box.showerror('错误', '你输入的数列有些不是数字！')
                break
            for i in range(len(nums) - 1):
                for j in range(len(nums) - 1 - i):
                    if sort_by == '升序':
                        if nums[j] > nums[j + 1]:
                            nums[j], nums[j + 1] = nums[j + 1], nums[j]
                    elif sort_by == '降序':
                        if nums[j] < nums[j + 1]:
                            nums[j], nums[j + 1] = nums[j + 1], nums[j]
            print(f'转换成功！结果：{nums}')
            box.showinfo('RESULT', f'转换成功，结果：{nums}，如需复制，请到输出区。')
    elif Home_Choice == '定时关机':
        shutdown_choice = easygui.buttonbox('请选择类型：', '定时关机',
                                            ['在当前计算机上设置定时关机', '远程关机在当前局域网下的计算机',
                                             '取消在当前计算机上的关机计划',
                                             '关闭在主页中的提醒'], default_choice='在当前计算机上设置定时关机')
        if shutdown_choice == '在当前计算机上设置定时关机':
            shutdown_time = enter_box.askinteger('关机时间', '请输入几秒后关机', minvalue=5)
            yn_continue = box.askyesno('确认', f'请确认关机等待时间：{str(shutdown_time)}秒，在当前计算机上。')
            if yn_continue:
                will_shutdown = True
                os.system(f'shutdown -s -t {str(shutdown_time)} -c 已经在App.py中设置好关机计划：{str(shutdown_time)}秒后关机。\
你可以在App.py中取消计划。')
        elif shutdown_choice == '远程关机在当前局域网下的计算机':
            box.showwarning('warning', """请确保目标计算机已经在组策略中设置好了，并且你知道对方ip地址。才能使用此功能。
否则你将会看到输出区提示：”拒绝访问“字样
具体设置方法自行Baidu""")
            shutdown_time = enter_box.askinteger('关机时间', '请输入几秒后关机', minvalue=20)
            ip = enter_box.askstring('ip', '请输入你要控制的计算机的ip地址')
            yn_continue = box.askyesno('确认', f'请确认关机等待时间：{str(shutdown_time)}秒，在当前{ip}上。')
            if yn_continue:
                this_pc_name = socket.gethostname()
                os.system(f'shutdown -s -t {str(shutdown_time)} -m \\\\{ip}')
                box.showinfo('成功', '执行成功')
        elif shutdown_choice == '取消在当前计算机上的关机计划':
            os.system('shutdown -test')
            will_shutdown = False
            box.showinfo('成功', '取消成功')
        elif shutdown_choice == '关闭在主页中的提醒':
            will_shutdown = False
            box.showinfo('ok', '取消成功！')
    elif Home_Choice == '反馈问题':
        box.showinfo('Have any questions?', '如果您有建议或者问题，请发送邮件到：543622842@qq.com 或者 yelij\
ing830@foxmail.com\n十分感谢您的支持！\nTanWeibo\n2023/8/18')
    elif Home_Choice == '更新日志':
        try:
            update_log_file = open('H:/Projects/App/Update_Log.log', 'r', encoding='utf-8')
        except FileNotFoundError:
            box.showwarning('不能找到文件', '无法找到文件，你可以访问我的Github(Github.co\
m/TanWeibo/Projects/blob/main/App/Update_Log.log)下载Update_Log.log并放在App.py的目录下')
        else:
            log = update_log_file.read()
            update_log_file.close()
            box.showinfo('log', f"""log:
{log}""")
    elif Home_Choice == '批量创建文件':
        file_type = enter_box.askstring('输入类型', '请输入你要批量创建文件的类型(txt文件直接输入txt)')
        file_quantity = enter_box.askinteger('输入数量', '请输入你要创建文件的数量')
        file_path = enter_box.askstring('输入路径', """请输入你要创建文件的位置(绝对路径)
Windows中，所有"\\"都替换为"/"。""")
        file_name = enter_box.askstring('输入文件名', '请输入你要创建文件的名字\n你的文件名+序列+后缀名')
        ok = easygui.buttonbox(f"""这样对吗？
文件类型：{file_type}
创建文件数量：{file_quantity}
创建文件路径：{file_path}
创建文件名：{file_name}""", '确认', ['是的', '不是，我要重新输入'])
        if ok == '是的':
            os.chdir(file_path)
            for num in range(1, file_quantity + 1):
                filename = f'{file_name}{num}.{file_type}'
                os.system(f'type nul>{filename}')
    elif Home_Choice == '账户相关':
        verified = False
        accounts_msg = f"欢迎:{username}!\n选择选项"
        while True:
            if verified:
                choices = ["注销账户","更改用户名", "修改密码", "初始化账户", "上锁"]
            else:
                choices = ["注销账户--该按钮已锁定", "更改用户名--该按钮已锁定", "修改密码--该按钮已锁定", "初始化账户--该按钮已锁定", "解锁"]
            ac_choice = easygui.buttonbox(accounts_msg, "Account Settings", choices)
            if verified:
                if ac_choice == "注销账户":
                    really_da = box.askyesno("真的吗？", "你确定注销账户？提交注销操作后将立刻注销！！！")
                    if not really_da:
                        pass
                    os.system(f'rd /s /q {userpath_win}')
                    box.showwarning("", "账户已经注销，请重新登录！")
                    userpath = None
                    username = "Guest"
                    logged = False
                    Login()
                    break
                elif ac_choice == "修改密码":
                    enPwd = enter_box.askstring("新密码", "输入新密码")
                    enPwdHash = hashlib.md5(enPwd.encode("utf-8")).hexdigest()
                    oPwdHashFile = open(f'{userpath_win}\\password.txt', 'w', encoding='utf-8')
                    oPwdHashFile.write(enPwdHash)
                    oPwdHashFile.close()
                    box.showwarning("", "账户密码已更改，请重新登录！")
                    userpath = None
                    userpath_win = None
                    username = "Guest"
                    logged = False
                    os.system("cls")
                    Login()
                    break
                elif ac_choice == "更改用户名":
                    newUsername = enter_box.askstring("Change Username", "输入你的新用户名")
                    os.system(f'move {userpath_win} .\\UserFiles\\{newUsername}')
                    userpath = f"./UserFiles/{newUsername}"
                    userpath_win = f".\\UserFiles\\{newUsername}"
                    username = newUsername
                    logged = True
                elif ac_choice == "初始化账户":
                    yes = box.askyesno()
                    initUserData(username, ePasswd)
                    box.showinfo("账户初始化成功", "你的用户数据已被重置。")
                elif ac_choice == "上锁":
                    verified = False
                    continue
                elif ac_choice is None:
                    break
            elif not verified:
                if ac_choice == "解锁":
                    ePasswd = enter_box.askstring("输入当前密码", "输入当前登录账户的密码，若要对其他账户操作请切换账户。")
                    ePasswdMD5 = hashlib.md5()
                    ePasswdMD5.update(ePasswd.encode('utf-8'))
                    ePasswdHash = ePasswdMD5.hexdigest()

                    rPasswdFileR = open(f"{userpath}/password.txt", 'r')
                    rPasswdHash = rPasswdFileR.read()
                    rPasswdFileR.close()
                    if(rPasswdHash == ePasswdHash):
                        verified = True
                        continue
                    else:
                        box.showerror("密码错误！", "密码错误，请重试！")
                        verified = False
                        continue
                elif ac_choice is None:
                    break
    elif Home_Choice == '关于':
        box.showinfo('关于', version)
    elif Home_Choice is None:
        break
    else:
        print("Bad Request")
        raise "Bad Request"
