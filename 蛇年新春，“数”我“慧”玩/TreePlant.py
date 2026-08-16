import tkinter.messagebox as boxes
import tkinter.simpledialog as enter_boxes
import easygui


def start():
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
if __name__ == '__main__':
    start()
