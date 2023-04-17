import cv2
import numpy as np
import win32gui

# 读取屏幕截图
import pyautogui


def capture_screen():
    # 获取窗口句柄
    hwnd = win32gui.FindWindow(None, '腾讯桌球')

    # 获取窗口位置
    left, top, right, bottom = win32gui.GetWindowRect(hwnd)

    # 获取窗口截图
    screenshot = pyautogui.screenshot(region=(left, top, right - left, bottom - top))
    # 获取球桌截图
    screenshot = screenshot.crop((123, 173, 915, 571))

    # screenshot.show()

    return screenshot


# 将PIL Image对象转换为OpenCV中的numpy数组
image_numpy = cv2.cvtColor(np.array(capture_screen()), cv2.COLOR_RGB2BGR)

# 将图像转换为灰度图像
gray = cv2.cvtColor(image_numpy, cv2.COLOR_BGR2GRAY)

# 高斯滤波
gaussian = cv2.GaussianBlur(gray, (1, 1), 0)

# 显示图像
cv2.imshow('Blurred Screenshot', gaussian)
processed_image = gaussian

# 检测圆形
circles = cv2.HoughCircles(processed_image, cv2.HOUGH_GRADIENT, 1, 10, param1=100, param2=30, minRadius=10,
                           maxRadius=50)

if circles is not None:
    circles = np.round(circles[0, :]).astype("int")

    for (x, y, r) in circles:
        cv2.circle(image_numpy, (x, y), r, (0, 255, 0), 1)

# 检测直线
edges = cv2.Canny(processed_image, 50, 150)
lines = cv2.HoughLines(edges, 1, np.pi / 180, 200)

if lines is not None:
    for line in lines:
        rho, theta = line[0]
        a, b = np.cos(theta), np.sin(theta)
        x0, y0 = a * rho, b * rho
        x1, y1 = int(x0 + 1000 * (-b)), int(y0 + 1000 * a)
        x2, y2 = int(x0 - 1000 * (-b)), int(y0 - 1000 * a)
        cv2.line(image_numpy, (x1, y1), (x2, y2), (0, 0, 255), 1)

# 显示结果
cv2.imshow("Image", image_numpy)
cv2.waitKey(0)
cv2.destroyAllWindows()
