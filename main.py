import ctypes
import math
import time
from ctypes import wintypes
import random
from concurrent.futures import ThreadPoolExecutor

import threading
# Define necessary ctypes and structures
user32 = ctypes.WinDLL('user32', use_last_error=True)
gdi32 = ctypes.WinDLL('gdi32', use_last_error=True)
errorCode = user32.SetProcessDPIAware()

GetDC = user32.GetDC
GetDC.restype = wintypes.HDC
GetDC.argtypes = [wintypes.HWND]

ReleaseDC = user32.ReleaseDC
ReleaseDC.restype = ctypes.c_int
ReleaseDC.argtypes = [wintypes.HWND, wintypes.HDC]

CreateCompatibleDC = gdi32.CreateCompatibleDC
CreateCompatibleDC.restype = wintypes.HDC
CreateCompatibleDC.argtypes = [wintypes.HDC]

CreateCompatibleBitmap = gdi32.CreateCompatibleBitmap
CreateCompatibleBitmap.restype = wintypes.HBITMAP
CreateCompatibleBitmap.argtypes = [wintypes.HDC, ctypes.c_int, ctypes.c_int]

SelectObject = gdi32.SelectObject
SelectObject.restype = wintypes.HGDIOBJ
SelectObject.argtypes = [wintypes.HDC, wintypes.HGDIOBJ]

BitBlt = gdi32.BitBlt
BitBlt.restype = ctypes.c_bool
BitBlt.argtypes = [wintypes.HDC, ctypes.c_int, ctypes.c_int, ctypes.c_int, ctypes.c_int,
                   wintypes.HDC, ctypes.c_int, ctypes.c_int, ctypes.c_ulong]

ROP_DstInvert = 0x00550009
ROP_SrcPaint = 0x00EE0086
ROP_SrcCopy = 0x00CC0020

StretchBlt = gdi32.StretchBlt
StretchBlt.restype = ctypes.c_bool
StretchBlt.argtypes = [
    wintypes.HDC,  # hDestDC
    ctypes.c_int,  # xDest
    ctypes.c_int,  # yDest
    ctypes.c_int,  # wDest
    ctypes.c_int,  # hDest
    wintypes.HDC,  # hSrcDC
    ctypes.c_int,  # xSrc
    ctypes.c_int,  # ySrc
    ctypes.c_int,  # wSrc
    ctypes.c_int,  # hSrc
    ctypes.c_ulong # dwRop
]

import ctypes
from ctypes import wintypes

# Additional imports and definitions as needed

# Define additional necessary ctypes and structures
CreateDIBSection = gdi32.CreateDIBSection
SetDIBitsToDevice = gdi32.SetDIBitsToDevice

class BITMAPINFOHEADER(ctypes.Structure):
    _fields_ = [
        ('biSize',          wintypes.DWORD),
        ('biWidth',         ctypes.c_long),
        ('biHeight',        ctypes.c_long),
        ('biPlanes',        wintypes.WORD),
        ('biBitCount',      wintypes.WORD),
        ('biCompression',   wintypes.DWORD),
        ('biSizeImage',     wintypes.DWORD),
        ('biXPelsPerMeter', ctypes.c_long),
        ('biYPelsPerMeter', ctypes.c_long),
        ('biClrUsed',       wintypes.DWORD),
        ('biClrImportant',  wintypes.DWORD)
    ]

class BITMAPINFO(ctypes.Structure):
    _fields_ = [
        ('bmiHeader', BITMAPINFOHEADER),
  # Assuming no color table is needed for a 32-bit DIB
    ]

executor = ThreadPoolExecutor(max_workers=1)

# Get screen dimensions
screen_width = user32.GetSystemMetrics(0)
screen_height = user32.GetSystemMetrics(1)

# Function to apply color shifting to a block
def color_shift(hdc, x, y, width, height):
    # Inverting colors of the block to give a shifting effect
    BitBlt(hdc, x, y, width, height, hdc, x, y, ROP_DstInvert)


