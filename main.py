import time
import winsound

import cv2
import numpy as np
import pyautogui


# 捕获屏幕截图
def capture_screen():
    screenshot = pyautogui.screenshot()
    screenshot.show()
    screen = np.array(screenshot)
    screen = cv2.cvtColor(screen, cv2.COLOR_RGB2BGR)
    return screen


# 识别台球和球杆的位置
def detect_cue_ball(image):
    # TODO: 实现台球和球杆的识别算法

    # 将图像转换为灰度图
    gray = cv2.cvtColor(image, cv2.COLOR_BGR2GRAY)

    # 对图像进行高斯模糊和Canny边缘检测
    blurred = cv2.GaussianBlur(gray, (11, 11), 0)
    edges = cv2.Canny(blurred, 30, 150)

    # 对边缘图像进行膨胀操作，填充边缘
    kernel = cv2.getStructuringElement(cv2.MORPH_ELLIPSE, (5, 5))
    dilated = cv2.dilate(edges, kernel)

    # 在边缘图像中寻找圆形区域，用于定位台球和球杆
    circles = cv2.HoughCircles(dilated, cv2.HOUGH_GRADIENT, 1, 100,
                               param1=30, param2=20, minRadius=15, maxRadius=50)

    # 如果没有找到圆形区域，返回空
    if circles is None:
        return None, None

    # 在圆形区域周围绘制圆形，用于可视化和调试
    for (x, y, r) in circles[0, :]:
        cv2.circle(image, (x, y), r, (0, 255, 0), 2)

    # 筛选圆形区域，用于定位台球和球杆
    cue_ball_center = None
    cue_stick_center = None
    for (x, y, r) in circles[0, :]:
        # 判断圆形是否位于屏幕中央，如果不是则视为球杆
        if abs(x - image.shape[1] / 2) < image.shape[1] / 4:
            cue_ball_center = (x, y)
        else:
            cue_stick_center = (x, y)

    # 返回定位结果
    return cue_ball_center, cue_stick_center


# 计算击球方向和力度
def calculate_shot(cue_ball_center, cue_stick_center):
    # TODO: 实现计算击球方向和力度的算法
    direction = (1, 0)
    strength = 100
    return direction, strength


# 模拟击球
def simulate_shot(direction, strength):
    # 根据击球方向和力度计算鼠标移动距离
    x = direction[0] * strength
    y = direction[1] * strength

    # 将鼠标移动到击球位置
    pyautogui.moveTo(cue_stick_center[0], cue_stick_center[1])

    # 模拟鼠标按下
    pyautogui.mouseDown()

    # 移动鼠标
    pyautogui.moveRel(x, y)

    # 模拟鼠标松开
    pyautogui.mouseUp()


# 主程序
if __name__ == "__main__":

    for i in range(3):
        winsound.Beep(2000, 200)
        time.sleep(.8)
    winsound.Beep(3000, 400)

    # 捕获屏幕截图
    image = capture_screen()
    # pyautogui.screenshot().show()

    # 识别台球和球杆的位置
    cue_ball_center, cue_stick_center = detect_cue_ball(image)

    # 计算击球方向和力度
    direction, strength = calculate_shot(cue_ball_center, cue_stick_center)

    # 模拟击球
    simulate_shot(direction, strength)
