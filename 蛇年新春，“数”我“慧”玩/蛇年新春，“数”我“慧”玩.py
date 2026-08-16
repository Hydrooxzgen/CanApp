import easygui
import sys
import tkinter.messagebox as boxes
import tkinter.simpledialog as enter_boxes
import easygui

def TreePlant():
    # Ask mode
    ask1 = easygui.buttonbox('请选择模式', '解植树问题', ['环形(封闭图形)', '直线植树'])

    # 初始化mode
    mode = None

    if ask1 == '环形(封闭图形)':
        mode = 'normal'
    elif ask1 == '直线植树':
        ask2 = easygui.buttonbox('请选择模式', '解植树问题', ['两边都种树', '两边都不种树', '一边种树，一边不种'])
        if ask2 == '两边都种树':
            mode = '+1'
        elif ask2 == '两边都不种树':
            mode = '-1'
        elif ask2 == '一边种树，一边不种':
            mode = 'normal'

    # 如果mode仍然是None，说明没有选择有效模式，提示用户重新选择
    if mode is None:
        boxes.showerror('错误', '请先选择一个有效的模式')
        return

    # Ask Data
    length = enter_boxes.askinteger('输入基本数据', '输入总长（周长）', )
    spacing_len = enter_boxes.askinteger('输入基本数据', '输入间距（每隔多长种一棵？）不带单位')

    # Start Compute
    trees_sum = length // spacing_len
    if mode == 'normal':
        boxes.showinfo('解', '共有' + str(trees_sum) + '棵树')
    elif mode == '+1':
        trees_sum += 1
        boxes.showinfo('解', '共有' + str(trees_sum) + '棵树')
    elif mode == '-1':
        trees_sum -= 1
        boxes.showinfo('解', '共有' + str(trees_sum) + '棵树')
pi = 3.14
def size():
    while True:
        shape = easygui.buttonbox('选择一个形状', '算面积', ['正方形', '长方形(平行四边形)', '三角形', '梯形', '圆形'])
        if shape == '正方形':
            a = enter_boxes.askfloat('输入信息', '请输入正方形的边长')
            size = a ** 2
            boxes.showinfo('面积', f'面积为：{size}')
        elif shape == '长方形(平行四边形)':
            a = enter_boxes.askfloat('输入信息', '请输入长方形的长')
            b = enter_boxes.askfloat('输入信息', '请输入长方形的宽(高)')
            size = a * b
            boxes.showinfo('面积', f'面积为：{size}')
        elif shape == '三角形':
            a = enter_boxes.askfloat('输入信息', '请输入三角形的底')
            h = enter_boxes.askfloat('输入信息', '请输入三角形的高')
            size = (a * h) / 2
            boxes.showinfo('面积', f'面积为：{size}')
        elif shape == '梯形':
            a = enter_boxes.askfloat('输入信息', '请输入梯形的上底')
            b = enter_boxes.askfloat('输入信息', '请输入梯形的下底')
            h = enter_boxes.askfloat('输入信息', '请输入梯形的高')
            size = (a + b) * h / 2
            boxes.showinfo('面积', f'面积为：{size}')
        elif shape == '圆形':
            r = enter_boxes.askfloat('输入信息', '请输入圆形的半径')
            size = pi * r ** 2
            boxes.showinfo('面积', f'面积为：{size}')
        elif shape is None:
            break

def clac():
    formula = enter_boxes.askstring('计算器', '请输入式子：')
    answer = eval(formula)
    boxes.showinfo('答案', f'答案为：{answer}')

def classic():
    chicken_feet = 2
    rabbit_feet = 4

    all_heads = enter_boxes.askinteger('鸡兔同笼', '一共有几个头？')
    all_feet = enter_boxes.askinteger('鸡兔同笼', '一共有几只脚？')
    rabbit = (all_feet - chicken_feet * all_heads) / (rabbit_feet - chicken_feet)
    chicken = all_heads - rabbit
    boxes.showinfo('答案', f'有{int(rabbit)}只兔 有{int(chicken)}只鸡')
def custom():
    a_name = enter_boxes.askstring('鸡兔同笼', 'a物品的名字(不重复)：')
    a_feet = enter_boxes.askinteger('鸡兔同笼', 'a物品的脚数(不重复)：')
    b_name = enter_boxes.askstring('鸡兔同笼', 'b物品的名字(不重复)：')
    b_feet = enter_boxes.askinteger('鸡兔同笼', 'b物品的脚数(不重复)：')
    all_heads = enter_boxes.askinteger('鸡兔同笼', '一共有个头？')
    all_feet = enter_boxes.askinteger('鸡兔同笼', '一共有几只脚？')
    if (a_name == b_name) or (a_feet == b_feet):
        boxes.showerror('错误', '名字/脚数 不能相同！')
    if a_feet > b_feet:
        a = (all_feet - b_feet * all_heads) / (a_feet - b_feet)
        b = all_heads - a
    elif a_feet < b_feet:
        b = (all_feet - a_feet * all_heads) / (b_feet - a_feet)
        a = all_heads - b
    boxes.showinfo('答案', f'{a_name}有{int(a)}只(个)，{b_name}有{int(b)}只(个)')
def chicken_rabbit():
    response = easygui.buttonbox('请选择模式：', '解鸡兔同笼问题', choices=['经典模式', '自定义模式'])
    if response == '经典模式':
        classic()
    elif response == '自定义模式':
        custom()
def average():
    numbers = []
    set_del_max_min = True
    while True:
        if set_del_max_min:
            del_max_min = boxes.askyesno('去除值', '你想要去除列表中的最大值和最小值吗？')
            set_del_max_min = False
        number = enter_boxes.askstring('计算平均数', '请输入一个数字，输入"start"开始计算，输入"exit"退出')
        if number == 'exit':
            numbers = []
            break
        elif numbers == [] and number == 'start':
            boxes.showerror('错误', '请输入数字！')
            set_del_max_min = False
            continue
        elif number != 'exit' and number != 'start':
            if number.isdecimal():
                number = int(number)
                numbers.append(number)
            else:
                boxes.showwarning('错误', '请输入整数！输入小数将去小数点及小数！')
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
            boxes.showinfo('平均数', f'它们的平均数为：{average}')
            numbers = []
            set_del_max_min = True
def square_root():
    number = enter_boxes.askfloat('开根号', '请输入你要开根号的数字')
    power = enter_boxes.askfloat('开根号', f'给{str(number)}开几次方？')
    answer = pow(number, 1/power)
    answer_int = int(answer)
    if answer_int == answer:
        boxes.showinfo('答案', f'答案为：{answer_int}')
    else:
        boxes.showinfo('答案', f'答案为：{answer}')
TOOLS = ['计算器', '鸡兔同笼', '计算平方根', '计算平均数', '解植树问题', '计算图形面积', '贪吃蛇']
def main():
    while True:
        tool = easygui.buttonbox('请选择功能', '蛇年新春，“数”我“慧”玩', TOOLS)
        if tool == '计算器':
            clac()
        elif tool == '鸡兔同笼':
            chicken_rabbit()
        elif tool == '计算平方根':
            square_root()
        elif tool == '计算平均数':
            average()
        elif tool == '解植树问题':
            TreePlant()
        elif tool == '计算图形面积':
            size()
        elif tool == '贪吃蛇':
            import tcSnake1
            tcSnake1.main_menu()
        elif tool not in TOOLS:
            sys.exit()
main()
