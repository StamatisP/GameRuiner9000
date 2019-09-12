import win32api
import win32con
import time
import random
import config
import threading
import win32gui
import scipy
from scipy import interpolate
import mouse
import sys


def threadedEvent(func, arg=0):
    if func == "jitter":
        _x = threading.Thread(target = jitterMouse)
        _x.start()
    elif func == "lock":
        _x = threading.Thread(target = lockMouse)
        _x.start()
    elif func == "lclick":
        _x = threading.Thread(target=clickMouse, args=("LEFT",))
        _x.start()
    elif func == "rclick":
        _x = threading.Thread(target=clickMouse, args=("RIGHT",))
        _x.start()
    elif func == "slow":
        _x = threading.Thread(target=slowMouse)
        _x.start()
    elif func == "bezier":
        _x = threading.Thread(target=bezierMouse)
        _x.start()
    elif func == "zawarudo":
        _x = threading.Thread(target=zaWarudo)
        _x.start()
    elif func == "escape":
        _x = threading.Thread(target=checkEscape)
        _x.start()
    elif func == "move":
        _x = threading.Thread(target=moveSelf, args=(arg,))
        _x.start()
    elif func == "dance":
        _x = threading.Thread(target=danceTime)
        _x.start()

def jitterMouse():
    #if isJittering:
    #    return
    #isJittering = True
    #print('leaguetest_support.jitterMouse')
    t_end = time.time() + 2
    while time.time() < t_end:
        time.sleep(0.001)
        _x, _y = win32api.GetCursorPos()
        #print(_x)
        #print(_y)
        _x = _x + random.randint(*config.jittermouserange)
        _y = _y + random.randint(*config.jittermouserange)
        win32api.SetCursorPos((_x, _y))
        #if random.randint(0, 100) > 50:
        #    win32api.mouse_event(win32con.MOUSEEVENTF_LEFTDOWN, _x, _y, 0, 0)
        #    win32api.mouse_event(win32con.MOUSEEVENTF_LEFTUP, _x, _y, 0, 0)


def lockMouse():
    oldX, oldY = win32api.GetCursorPos()
    t_end = time.time() + 5
    while time.time() < t_end:
        win32api.SetCursorPos((oldX, oldY))


def clickMouse(side):
    oldX, oldY = win32api.GetCursorPos()
    if side == "LEFT":
        win32api.mouse_event(win32con.MOUSEEVENTF_LEFTDOWN, oldX, oldY, 0, 0)
        win32api.mouse_event(win32con.MOUSEEVENTF_LEFTUP, oldX, oldY, 0, 0)
    elif side == "RIGHT":
        win32api.mouse_event(win32con.MOUSEEVENTF_RIGHTDOWN, oldX, oldY, 0, 0)
        win32api.mouse_event(win32con.MOUSEEVENTF_RIGHTUP, oldX, oldY, 0, 0)


def randomAbility():
    randabil = random.randint(1, 4)
    Q = 0x51
    W = 0x57
    E = 0x45
    R = 0x52
    # maybe in the future it can be weighted? ults get used less?
    if randabil == 1:
        win32api.keybd_event(Q, 0, win32con.KEYEVENTF_EXTENDEDKEY, 0)
        time.sleep(0.1)
        win32api.keybd_event(Q, 0, win32con.KEYEVENTF_EXTENDEDKEY | win32con.KEYEVENTF_KEYUP, 0)
    elif randabil == 2:
        win32api.keybd_event(W, 0, win32con.KEYEVENTF_EXTENDEDKEY, 0)
        time.sleep(0.1)
        win32api.keybd_event(W, 0, win32con.KEYEVENTF_EXTENDEDKEY | win32con.KEYEVENTF_KEYUP, 0)
    elif randabil == 3:
        win32api.keybd_event(E, 0, win32con.KEYEVENTF_EXTENDEDKEY, 0)
        time.sleep(0.1)
        win32api.keybd_event(E, 0, win32con.KEYEVENTF_EXTENDEDKEY | win32con.KEYEVENTF_KEYUP, 0)
    elif randabil == 4:
        win32api.keybd_event(R, 0, win32con.KEYEVENTF_EXTENDEDKEY, 0)
        time.sleep(0.1)
        win32api.keybd_event(R, 0, win32con.KEYEVENTF_EXTENDEDKEY | win32con.KEYEVENTF_KEYUP, 0)


def randomItem():
    randitem = random.randint(1, 7)
    if randitem == 1:
        win32api.keybd_event(0x31, 0, 0, 0)
        time.sleep(0.1)
        win32api.keybd_event(0x31, 0, win32con.KEYEVENTF_KEYUP, 0)
    elif randitem == 2:
        win32api.keybd_event(0x32, 0, 0, 0)
        time.sleep(0.1)
        win32api.keybd_event(0x32, 0, win32con.KEYEVENTF_KEYUP, 0)
    elif randitem == 3:
        win32api.keybd_event(0x33, 0, 0, 0)
        time.sleep(0.1)
        win32api.keybd_event(0x33, 0, win32con.KEYEVENTF_KEYUP, 0)
    elif randitem == 4:
        win32api.keybd_event(0x34, 0, 0, 0)
        time.sleep(0.1)
        win32api.keybd_event(0x34, 0, win32con.KEYEVENTF_KEYUP, 0)
    elif randitem == 5:
        win32api.keybd_event(0x35, 0, 0, 0)
        time.sleep(0.1)
        win32api.keybd_event(0x35, 0, win32con.KEYEVENTF_KEYUP, 0)
    elif randitem == 6:
        win32api.keybd_event(0x36, 0, 0, 0)
        time.sleep(0.1)
        win32api.keybd_event(0x36, 0, win32con.KEYEVENTF_KEYUP, 0)
    elif randitem == 7:
        win32api.keybd_event(0x37, 0, 0, 0)
        time.sleep(0.1)
        win32api.keybd_event(0x37, 0, win32con.KEYEVENTF_KEYUP, 0)


