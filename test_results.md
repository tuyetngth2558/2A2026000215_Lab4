# Lab 4 - Test Results 


## Test 1 - Direct Answer 
**User:** Xin chào! Tôi đang muốn đi du lịch nhưng chưa biết đi đâu.  
**Expected:** Không gọi tool, hỏi thêm sở thích/ngân sách/thời gian.

**Console log:**
```text
Bạn: Xin chào! Tôi đang muốn đi du lịch nhưng chưa biết đi đâu.

TravelBuddy đang suy nghĩ...
Trả lời trực tiếp

TravelBuddy: Chào bạn! Mình rất sẵn sàng giúp lên kế hoạch du lịch.
Bạn cho mình biết thêm 3 thông tin nhé: (1) Bạn thích biển/núi/thành phố? (2) Ngân sách dự kiến bao nhiêu? (3) Bạn đi mấy ngày?
```

## Test 2 - Single Tool Call
**User:** Tìm giúp tôi chuyến bay từ Hà Nội đi Đà Nẵng  
**Expected:** Gọi `search_flights("Hà Nội","Đà Nẵng")`.

**Console log:**
```text
Bạn: Tìm giúp tôi chuyến bay từ Hà Nội đi Đà Nẵng

TravelBuddy đang suy nghĩ...
Gọi tool: search_flights({'origin': 'Hà Nội', 'destination': 'Đà Nẵng'})
Trả lời trực tiếp

TravelBuddy: Mình đã tìm được 4 chuyến bay từ Hà Nội đi Đà Nẵng
1.Vietnam Airlines | 06:00-07:20 | economy | 1.450.000đ
2.Vietnam Airlines | 14:00-15:20 | business | 2.800.000đ
3.VietJet Air | 08:30-09:50 | economy | 890.000đ
4.Bamboo Airways | 11:00-12:20 | economy | 1.200.000đ
```

## Test 3 - Multi-Step Tool Chaining
**User:** Tôi ở Hà Nội, muốn đi Phú Quốc 2 đêm, budget 5 triệu. Tư vấn giúp!  
**Expected:** Chuỗi nhiều bước: bay -> khách sạn -> budget.

**Console log:**
```text
Bạn: Tôi ở Hà Nội, muốn đi Phú Quốc 2 đêm, budget 5 triệu. Tư vấn giúp!

TravelBuddy đang suy nghĩ...
Gọi tool: search_flights({'origin': 'Hà Nội', 'destination': 'Phú Quốc'})
Gọi tool: search_hotels({'city': 'Phú Quốc', 'max_price_per_night': 1950000})
Gọi tool: calculate_budget({'total_budget': 5000000, 'expenses': 've_bay:1100000,khach_san:400000'})
Trả lời trực tiếp

TravelBuddy: Chuyến bay: VietJet Air 16:00-18:15, 1.100.000đ
Khách sạn: 9Station Hostel, 200.000đ/đêm (2 đêm = 400.000đ)
Tổng chi phí ước tính: 1.500.000đ
Còn lại trong ngân sách: 3.500.000đ
Gợi ý thêm: Bạn có thể nâng hạng phòng hoặc dành ngân sách cho ăn uống/vui chơi.
```

## Test 4 - Missing Info / Clarification

Mở rộng: Agent phải **hỏi làm rõ** khi thiếu dữ liệu, **không gọi tool** cho đến khi đủ thông tin.

### Test 4a — Đặt khách sạn (thiếu toàn bộ chi tiết)
**User:** Tôi muốn đặt khách sạn  
**Expected:** Hỏi thành phố, số đêm, ngân sách/đêm; chưa gọi tool.

**Console log:**
```text
Bạn: Tôi muốn đặt khách sạn

TravelBuddy đang suy nghĩ...
Trả lời trực tiếp

TravelBuddy: Mình hỗ trợ ngay nhé. Bạn cho mình xin thêm thành phố, số đêm lưu trú và ngân sách tối đa mỗi đêm để mình lọc khách sạn phù hợp.
```

### Test 4b — Có thành phố nhưng thiếu số đêm và ngân sách
**User:** Tôi muốn book phòng ở Đà Nẵng  
**Expected:** Hỏi số đêm và mức giá tối đa mỗi đêm (hoặc tổng budget); chưa gọi `search_hotels`.

**Console log:**
```text
Bạn: Tôi muốn book phòng ở Đà Nẵng

TravelBuddy đang suy nghĩ...
Trả lời trực tiếp

TravelBuddy: Bạn định ở Đà Nẵng mấy đêm và ngân sách tối đa mỗi đêm (hoặc tổng budget cho chỗ ở) là bao nhiêu? Mình cần hai thông tin này để gợi ý khách sạn phù hợp.
```

### Test 4c — Muốn tìm vé nhưng không nói điểm đi / điểm đến
**User:** Tìm giúp tôi vé máy bay rẻ nhất  
**Expected:** Hỏi điểm khởi hành, điểm đến, (tuỳ chọn) ngày bay; chưa gọi `search_flights`.

**Console log:**
```text
Bạn: Tìm giúp tôi vé máy bay rẻ nhất

TravelBuddy đang suy nghĩ...
Trả lời trực tiếp

TravelBuddy: Bạn bay từ thành phố nào và đến đâu? Nếu có ngày đi cụ thể thì cho mình biết thêm để mình tra chuyến phù hợp.
```

### Test 4d — Ngân sách chung nhưng chưa rõ điểm đến / số ngày
**User:** Tôi có 3 triệu muốn đi chơi biển  
**Expected:** Hỏi khởi hành từ đâu, điểm đến ưu tiên, số ngày; chưa gọi tool.

**Console log:**
```text
Bạn: Tôi có 3 triệu muốn đi chơi biển

TravelBuddy đang suy nghĩ...
Trả lời trực tiếp

TravelBuddy: Ngân sách 3 triệu nghe ổn để lên phương án. Bạn xuất phát từ đây (Hà Nội / TP.HCM / …), muốn đi biển ở đâu (ví dụ Đà Nẵng, Phú Quốc), và đi mấy ngày mấy đêm? Mình cần thông tin này mới tư vấn vé và chỗ ở cụ thể.
```

## Test 5 - Guardrail / Refusal
**User:** Giải giúp tôi bài tập lập trình Python về linked list  
**Expected:** Từ chối lịch sự vì ngoài phạm vi.

**Console log:**
```text
Bạn: Giải giúp tôi bài tập lập trình Python về linked list

TravelBuddy đang suy nghĩ...
Trả lời trực tiếp

TravelBuddy: Xin lỗi bạn, mình chỉ hỗ trợ các yêu cầu liên quan du lịch (vé máy bay, khách sạn, lịch trình, ngân sách chuyến đi).
Nếu bạn cần, mình có thể tư vấn một chuyến đi theo ngân sách ngay bây giờ.
```
