import tkinter.messagebox as boxes
import tkinter.simpledialog as enter_boxes
import easygui


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
def start():
    response = easygui.buttonbox('请选择模式：', '解鸡兔同笼问题', choices=['经典模式', '自定义模式'])
    if response == '经典模式':
        classic()
    elif response == '自定义模式':
        custom()
if __name__ == '__main__':
    start()
