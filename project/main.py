import numpy as np
from OpenGL.GL import *
from OpenGL.GLU import *
from OpenGL.GLUT import *
from PIL import Image
import numpy
import random

# 外边框参数
cubeVertices = (
    (1.5, 1.5, 1.5), (1.5, 1.5, -1.5), (1.5, -1.5, -1.5), (1.5, -1.5, 1.5), (-1.5, 1.5, 1.5), (-1.5, -1.5, -1.5),
    (-1.5, -1.5, 1.5), (-1.5, 1.5, -1.5))
cubeEdges = ((0, 1), (0, 3), (0, 4), (1, 2), (1, 7), (2, 5), (2, 3), (3, 6), (4, 6), (4, 7), (5, 6), (5, 7))

# 摄像机参数
IS_PERSPECTIVE = True  # 透视投影
VIEW = np.array([-0.8, 0.8, -0.8, 0.8, 0.1, 15.0])  # 视景体的left/right/bottom/top/near/far六个面
LEFT_IS_DOWNED = False
CameraPos = np.array([0.0, 0.0, 2])
CameraFront = np.array([0, 0, 0])
CameraUp = np.array([0, 1, 0])
SCALE_K = np.array([1, 1, 1])
yaw = 0
pitch = 0
MOUSE_X, MOUSE_Y = 0, 0

# 位置、速度参数
v_count = 0
v = 0
vx = 0.0
vy = 0.0
tempy = 0.0
a = -9.8  # 向下加速度
x = 0
y = 0
z = 0  # 球心坐标
t = 0.01
number = 100
vballX = [0.0 for i in range(number)]
vballY = [0.0 for i in range(number)]
vballZ = [0.0 for i in range(number)]
ballX = [0.0 for i in range(number)]
ballY = [0.0 for i in range(number)]
ballZ = [0.0 for i in range(number)]

# 判断指令
jump = False
flag = False
crash = False
warningFlag = False
winFlag = False

# 图片读取
image = Image.open("warning.bmp")
win_image = Image.open("winwarning.bmp")
guide = Image.open("guide.bmp")
array = numpy.array(image)
win_array = numpy.array(win_image)
guide_array = numpy.array(guide)
ImageWidth = 0
ImageHeight = 0


# 外边框绘制
def wireCube():
    glBegin(GL_LINES)
    for cubeEdge in cubeEdges:
        for cubeVertex in cubeEdge:
            glVertex3fv(cubeVertices[cubeVertex])
    glEnd()


# 小球初速度设置
def initVelocity():
    global v
    global v_count
    global vx
    global vy
    v = v_count
    vx = vx + v
    vy = vy + v


# 标靶碎片初速度设置
def initFragmentVelocity():
    global vballX
    global vballY
    global vballZ
    for i in range(number):
        vballX[i] = random.uniform(-6, 6)
        vballY[i] = random.uniform(-3, 3)
        vballZ[i] = random.uniform(-6, 6)


# 小球运动设置
def MoveBall():
    global x
    global vx
    global y
    global vy
    global tempy
    global v_count
    global jump
    global flag
    global warningFlag
    global winFlag

    x = x + vx * t
    vy = vy + a * t
    y = y + vy * t

    if y <= -1.5:
        vy = -vy
    if x >= 1.5 or x <= -1.5:
        vy = 0
        vx = 0
        v_count = 0
        warningFlag = True
    if flag:
        vx = -vx
        v_count = 0
        winFlag = True
        flag = False


# 标靶碎片运动设置
def MoveTarget():
    global ballY
    global ballX
    global ballZ
    global vballX
    global vballY
    global vballZ
    for i in range(number):
        vballY[i] = vballY[i] + a * t
        ballX[i] = ballX[i] + vballX[i] * t
        ballY[i] = ballY[i] + vballY[i] * t
        ballZ[i] = ballZ[i] + vballZ[i] * t
        if ballY[i] <= -1.5:
            vballY[i] = -vballY[i]
        if ballX[i] >= 1.5 or ballX[i] <= -1.5:
            vballX[i] = -vballX[i]
        if ballZ[i] >= 1.5 or ballZ[i] <= -1.5:
            vballZ[i] = -vballZ[i]


# 键盘按键监听
def keyDown(key, x1, y1):
    global jump
    global v_count
    global vx
    global vy
    global x
    global y
    global z
    global vballX
    global vballY
    global vballZ
    global ballX
    global ballY
    global ballZ
    global flag
    global warningFlag
    global winFlag

    if key == b'w':
        vy += 1
    elif key == b's':
        if vy >= 0:
            vy -= 1
    elif key == b'a':
        if vx >= 0:
            vx -= 1
    elif key == b'd':
        vx += 1
    elif key == b' ':
        if v_count <= 10:
            v_count += 1
        else:
            v_count = 0
    elif key == b'\r':
        initVelocity()
        initFragmentVelocity()
        jump = True
    elif key == b'r':
        v_count = 0
        vx = 0.0
        vy = 0.0
        x = -1.5
        y = -1.5
        z = 0  # 球心坐标
        vballX = [0 for i in range(number)]
        vballY = [0 for i in range(number)]
        vballZ = [0 for i in range(number)]
        ballX = [0 for i in range(number)]
        ballY = [0 for i in range(number)]
        ballZ = [0 for i in range(number)]
        glWindowPos2i(0, 500)
        jump = False
        flag = False
        warningFlag = False
        winFlag = False
    elif key == b'\x1b':
        exit(0)
    else:
        print("no")
        print(key)