def slowMouse():
    speed = win32gui.SystemParametersInfo(win32con.SPI_GETMOUSESPEED)
    newspeed = speed / 2
    win32gui.SystemParametersInfo(win32con.SPI_SETMOUSESPEED, newspeed)
    time.sleep(3)
    win32gui.SystemParametersInfo(win32con.SPI_SETMOUSESPEED, speed)


#dont use
def bezierMouse():
    t_end = time.time() + 2
    while time.time() < t_end:
        cp = random.randint(3, 5)  # Number of control points. Must be at least 2.
        x1, y1 = win32api.GetCursorPos()  # Starting position
        time.sleep(0.01)
        x2, y2 = win32api.GetCursorPos()  # Destination

        # Distribute control points between start and destination evenly.
        x = scipy.linspace(x1, x2, num=cp, dtype='int')
        y = scipy.linspace(y1, y2, num=cp, dtype='int')

        # Randomise inner points a bit (+-RND at most).
        RND = 10
        xr = scipy.random.randint(-RND, RND, size=cp)
        yr = scipy.random.randint(-RND, RND, size=cp)
        xr[0] = yr[0] = xr[-1] = yr[-1] = 0
        x += xr
        y += yr

        # Approximate using Bezier spline.
        degree = 3 if cp > 3 else cp - 1  # Degree of b-spline. 3 is recommended.
        # Must be less than number of control points.
        tck, u = scipy.interpolate.splprep([x, y], k=degree)
        screensize = (win32api.GetSystemMetrics(win32con.SM_CXSCREEN), win32api.GetSystemMetrics(win32con.SM_CYSCREEN))
        u = scipy.linspace(0, 1, num=max(screensize))
        points = scipy.interpolate.splev(u, tck)

        # Move mouse.
        duration = 0.1
        timeout = duration / len(points[0])
        for point in zip(*(i.astype(int) for i in points)):
            win32api.SetCursorPos(point)
            time.sleep(timeout)


def reverseMouseEvent(events):
    newEvents = []
    #print(sorted(events, key=lambda x: int(x[1])))
    #for event in events:
        #print(sorted(events))

def zaWarudo():
    #x1, y1 = win32api.GetCursorPos()
    recorded = []
    mouse.hook(recorded.append)
    time.sleep(3)
    mouse.unhook(recorded.append)
    #print(recorded)
    print("not funny, didnt happen")
    mouse.play(reverseMouseEvent(recorded))


def checkEscape():
    while True:
        if win32api.GetAsyncKeyState(win32con.VK_ESCAPE):
            sys.exit()


def moveSelf(direction):
    W = 0x57
    A = 0x41
    S = 0x53
    D = 0x44
    t_end = time.time() + 3
    if direction == "LEFT":
        while time.time() < t_end:
            win32api.keybd_event(A, 0, 0, 0)
            time.sleep(0.05)
        win32api.keybd_event(A, win32con.KEYEVENTF_KEYUP, 0, 0)
    if direction == "RIGHT":
        while time.time() < t_end:
            win32api.keybd_event(D, 0, 0, 0)
            time.sleep(0.05)
        win32api.keybd_event(D, win32con.KEYEVENTF_KEYUP, 0, 0)
    if direction == "UP":
        while time.time() < t_end:
            win32api.keybd_event(W, 0, 0, 0)
            time.sleep(0.05)
        win32api.keybd_event(W, win32con.KEYEVENTF_KEYUP, 0, 0)
    if direction == "DOWN":
        while time.time() < t_end:
            win32api.keybd_event(S, 0, 0, 0)
            time.sleep(0.05)
        win32api.keybd_event(S, win32con.KEYEVENTF_KEYUP, 0, 0)


def danceTime():
    W = 0x57
    A = 0x41
    S = 0x53
    D = 0x44
    t_end = time.time() + 3
    while time.time() < t_end:
        rnd = random.randint(0, 3)
        if rnd == 0:
            win32api.keybd_event(A, 0, 0, 0)
            time.sleep(0.05)
            win32api.keybd_event(A, win32con.KEYEVENTF_KEYUP, 0, 0)
        elif rnd == 1:
            win32api.keybd_event(S, 0, 0, 0)
            time.sleep(0.05)
            win32api.keybd_event(S, win32con.KEYEVENTF_KEYUP, 0, 0)
        elif rnd == 2:
            win32api.keybd_event(W, 0, 0, 0)
            time.sleep(0.05)
            win32api.keybd_event(W, win32con.KEYEVENTF_KEYUP, 0, 0)
        elif rnd == 3:
            win32api.keybd_event(D, 0, 0, 0)
            time.sleep(0.05)
            win32api.keybd_event(D, win32con.KEYEVENTF_KEYUP, 0, 0)

        time.sleep(0.1)