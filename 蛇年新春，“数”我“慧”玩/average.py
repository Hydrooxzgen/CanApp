import tkinter.messagebox as boxes
import tkinter.simpledialog as enter_boxes

def start():
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
if __name__ == '__main__':
    start()

