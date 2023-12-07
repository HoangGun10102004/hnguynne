from copy import deepcopy

HETTGIAN = 1800

'Đây là bộ chứa dữ liệu cho các trạng thái của từng bước'

class state:
    def __init__(self, board, state_parent, list_check_point): #(Bảng lưu trữ hiện tại, Trạng thái cha của trạng thái này, Danh sách các điểm kiểm tra)
        self.board = board #
        self.state_parent = state_parent
        self.cost = 1 # Chi phí để chuyển từ trạng thái cha sang trạng thái hiện tại ( Mặc định là 1)
        self.heuristic = 0 # Uớc lượng được sử dụng trong thuật toán A* để ước lượng chi phí từ trạng thái hiện tại đến trạng thái mục tiêu.
        self.check_points = deepcopy(list_check_point) # Tạo một bản sao độc lập của list_check_point
    ''
    def get_line(self):
        'Tiến hành sử dụng đệ quy để tìm danh sách các bảng từ trạng thái ban đầu đến trạng thái hiện tại.'
        if self.state_parent is None: # Trạng thái hiện tại không có trạng thái cha -> nó là trạng thái ban đầu
            return [self.board] # Trả về bảng của trạng thái hiện tại
        return (self.state_parent).get_line() + [self.board] # Tạo ra một danh sách các bảng từ trạng thái ban đầu đến trạng thái hiện tại.
    'Tính toán hàm ước lượng được sử dụng cho thuật toán A*'
    def compute_heuristic(self):
        list_boxes = TimVTHop(self.board)
        if self.heuristic == 0:
            # Tính toán giá trị của hàm ước lượng bằng cách cộng self.cost (chi phí) với tổng khoảng cách Manhattan từ mỗi hộp đến điểm kiểm tra tương ứng. Khoảng cách Manhattan được tính bằng cách lấy tổng giá trị tuyệt đối của hiệu giữa tọa độ x và y của hộp và tọa độ x và y của điểm kiểm tra.
            self.heuristic = self.cost + abs(sum(list_boxes[i][0] + list_boxes[i][1] - self.check_points[i][0] - self.check_points[i][1] for i in range(len(list_boxes))))
        return self.heuristic
    ''' Hai hàm này nạp chồng các toán tử so sánh lớn hơn và nhỏ hơn. Chúng cho phép các trạng thái được lưu trữ trong hàng đợi ưu tiên dựa trên giá trị của hàm ước lượng '''
    def __gt__(self, other):
        if self.compute_heuristic() > other.compute_heuristic():
            return True
        else:
            return False
    def __lt__(self, other):
        if self.compute_heuristic() < other.compute_heuristic():
            return True
        else :
            return False
        
'Kiểm tra xem bảng đã đạt đến trạng thái mục tiêu hay chưa'
def KTraChienThang(board, list_check_point):
    # trả về true nếu tất cả các điểm kiểm tra được bao phủ bởi các hộp
    for p in list_check_point:
        # Kiểm tra xem tại mỗi điểm kiểm tra, có một hộp ($) trên bảng (board) hay không. Nếu không, hàm sẽ trả về False.
        if board[p[0]][p[1]] != '$':
            return False
    return True

'Sử dụng để tạo một bản sao của bảng đầu vào'
def GanMT(board):
    # Tạo một danh sách mới với cùng kích thước và giá trị như board
    return [[board[x][y] for y in range(len(board[0]))] for x in range(len(board))]

'Sử dụng để tìm vị trí hiện tại của người chơi trong một bảng.'
def TimVTriNguoiChoi(board):
    #trả lại vị trí của người chơi trong bảng
    for x in range(len(board)):
        for y in range(len(board[0])):
            # Kiểm tra xem tại vị trí (x, y) trên board, có phải là người chơi (@) hay không.
            if board[x][y] == '@':
                return (x,y)
    return (-1,-1)  # Lỗi board ( Không tìm thấy )

'Dùng để so sánh 2 ma trận với nhau'
def SoSanhMT(board_A, board_B):
    # trả về true nếu bảng A giống bảng B
    if len(board_A) != len(board_B) or len(board_A[0]) != len(board_B[0]):
        return False
    for i in range(len(board_A)):
        for j in range(len(board_A[0])):
            if board_A[i][j] != board_B[i][j]:
                return False
    return True

