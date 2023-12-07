import numpy as np
import os
from colorama import Fore
from colorama import Style
from copy import deepcopy
import pygame
from pygame.constants import KEYDOWN
import bfs
import astar

'Thời gian cho các thuật toán: Ở đây cho 1800s ~ 30 phút'
HETTGIAN = 1800

'Tiến hành liên kết thư mục CheckPoints và TestCases'
path_Board = os.getcwd() + '\\..\\TestCases' # Liên kết với thư mục tạo map
path_CheckPoint = os.getcwd() + '\\..\\CheckPoints' # Liên kết với thư mục tạo điểm thắng trò chơi khi đặt hết 


'Tiến hành kiểm tra và trả lại 1 map tại thư mục TestCase'
def LayMap():
    os.chdir(path_Board)
    Dsach_Board = [] # Khởi tạo danh sách bản đồ
    for file in os.listdir(): # Duyệt qua tất cả các file có trong thư mục TestCase
        if file.endswith(".txt"):
            file_path = f"{path_Board}\{file}" # Tạo một đường dẫn đầy đủ đến file
            Board = get_board(file_path) # Đọc nội dung file bản đồ và lưu trữ vào Board
            Dsach_Board.append(Board) # Tiến hành thêm bản đồ vào danh sách 
    return Dsach_Board # Trả về danh sách bản đồ

'Tiến hành đọc một tập tin txt và tiến hành kiểm tra'
def get_pair(path):
    result = np.loadtxt(f"{path}", dtype=int, delimiter=',')
    return result

'Tiến hành kiểm tra và trả lại các điểm thắng tại thư mục CheckPoints'
def LayCheckPoints():
    os.chdir(path_CheckPoint)
    Dsach_CheckPoints = []
    for file in os.listdir():
        if file.endswith(".txt"):
            file_path = f"{path_CheckPoint}\{file}"
            Check_Point = get_pair(file_path)
            Dsach_CheckPoints.append(Check_Point)
    return Dsach_CheckPoints

'Định dạng lại tệp txt khi kiểm tra đầu vào'
def DDHang(row):
    for i in range(len(row)):
        if row[i] == '1':
            row[i] = '#'
        elif row[i] == 'p':
            row[i] = '@'
        elif row[i] == 'b':
            row[i] = '$'
        elif row[i] == 'c':
            row[i] = '%'

'Đọc file TXT của TestCase và kiểm tra'
def get_board(path):
    result = np.loadtxt(f"{path}", dtype=str, delimiter=',')
    for row in result:
        DDHang(row)
    return result

'Tiến hành khai báo, khởi tạo bản đồ và điểm kiểm tra '
Maps = LayMap()
Check_Points = LayCheckPoints()

'Khởi tạo trò chơi bằng pygame'
pygame.init()
pygame.font.init()
screen = pygame.display.set_mode((640, 640))
pygame.display.set_caption('AI - 5 - SOKOBAN')
clock = pygame.time.Clock()
BACKGROUND = (0, 0, 0)
WHITE = (255, 255, 255)



