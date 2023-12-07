import HamHoTro as HHT
import time

def BFS_search(board, list_check_point):
    start_time = time.time()
    
    'NẾU BÀN BẮT ĐẦU LÀ MỤC TIÊU HOẶC KHÔNG CÓ ĐIỂM KIỂM TRA'
    if HHT.KTraChienThang(board,list_check_point):
        print("Found win")
        return [board]
    
    'Tiến hành khởi tạo trạng thái bắt đầu'
    Start_State = HHT.state(board, None, list_check_point)
    'Tiến hành khởi tạo 2 danh sách dùng cho BFS'
    List_State = [Start_State]
    List_Visit = [Start_State]
    
    'Tiến hành lặp qua danh sách đã truy cập'
    while len(List_Visit) != 0:
        # Nhận Now_State ngay để tìm kiếm 
        Now_State = List_Visit.pop(0)
        # Nhận vị trí hiện tại của người chơi
        Cur_Pos = HHT.TimVTriNguoiChoi(Now_State.board)
        
        'Tiến hành nhận danh sách vị trí người chơi có thể di chuyển đến'
        DSachCTDiChuyen = HHT.VtriTiepTheo(Now_State.board, Cur_Pos) # Danh sách có thể di chuyển
        
        'Tạo một trạng thái mới từ danh sách có thể di chuyển'
        for next_pos in DSachCTDiChuyen:
            'Tạo Board mới'
            new_board = HHT.DiChuyen(Now_State.board, next_pos, Cur_Pos, list_check_point)
            
            'Nếu Board không có trong danh sách trước -> Bỏ qua State'
            if HHT.TTBangKhong(new_board, List_State):
                continue
            
            'NẾU MỘT HỘP HOẶC NHIỀU HỘP BỊ KÍN Ở GÓC --> BỎ QUA TRẠNG THÁI'
            if HHT.KhongTheThang(new_board, list_check_point):
                continue
            
            'NẾU TẤT CẢ CÁC HỘP BỊ KÍN --> BỎ QUA STATE'
            if HHT.AllHopBiKet(new_board, list_check_point):
                continue
            
            'TẠO TRẠNG THÁI MỚI'
            new_state = HHT.state(new_board, Now_State, list_check_point)
            'KIỂM TRA TRẠNG THÁI MỚI CÓ LÀ MỤC TIÊU HAY KHÔNG'
            if HHT.KTraChienThang(new_board, list_check_point):
                print("Found win")
                return (new_state.get_line(), len(List_State))
            
            'GỬI TRẠNG THÁI MỚI VÀO DANH SÁCH ĐÃ TRUY CẬP VÀ DANH SÁCH ĐÃ QUA'
            List_State.append(new_state)
            List_Visit.append(new_state)
            
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
        
            
        