'Sử dụng để kiểm tra xem một bảng đã tồn tại trong danh sách các trạng thái đã duyệt qua hay chưa. '
def TTBangKhong(board, list_state):
    # trả về true nếu có cùng bảng trong danh sách
    for state in list_state:
        if SoSanhMT(state.board, board):
            return True
    return False

'kiểm tra xem hộp có ở điểm kiểm tra không ?'
def HopOCheckPoint(box, list_check_point):
    for check_point in list_check_point:
        # Kiểm tra xem tọa độ x và y của hộp (box) có bằng với tọa độ x và y của điểm kiểm tra (check_point) hay không.
        if box[0] == check_point[0] and box[1] == check_point[1]:
            return True
    return False

'Kiểm tra xem hộp có bị kẹt ở góc không ?'
def KTraGoc(board, x, y, list_check_point):
    # trả về true nếu board[x][y] ở góc
    if board[x-1][y-1] == '#':
        if board[x-1][y] == '#' and board[x][y-1] == '#':
            if not HopOCheckPoint((x,y), list_check_point):
                return True
    if board[x+1][y-1] == '#':
        if board[x+1][y] == '#' and board[x][y-1] == '#':
            if not HopOCheckPoint((x,y), list_check_point):
                return True
    if board[x-1][y+1] == '#':
        if board[x-1][y] == '#' and board[x][y+1] == '#':
            if not HopOCheckPoint((x,y), list_check_point):
                return True
    if board[x+1][y+1] == '#':
        if board[x+1][y] == '#' and board[x][y+1] == '#':
            if not HopOCheckPoint((x,y), list_check_point):
                return True
    return False

' Tìm tất cả các vị trí của hộp '
def TimVTHop(board):
    result = []
    for i in range(len(board)):
        for j in range(len(board[0])):
            if board[i][j] == '$':
                result.append((i,j))
    return result

' KIỂM TRA DUY NHẤT MỘT HỘP CÓ THỂ DI CHUYỂN ÍT NHẤT 1 HƯỚNG '
def HopDiChuyenDuocKhong(board, box_position):
    left_move = (box_position[0], box_position[1] - 1) 
    right_move = (box_position[0], box_position[1] + 1)
    up_move = (box_position[0] - 1, box_position[1])
    down_move = (box_position[0] + 1, box_position[1])
    if (board[left_move[0]][left_move[1]] == ' ' or board[left_move[0]][left_move[1]] == '%' or board[left_move[0]][left_move[1]] == '@') and board[right_move[0]][right_move[1]] != '#' and board[right_move[0]][right_move[1]] != '$':
        return True
    if (board[right_move[0]][right_move[1]] == ' ' or board[right_move[0]][right_move[1]] == '%' or board[right_move[0]][right_move[1]] == '@') and board[left_move[0]][left_move[1]] != '#' and board[left_move[0]][left_move[1]] != '$':
        return True
    if (board[up_move[0]][up_move[1]] == ' ' or board[up_move[0]][up_move[1]] == '%' or board[up_move[0]][up_move[1]] == '@') and board[down_move[0]][down_move[1]] != '#' and board[down_move[0]][down_move[1]] != '$':
        return True
    if (board[down_move[0]][down_move[1]] == ' ' or board[down_move[0]][down_move[1]] == '%' or board[down_move[0]][down_move[1]] == '@') and board[up_move[0]][up_move[1]] != '#' and board[up_move[0]][up_move[1]] != '$':
        return True
    return False

''' KIỂM TRA TẤT CẢ CÁC HỘP CÓ BỊ Kẹt không '''
def AllHopBiKet(board, list_check_point):
    box_positions = TimVTHop(board)
    result = True
    for box_position in box_positions:
        if HopOCheckPoint(box_position, list_check_point):
            return False
        if HopOCheckPoint(board, box_position):
            result = False
    return result

''' KIỂM TRA ÍT NHẤT MỘT HỘP CÓ BỊ KÍN Ở GÓC '''
def KhongTheThang(board, list_check_point):
    '''trả về true nếu hộp ở góc tường -> không thể thắng'''
    for x in range(len(board)):
        for y in range(len(board[0])):
            if board[x][y] == '$':
                if KTraGoc(board, x, y, list_check_point):
                    return True
    return False

