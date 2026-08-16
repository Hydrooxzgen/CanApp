import tkinter.messagebox as box
import tkinter.simpledialog as enter_box
import easygui
import random
import os
from pythonping import ping
import time
import sys
from colorama import Fore, Back, Style
import socket

if sys.version_info.major != 3:
    print('You only use Python3 to run this program!')
    sys.exit(1)
print('Loading.... It\'ll take some time......')
normalRun = False

start_time = time.perf_counter()
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
version = 'NiceProgram App VERSION 2.4'
will_shutdown = False
message = '欢迎来到App.py，请你选择一个功能'
shutdown_time = None
print('Done')
print(Fore.BLUE + '*:这是输出区，在使用Ping等功能时，返回结果将显示在这里。')
print(Style.RESET_ALL)
while True:
    if will_shutdown:
        message = f"""欢迎来到App.py，请你选择一个功能
请注意，在{int(shutdown_time)}秒后，你的电脑将会关机，你可以在App.py>定时关机>取消在当前计算机上的关机计划中取消。如果无法取消请赶紧在\
cmd、PowerShell、终端窗口或运行窗口中执行命令：
shutdown -test
如果已经执行shutdown -test，请忽略此消息！"""
    else:
        message = '欢迎来到App.py，请你选择一个功能'
    Home_Choice = easygui.buttonbox(message, '主页',
                                    ['计算鸡兔同笼问题', '九九乘法表', '按升/降排序数列'
                                    , '进制转换', '计算正确率', '计算平均数',  '凑钱数', '摩斯密码转换器', '读心术', '猜数字'
                                    , '石头剪刀布', 'BMI检测', '批量创建文件', 'Ping', '激活Windows(需要管理员权限)', '定时关机', '关于'])
    if Home_Choice == '猜数字':
        scope = enter_box.askstring('输入范围', '输入范围，中间用“~”分隔')
        find_to = scope.find('~')
        try:
            start = int(scope[:find_to])
            end = int(scope[find_to + 1:])
        except ValueError:
            box.showerror('数值错误', '你输入的不是数/整数！')
        else:
            right = random.randint(start, end)
            Error_frequency = 0
            while True:
                Guess_numbers_Enter = enter_box.askstring('输入', f"""计算机已经创建了{start}~{end}中的数字，尽你的能力猜到它！
输入exit退出""")
                if Guess_numbers_Enter != 'exit':
                    if not Guess_numbers_Enter.isdecimal():
                        box.showerror('数值错误', '你输入的不是数字')
                        continue
                    Guess_numbers_Enter = int(Guess_numbers_Enter)
                    if start <= Guess_numbers_Enter <= end:
                        if Guess_numbers_Enter == right:
                            box.showinfo('猜对了！', f'恭喜你猜对了数字：{right}，你一共用了{Error_frequency}次。')
                            break
                        elif Guess_numbers_Enter > right:
                            Error_frequency += 1
                            box.showinfo('回答错误', '太大啦！')
                            continue
                        elif Guess_numbers_Enter < right:
                            Error_frequency += 1
                            box.showinfo('回答错误', '太小啦！')
                    else:
                        box.showerror('超出范围', '输入的数值超出范围！')
                        continue
                elif Guess_numbers_Enter == 'exit':
                    break
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
        def main(head, feet):
            chickens = int((4 * head - feet) / 2)
            try:
                if head != 0 and (4 * head - feet) % (chickens * 2) == 0:
                    rabbits = int(head - chickens)
                    if chickens < 0 or rabbits < 0:
                        box.showerror('无解', f'{head}个头，{feet}只脚的题目无解')
                    else:
                        box.showinfo('结果', f'鸡有{str(chickens)}只，兔子有{str(rabbits)}只')
                else:
                    box.showerror('无解', f'{head}个头，{feet}只脚的题目无解')
            except ZeroDivisionError:
                box.showerror('无解', f'{head}个头，{feet}只脚的题目无解')


        enter_head = enter_box.askinteger('输入', '头的数量', minvalue=1)
        enter_feet = enter_box.askinteger('输入', '脚的数量', minvalue=enter_head)
        main(enter_head, enter_feet)
    elif Home_Choice == '激活Windows(需要管理员权限)':
        box.showwarning('注意事项', """按下确定后几秒钟会弹出一个窗口。
在那个窗口中：
按下1:永久激活当前版本Windows
按下2:把Windows激活到2038年
按下3:把Windows和Office激活到180天后
(还是不会科学上网)""")
        os.system('start ActiveScript.bat')
    elif Home_Choice == '九九乘法表':
        box.showinfo('info', '乘法表将会在输出区内输出')
        print('九九乘法表：')
        for i in range(1, 10):
            for j in range(1, i + 1):
                print(f'{j}x{i}={i * j}', end='\t')
            print()
    elif Home_Choice == 'BMI检测':
        high = enter_box.askfloat('输入', '输入身高(m)', minvalue=0.1, maxvalue=2.0)
        weight = enter_box.askfloat('输入', '输入体重(kg)', minvalue=2.5, maxvalue=640.0)
        bmi = weight / (high ** 2)
        if bmi <= 18.4:
            box.showinfo('BMI', f'你的BMI值：{bmi} 温馨提示：你的体型偏瘦，要注意营养哦~')
        elif 18.4 < bmi <= 23.9:
            box.showinfo('BMI', f'你的BMI值：{bmi} 温馨提示：标准体型，继续保持哦~')
        elif 24 <= bmi <= 27.9:
            box.showinfo('BMI', f'你的BMI值：{bmi} 温馨提示：你的体型过胖，要注意身体哦~')
        elif bmi >= 28:
            box.showinfo('BMI', f'你的BMI值：{bmi} 温馨提示：你的体型肥胖，要注意饮食哦~')
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
    elif Home_Choice == '关于':
        box.showinfo('关于', version)
    elif Home_Choice is None:
        end_time = time.perf_counter()
        print(f'本次运行时间:{str(end_time - start_time)}秒')
        time.sleep(2)
        break