def screen_tunneling(hdc, width, height):
    for i in range(50, 0, -1):
        radius = int((min(width, height) / 2) * (i / 50))
        BitBlt(hdc, width // 2 - radius, height // 2 - radius, radius * 2, radius * 2,
               hdc, width // 2 - radius, height // 2 - radius, ROP_SrcPaint)

def warping(hdc, width, height):
    for y in range(0, height, 20):
        offset = int(math.sin(y / 20) * 20)
        BitBlt(hdc, 0, y, width, 20, hdc, offset, y, ROP_SrcPaint)

def distortion(hdc, width, height):
    for y in range(0, height, 5):
        offset = random.randint(-20, 20)
        BitBlt(hdc, 0, y, width, 5, hdc, offset, y, ROP_SrcPaint)

def shake(hdc, width, height):
    x_offset = random.randint(-10, 10)
    y_offset = random.randint(-10, 10)
    BitBlt(hdc, x_offset, y_offset, width - abs(x_offset), height - abs(y_offset), hdc, 0, 0, 0xCC0020)

def ripple(hdc, width, height, frequency=random.randint(10,30), amplitude=random.randint(10,30)):
    for y in range(0, height, 2):
        offset = int(math.sin(y / frequency) * amplitude)
        BitBlt(hdc, 0, y, width, 2, hdc, offset, y, ROP_SrcPaint)

def checkerboard_glitch(hdc, width, height, block_size=random.randint(50,100)):
    for y in range(0, height, block_size):
        for x in range(0, width, block_size):
            if (x + y) // block_size % 2 == 0:
                BitBlt(hdc, x, y, block_size, block_size, hdc, x, y, ROP_DstInvert)

def random_rectangle_fill(hdc, width, height, num_rectangles=random.randint(10,20)):
    for _ in range(num_rectangles):
        x = random.randint(0, width)
        y = random.randint(0, height)
        rect_width = random.randint(10, 100)
        rect_height = random.randint(10, 100)
        BitBlt(hdc, x, y, rect_width, rect_height, hdc, x, y, random.choice([0x660046, ROP_DstInvert]))

# Function to apply multiplication effect (kaleidoscope-like effect)
def multiplication(hdc, width, height):
    # Multiplication effect by dividing the screen and mirroring the parts
    quarter_width, quarter_height = width // 4, height // 4
    BitBlt(hdc, quarter_width, quarter_height, quarter_width * 2, quarter_height * 2,
           hdc, 0, 0, ROP_SrcPaint)
    BitBlt(hdc, 0, quarter_height, quarter_width, quarter_height * 2,
           hdc, quarter_width * 3, quarter_height, ROP_SrcPaint)
    BitBlt(hdc, quarter_width, 0, quarter_width * 2, quarter_height,
           hdc, quarter_width, quarter_height * 3, ROP_SrcPaint)

# Function to apply RGB shift effect
def rgb_shift(hdc, width, height, shift_amount=random.randint(5,10)):
    # Shift the red, green, and blue components separately
    red_shift = (shift_amount, 0)
    green_shift = (0, shift_amount)
    for y in range(0, height, 2):
        # Apply a horizontal shift for the red channel
        BitBlt(hdc, red_shift[0], y, width - red_shift[0], 2, hdc, 0, y, ROP_SrcCopy)
        # Apply a vertical shift for the green channel
        BitBlt(hdc, 0, y + green_shift[1], width, 2, hdc, 0, y, ROP_SrcCopy)


def full_screen_ripple(hdc, width, height, frequency=random.randint(20,40), amplitude=random.randint(15,30)):
    for y in range(0, height, 1):
        offset = int(math.sin(y / frequency) * amplitude)
        BitBlt(hdc, 0, y, width, 1, hdc, offset, y, ROP_SrcCopy)


def complex_distortion(hdc, width, height, distortion_amount=random.randint(10,20)):
    for y in range(0, height, 5):
        for x in range(0, width, 5):
            offset_x = random.randint(-distortion_amount, distortion_amount)
            offset_y = random.randint(-distortion_amount, distortion_amount)
            BitBlt(hdc, x + offset_x, y + offset_y, 5, 5, hdc, x, y, ROP_SrcCopy)

def apply_glitch_threaded(glitch_function, *args, **kwargs):
       executor.submit(glitch_function, *args, **kwargs)


def line_glitch(hdc, width, height, line_thickness=random.randint(1,2)):
    for x in range(0, width, line_thickness):
        BitBlt(hdc, x, 0, line_thickness, height, hdc, x, random.randint(0, height), ROP_SrcCopy)
    for y in range(0, height, line_thickness):
        BitBlt(hdc, 0, y, width, line_thickness, hdc, random.randint(0, width), y, ROP_SrcCopy)

def screen_flicker(hdc, width, height):
    BitBlt(hdc, 0, 0, width, height, hdc, 0, 0, ROP_DstInvert)

def wave_distortion(hdc, width, height, wave_amplitude=random.randint(20,40), wave_frequency=random.uniform(0.1,0.2)):
    for x in range(0, width, 2):
        offset = int(math.sin(x * wave_frequency) * wave_amplitude)
        BitBlt(hdc, x, offset, 2, height - abs(offset), hdc, x, 0, ROP_SrcCopy)

def pixelate(hdc, width, height, block_size=random.randint(10,20)):
    for y in range(0, height, block_size):
        for x in range(0, width, block_size):
            BitBlt(hdc, x, y, block_size, block_size, hdc, x + block_size // 2, y + block_size // 2, ROP_SrcCopy)

def fragmentation(hdc, width, height, fragment_size=random.randint(50,100)):
    for _ in range(random.randint(10,20)):
        src_x = random.randint(0, width - fragment_size)
        src_y = random.randint(0, height - fragment_size)
        dst_x = random.randint(0, width - fragment_size)
        dst_y = random.randint(0, height - fragment_size)
        BitBlt(hdc, dst_x, dst_y, fragment_size, fragment_size, hdc, src_x, src_y, ROP_SrcCopy)

def chaotic_scramble(hdc, width, height, scramble_size=random.randint(50,100), scramble_amount=random.randint(50,100)):
    for _ in range(scramble_amount):
        src_x = random.randint(0, width - scramble_size)
        src_y = random.randint(0, height - scramble_size)
        dst_x = random.randint(0, width - scramble_size)
        dst_y = random.randint(0, height - scramble_size)
        BitBlt(hdc, dst_x, dst_y, scramble_size, scramble_size, hdc, src_x, src_y, ROP_SrcCopy)

SM_CXSCREEN = 0
SM_CYSCREEN = 1
SM_CXICON = 11
SM_CYICON = 12
LoadIcon = ctypes.windll.user32.LoadIconW
LoadIcon.argtypes = [wintypes.HINSTANCE, wintypes.LPCWSTR]
LoadIcon.restype = wintypes.HICON



# Get functions from the DLLs
GetSystemMetrics = user32.GetSystemMetrics
GetDesktopWindow = user32.GetDesktopWindow
GetWindowDC = user32.GetWindowDC
ReleaseDC = user32.ReleaseDC
DrawIcon = user32.DrawIcon
LoadIcon = user32.LoadIconW
# Pre-calculate the screen width and height
scrw = GetSystemMetrics(SM_CXSCREEN)
scrh = GetSystemMetrics(SM_CYSCREEN)

# Define a function to convert the identifier to the right resource format
def MAKEINTRESOURCE(i):
    return wintypes.LPWSTR(i & 0xFFFF)

# Predefined system icon identifiers
IDI_APPLICATION = MAKEINTRESOURCE(32512)
IDI_HAND = MAKEINTRESOURCE(32513)
IDI_QUESTION = MAKEINTRESOURCE(32514)
IDI_EXCLAMATION = MAKEINTRESOURCE(32515)
IDI_ASTERISK = MAKEINTRESOURCE(32516)
IDI_WINLOGO = MAKEINTRESOURCE(32517)
IDI_SHIELD = MAKEINTRESOURCE(32518)  # May not be available in older versions of Windows

# Load icons using predefined identifiers
hIconApp = LoadIcon(0, IDI_APPLICATION)
hIconHand = LoadIcon(0, IDI_HAND)
hIconQuestion = LoadIcon(0, IDI_QUESTION)
hIconExclamation = LoadIcon(0, IDI_EXCLAMATION)
hIconAsterisk = LoadIcon(0, IDI_ASTERISK)
hIconWinLogo = LoadIcon(0, IDI_WINLOGO)
hIconShield = LoadIcon(0, IDI_SHIELD)  # Check availability

# Get the Desktop window and its device context
hwnd = GetDesktopWindow()
hdc = GetWindowDC(hwnd)

def icon():
    time.sleep(5)
    while True:
        icons = [hIconApp, hIconHand, hIconQuestion, hIconExclamation, hIconAsterisk, hIconWinLogo, hIconShield]
        for i in range(10):
            for icon in icons:
                x_pos = random.randint(0, scrw)
                y_pos = random.randint(0, scrh)
                DrawIcon(hdc, x_pos, y_pos, icon)


def color_cycling(hdc, width, height):
    for i in range(3):  # Cycle colors
        BitBlt(hdc, 0, 0, width, height, hdc, 0, 0, ROP_DstInvert | (ROP_DstInvert << (8 * i)))


CHANCE = 0.005

def apply_shader_effect():
    hdc_screen = GetDC(None)
    hdc_buffer = CreateCompatibleDC(hdc_screen)
    hbm_buffer = CreateCompatibleBitmap(hdc_screen, screen_width, screen_height)
    SelectObject(hdc_buffer, hbm_buffer)

    try:
        # Create an infinite loop to continuously apply effects
        while True:
            BitBlt(hdc_buffer, 0, 0, screen_width, screen_height, hdc_screen, 0, 0, ROP_SrcCopy)

            # Initialize a list to keep track of threads
            threads = []

            # List of possible glitch effects
            glitch_effects = [
                screen_tunneling, warping, distortion, multiplication,
                shake, ripple, checkerboard_glitch, random_rectangle_fill,
                rgb_shift, full_screen_ripple, complex_distortion, line_glitch,
                screen_flicker, wave_distortion, pixelate, fragmentation,
                chaotic_scramble
            ]

            # Apply random glitch effects based on CHANCE
            for effect in glitch_effects:
                if random.random() < CHANCE:
                    thread = threading.Thread(target=apply_glitch_threaded, args=(effect, hdc_buffer, screen_width, screen_height))
                    threads.append(thread)
                    thread.start()
                    BitBlt(hdc_screen, 0, 0, screen_width, screen_height, hdc_buffer, 0, 0, ROP_SrcCopy)

            # Wait for all threads to finish before updating the screen
            for thread in threads:
                thread.join()


    finally:
        # Clean up resources
        ReleaseDC(None, hdc_screen)
        gdi32.DeleteObject(SelectObject(hdc_buffer, hbm_buffer))
        gdi32.DeleteDC(hdc_buffer)


def increase_max_workers_periodically(interval=0.25):
    global CHANCE
    while True:
        current_max_workers = executor._max_workers
        if current_max_workers >= 200:
            print("Reached the maximum number of workers.")
            break  # Exit the loop if max workers reached
        new_max_workers = min(current_max_workers + 1, 200)  # Do not exceed 150 workers
        CHANCE = min(CHANCE + 0.005, 1.0)  # Do not exceed a CHANCE of 1.0

        # Increase the internal max_workers value of the ThreadPoolExecutor
        executor._max_workers = new_max_workers
        # Manually create and add a new worker thread to the pool
        t = threading.Thread(target=executor._adjust_thread_count)
        t.daemon = True
        t.start()

        print(f"WORKERS: {new_max_workers}")
        print(f"CHANCE: {CHANCE}")
        time.sleep(interval)  # Wait for the specified interval before increasing max workers again

if __name__ == '__main__':
    # Start the thread to increase max workers every second
    increase_workers_thread = threading.Thread(target=increase_max_workers_periodically)
    increase_workers_thread.daemon = True
    increase_workers_thread.start()

    iconthread = threading.Thread(target=icon)
    iconthread.daemon = True
    iconthread.start()

    # Start applying shader effect
    apply_shader_effect()