''' Điểm tiếp theo có thể di chuyển '''
def VtriTiepTheo(board, cur_pos):
    '''trả về danh sách các vị trí mà người chơi có thể di chuyển đến từ vị trí hiện tại'''
    x,y = cur_pos[0], cur_pos[1]
    list_can_move = []
    # MOVE UP (x - 1, y)
    if 0 <= x - 1 < len(board):
        value = board[x - 1][y]
        if value == ' ' or value == '%':
            list_can_move.append((x - 1, y))
        elif value == '$' and 0 <= x - 2 < len(board):
            next_pos_box = board[x - 2][y]
            if next_pos_box != '#' and next_pos_box != '$':
                list_can_move.append((x - 1, y))
    # MOVE DOWN (x + 1, y)
    if 0 <= x + 1 < len(board):
        value = board[x + 1][y]
        if value == ' ' or value == '%':
            list_can_move.append((x + 1, y))
        elif value == '$' and 0 <= x + 2 < len(board):
            next_pos_box = board[x + 2][y]
            if next_pos_box != '#' and next_pos_box != '$':
                list_can_move.append((x + 1, y))
    # MOVE LEFT (x, y - 1)
    if 0 <= y - 1 < len(board[0]):
        value = board[x][y - 1]
        if value == ' ' or value == '%':
            list_can_move.append((x, y - 1))
        elif value == '$' and 0 <= y - 2 < len(board[0]):
            next_pos_box = board[x][y - 2]
            if next_pos_box != '#' and next_pos_box != '$':
                list_can_move.append((x, y - 1))
    # MOVE RIGHT (x, y + 1)
    if 0 <= y + 1 < len(board[0]):
        value = board[x][y + 1]
        if value == ' ' or value == '%':
            list_can_move.append((x, y + 1))
        elif value == '$' and 0 <= y + 2 < len(board[0]):
            next_pos_box = board[x][y + 2]
            if next_pos_box != '#' and next_pos_box != '$':
                list_can_move.append((x, y + 1))
    return list_can_move

''' DI CHUYỂN HỘI ĐỒNG THEO HƯỚNG ĐẶC BIỆT '''
def DiChuyen(board, next_pos, cur_pos, list_check_point):
    '''trả lại bảng mới sau khi di chuyển'''
    # LÀM board MỚI GIỐNG NHƯ board HIỆN TẠI
    new_board = GanMT(board) 
    # TÌM VỊ TRÍ TIẾP THEO NẾU CHUYỂN ĐẾN HỘP
    if new_board[next_pos[0]][next_pos[1]] == '$':
        x = 2*next_pos[0] - cur_pos[0]
        y = 2*next_pos[1] - cur_pos[1]
        new_board[x][y] = '$'
    # DI CHUYỂN NGƯỜI CHƠI ĐẾN VỊ TRÍ MỚI
    new_board[next_pos[0]][next_pos[1]] = '@'
    new_board[cur_pos[0]][cur_pos[1]] = ' '
    # KIỂM TRA NẾU TẠI VỊ TRÍ ĐIỂM CHECK KHÔNG CÓ GÌ THÌ CẬP NHẬT % THÍCH ĐIỂM KIỂM TRA
    for p in list_check_point:
        if new_board[p[0]][p[1]] == ' ':
            new_board[p[0]][p[1]] = '%'
    return new_board 

' TÌM TẤT CẢ ĐIỂM KIỂM TRA TRÊN board'
def TimListCheckPoints(board):
    '''điểm kiểm tra danh sách trở lại từ bảng
        nếu không có điểm kiểm tra nào, hãy trả về danh sách trống
        nó sẽ kiểm tra số hộp, nếu số hộp < số điểm kiểm tra
            return list [(-1,-1)]'''
            
    list_check_point = []
    num_of_box = 0
    ''' KIỂM TRA TOÀN BỘ BẢNG ĐỂ TÌM ĐIỂM VÀ SỐ HỘP'''
    for x in range(len(board)):
        for y in range(len(board[0])):
            if board[x][y] == '$':
                num_of_box += 1
            elif board[x][y] == '%':
                list_check_point.append((x,y))
    ''' KIỂM TRA NẾU SỐ HỘP < SỐ ĐIỂM KIỂM TRA'''
    if num_of_box < len(list_check_point):
        return [(-1,-1)]
    return list_check_point