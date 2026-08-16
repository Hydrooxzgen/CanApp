import tkinter.messagebox as boxes
import tkinter.simpledialog as enter_boxes

def start():
    formula = enter_boxes.askstring('计算器', '请输入式子：')
    answer = eval(formula)
    boxes.showinfo('答案', f'答案为：{answer}')
if __name__ == '__main__':
    start()

