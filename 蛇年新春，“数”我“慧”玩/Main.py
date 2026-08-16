import easygui
import chicken_rabbit
import clac
import square_root
import average
import sys
import TreePlant
import Size

TOOLS = ['计算器', '鸡兔同笼', '计算平方根', '计算平均数', '解植树问题', '计算图形面积', '贪吃蛇']
def main():
    while True:
        tool = easygui.buttonbox('请选择功能', '蛇年新春，“数”我“慧”玩', TOOLS)
        if tool == '计算器':
            clac.start()
        elif tool == '鸡兔同笼':
            chicken_rabbit.start()
        elif tool == '计算平方根':
            square_root.start()
        elif tool == '计算平均数':
            average.start()
        elif tool == '解植树问题':
            TreePlant.start()
        elif tool == '计算图形面积':
            Size.start()
        elif tool == '贪吃蛇':
            import tcSnake1
            tcSnake1.main_menu()
        elif tool not in TOOLS:
            sys.exit()
main()
