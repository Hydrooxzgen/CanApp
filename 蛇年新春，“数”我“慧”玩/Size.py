import tkinter.messagebox as boxes
import tkinter.simpledialog as enter_boxes
import easygui

pi = 3.14
def start():
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
if __name__ == '__main__':
    start()

