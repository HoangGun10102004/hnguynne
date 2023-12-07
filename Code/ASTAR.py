import HamHoTro as HHT
import time
from queue import PriorityQueue

def AStart_Search(board, list_check_point):
    start_time = time.time()
    
    ' NẾU BÀN BẮT ĐẦU LÀ MỤC TIÊU HOẶC KHÔNG CÓ ĐIỂM KIỂM TRA'
    if HHT.KTraChienThang(board,list_check_point):
        print("Found win")
        return [board]
    
    ''' KHỞI TẠO TRẠNG THÁI BẮT ĐẦU '''
    start_state = HHT.state(board, None, list_check_point)
    list_state = [start_state]
    
    ''' KHỞI TẠO HÀNG ƯU TIÊN '''
    heuristic_queue = PriorityQueue()
    heuristic_queue.put(start_state)
    
    ''' LOẠI QUA HÀNG ƯU TIÊN '''
    while not heuristic_queue.empty():
        
        '''NHẬN now_state NGAY ĐỂ TÌM KIẾM'''
        now_state = heuristic_queue.get()
        
        ''' GET THE PLAYER'S CURRENT POSITION'''
        cur_pos = HHT.TimVTriNguoiChoi(now_state.board) 

        ''' NHẬN DANH SÁCH VỊ TRÍ NGƯỜI CHƠI CÓ THỂ DI CHUYỂN ĐẾN '''
        list_can_move = HHT.VtriTiepTheo(now_state.board, cur_pos)
        ''' TẠO TRẠNG THÁI MỚI TỪ DANH SÁCH CÓ THỂ DI CHUYỂN '''
        for next_pos in list_can_move:
            ''' Tạo BOARD MỚI '''
            new_board = HHT.DiChuyen(now_state.board, next_pos, cur_pos, list_check_point)
            
            'Nếu Board không có trong danh sách trước -> Bỏ qua State'
            if HHT.TTBangKhong(new_board, list_state):
                continue
            
            'NẾU MỘT HỘP HOẶC NHIỀU HỘP BỊ KÍN Ở GÓC --> BỎ QUA TRẠNG THÁI'
            if HHT.KhongTheThang(new_board, list_check_point):
                continue
            
            'NẾU TẤT CẢ CÁC HỘP BỊ KÍN --> BỎ QUA STATE'
            if HHT.AllHopBiKet(new_board, list_check_point):
                continue

            'TẠO TRẠNG THÁI MỚI'
            new_state = HHT.state(new_board, now_state, list_check_point)
            'KIỂM TRA TRẠNG THÁI MỚI CÓ LÀ MỤC TIÊU HAY KHÔNG'
            if HHT.KTraChienThang(new_board, list_check_point):
                print("Found win")
                return (new_state.get_line(), len(list_state))
            
            'GỬI TRẠNG THÁI MỚI VÀO DANH SÁCH ĐÃ TRUY CẬP VÀ DANH SÁCH ĐÃ QUA'
            list_state.append(new_state)
            heuristic_queue.put(new_state)

            'TÍNH THỜI GIAN CHỜ'
            end_time = time.time()
            if end_time - start_time > HHT.HETTGIAN:
                return []
        end_time = time.time()
        if end_time - start_time > HHT.HETTGIAN:
            return []
    'KHÔNG TÌM GIẢI PHÁP'
    print("Not Found")
    return []