# 初始化参数
def init():
    global x
    global y
    glClearColor(0.0, 0.0, 0.0, 1.0)  # 设置画布背景色。注意：这里必须是4个参数
    glEnable(GL_DEPTH_TEST)  # 开启深度测试，实现遮挡关系
    glDepthFunc(GL_LEQUAL)  # 设置深度测试函数（GL_LEQUAL只是选项之一）
    x = -1.5
    y = -1.5
    glClearColor(1.0, 1.0, 1.0, 0.0)
    glOrtho(-2.0, 2.0, -2.0, 2.0, 2.0, -4.0)


# 绘制函数
def display():
    global IS_PERSPECTIVE, VIEW
    global CameraPos, CameraFront, CameraUp
    global SCALE_K
    global WIN_W, WIN_H
    global angle
    global t
    glClear(GL_COLOR_BUFFER_BIT | GL_DEPTH_BUFFER_BIT)

    # 设置投影（透视投影）
    glMatrixMode(GL_PROJECTION)
    glLoadIdentity()

    # 设置模型视图
    glMatrixMode(GL_MODELVIEW)
    glLoadIdentity()

    # 几何变换
    glScale(0.5 * SCALE_K[0], 0.5 * SCALE_K[1], 0.5 * SCALE_K[2])

    # 视点
    gluLookAt(
        CameraPos[0], CameraPos[1], CameraPos[2],
        CameraFront[0], CameraFront[1], CameraFront[2],
        CameraUp[0], CameraUp[1], CameraUp[2]
    )
    # 碰撞检测
    CollisionDetector(x, y, z)
    # 绘制小球
    glColor3f(0.0, 0.0, 1.0)  # 当前颜色
    glPushMatrix()
    glTranslatef(x, y, 0)
    glutSolidSphere(0.1, 100, 100)
    glPopMatrix()
    # 绘制外边框
    glColor3f(1.0, 0.0, 0.0)
    glPushMatrix()
    wireCube()
    glPopMatrix()
    # 绘制标靶
    glColor3f(0.0, 1.0, 0.0)
    for i in range(number):
        glPushMatrix()
        glTranslatef(ballX[i], ballY[i], ballZ[i])
        glutSolidSphere(0.05, 100, 100)
        glPopMatrix()
    glColor3f(0.0, 0.0, 0.0)
    # 绘制操作引导图
    glWindowPos2i(0, 500)
    glDrawPixels(guide_array.shape[0], guide_array.shape[1], GL_RGB, GL_UNSIGNED_BYTE, guide_array)
    # 状态判断
    if not jump and not winFlag:
        glBegin(GL_LINES)
        glVertex3f(x, y, z)
        glVertex3f(vx + v_count - 1.5, vy + v_count - 1.5, z)
        glEnd()
    if warningFlag:
        showWarning(array)
    if winFlag:
        showWarning(win_array)
    glutSwapBuffers()  # 动画显示


# 定时器函数
def myTime(value):
    global jump
    global flag
    global crash
    global r
    # 判断小球发射
    if jump:
        MoveBall()
    # 判断小球与标靶碰撞
    if winFlag:
        MoveTarget()
    glutPostRedisplay()
    glutTimerFunc(33, myTime, 1)


# 碰撞检测函数
def CollisionDetector(x, y, z):
    global flag
    xDown = 0.1
    xUp = 0.1
    yDown = 0.1
    yUp = 0.1
    zDown = 0.1
    zUp = 0.1
    x = abs(x) - 0
    y = abs(y) - 0
    z = abs(z) - 0
    if (x < xDown or x < xUp) and (y < yDown or y < yUp) and (z < zDown or z < zUp):
        flag = True


# 击中状态和脱靶状态提醒
def showWarning(array):
    global ImageWidth
    global ImageHeight
    ImageWidth = array.shape[0]
    ImageHeight = array.shape[1]
    glWindowPos2i(250, 500)
    glDrawPixels(ImageWidth, ImageHeight, GL_RGB, GL_UNSIGNED_BYTE, array)


# 鼠标点击监听
def Mouse_click(button, state, x, y):
    global LEFT_IS_DOWNED
    global MOUSE_X, MOUSE_Y
    global SCALE_K

    MOUSE_X = x
    MOUSE_Y = y
    if button == GLUT_LEFT_BUTTON:
        LEFT_IS_DOWNED = state == GLUT_DOWN


# 鼠标移动监听
def Mouse_motion(x, y):
    global LEFT_IS_DOWNED
    global MOUSE_X, MOUSE_Y
    global yaw, pitch
    global CameraPos

    if LEFT_IS_DOWNED:
        dx = x - MOUSE_X
        dy = MOUSE_Y - y
        MOUSE_X = x
        MOUSE_Y = y

        sensitivity = 0.2
        dx = dx * sensitivity
        dy = dy * sensitivity

        yaw = yaw + dx
        pitch = pitch + dy

        if pitch > 89:
            pitch = 89
        if pitch < -89:
            pitch = -89

        CameraPos[0] = np.cos(np.radians(yaw)) * np.cos(np.radians(pitch))
        CameraPos[1] = np.sin(np.radians(pitch))
        CameraPos[2] = np.sin(np.radians(yaw)) * np.cos(np.radians(pitch))

        glutPostRedisplay()


# 主函数
if __name__ == "__main__":
    glutInit()  # glut初始化
    glutInitDisplayMode(GLUT_DOUBLE | GLUT_RGB)  # 显示模式
    glutInitWindowSize(800, 800)
    glutCreateWindow(" Hit The Target! ")  # 窗口名字
    init()  # 初始化相关参数
    glutDisplayFunc(display)  # 注册显示回调函数
    glutTimerFunc(33, myTime, 1)
    glutMouseFunc(Mouse_click)  # 初始化键盘鼠标交互
    glutMotionFunc(Mouse_motion)
    glutKeyboardFunc(keyDown)
    glutMainLoop()
