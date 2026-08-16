import tkinter.messagebox as boxes
import tkinter.simpledialog as enter_boxes

def start():
    number = enter_boxes.askfloat('开根号', '请输入你要开根号的数字')
    power = enter_boxes.askfloat('开根号', f'给{str(number)}开几次方？')
    answer = pow(number, 1/power)
    answer_int = int(answer)
    if answer_int == answer:
        boxes.showinfo('答案', f'答案为：{answer_int}')
    else:
        boxes.showinfo('答案', f'答案为：{answer}')
if __name__ == '__main__':
    start()

