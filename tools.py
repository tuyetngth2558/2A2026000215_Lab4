from __future__ import annotations

from langchain_core.tools import tool

# ============================================================
# MOCK DATA — Dữ liệu giả lập hệ thống du lịch
# ============================================================
FLIGHTS_DB = {
    ("Hà Nội", "Đà Nẵng"): [
        {"airline": "Vietnam Airlines", "departure": "06:00", "arrival": "07:20", "price": 1_450_000, "class": "economy"},
        {"airline": "Vietnam Airlines", "departure": "14:00", "arrival": "15:20", "price": 2_800_000, "class": "business"},
        {"airline": "VietJet Air", "departure": "08:30", "arrival": "09:50", "price": 890_000, "class": "economy"},
        {"airline": "Bamboo Airways", "departure": "11:00", "arrival": "12:20", "price": 1_200_000, "class": "economy"},
    ],
    ("Hà Nội", "Phú Quốc"): [
        {"airline": "Vietnam Airlines", "departure": "07:00", "arrival": "09:15", "price": 2_100_000, "class": "economy"},
        {"airline": "VietJet Air", "departure": "10:00", "arrival": "12:15", "price": 1_350_000, "class": "economy"},
        {"airline": "VietJet Air", "departure": "16:00", "arrival": "18:15", "price": 1_100_000, "class": "economy"},
    ],
    ("Hà Nội", "Hồ Chí Minh"): [
        {"airline": "Vietnam Airlines", "departure": "06:00", "arrival": "08:10", "price": 1_600_000, "class": "economy"},
        {"airline": "VietJet Air", "departure": "07:30", "arrival": "09:40", "price": 950_000, "class": "economy"},
        {"airline": "Bamboo Airways", "departure": "12:00", "arrival": "14:10", "price": 1_300_000, "class": "economy"},
        {"airline": "Vietnam Airlines", "departure": "18:00", "arrival": "20:10", "price": 3_200_000, "class": "business"},
    ],
    ("Hồ Chí Minh", "Đà Nẵng"): [
        {"airline": "Vietnam Airlines", "departure": "09:00", "arrival": "10:20", "price": 1_300_000, "class": "economy"},
        {"airline": "VietJet Air", "departure": "13:00", "arrival": "14:20", "price": 780_000, "class": "economy"},
    ],
    ("Hồ Chí Minh", "Phú Quốc"): [
        {"airline": "Vietnam Airlines", "departure": "08:00", "arrival": "09:00", "price": 1_100_000, "class": "economy"},
        {"airline": "VietJet Air", "departure": "15:00", "arrival": "16:00", "price": 650_000, "class": "economy"},
    ],
}

HOTELS_DB = {
    "Đà Nẵng": [
        {"name": "Mường Thanh Luxury", "stars": 5, "price_per_night": 1_800_000, "area": "Mỹ Khê", "rating": 4.5},
        {"name": "Sala Danang Beach", "stars": 4, "price_per_night": 1_200_000, "area": "Mỹ Khê", "rating": 4.3},
        {"name": "Fivitel Danang", "stars": 3, "price_per_night": 650_000, "area": "Sơn Trà", "rating": 4.1},
        {"name": "Memory Hostel", "stars": 2, "price_per_night": 250_000, "area": "Hải Châu", "rating": 4.6},
        {"name": "Christina's Homestay", "stars": 2, "price_per_night": 350_000, "area": "An Thượng", "rating": 4.7},
    ],
    "Phú Quốc": [
        {"name": "Vinpearl Resort", "stars": 5, "price_per_night": 3_500_000, "area": "Bãi Dài", "rating": 4.4},
        {"name": "Sol by Meliá", "stars": 4, "price_per_night": 1_500_000, "area": "Bãi Trường", "rating": 4.2},
        {"name": "Lahana Resort", "stars": 3, "price_per_night": 800_000, "area": "Dương Đông", "rating": 4.0},
        {"name": "9Station Hostel", "stars": 2, "price_per_night": 200_000, "area": "Dương Đông", "rating": 4.5},
    ],
    "Hồ Chí Minh": [
        {"name": "Rex Hotel", "stars": 5, "price_per_night": 2_800_000, "area": "Quận 1", "rating": 4.3},
        {"name": "Liberty Central", "stars": 4, "price_per_night": 1_400_000, "area": "Quận 1", "rating": 4.1},
        {"name": "Cochin Zen Hotel", "stars": 3, "price_per_night": 550_000, "area": "Quận 3", "rating": 4.4},
        {"name": "The Common Room", "stars": 2, "price_per_night": 180_000, "area": "Quận 1", "rating": 4.6},
    ],
}


def _vnd(amount: int) -> str:
    return f"{amount:,}".replace(",", ".") + "đ"


@tool
def search_flights(origin: str, destination: str) -> str:
    """Tìm kiếm các chuyến bay giữa hai thành phố."""
    try:
        key = (origin.strip(), destination.strip())
        flights = FLIGHTS_DB.get(key)
        reversed_route = False
        if not flights:
            reverse_key = (destination.strip(), origin.strip())
            flights = FLIGHTS_DB.get(reverse_key)
            reversed_route = bool(flights)

        if not flights:
            return f"Không tìm thấy chuyến bay từ {origin} đến {destination}."

        lines = []
        route_title = f"{origin} -> {destination}"
        if reversed_route:
            route_title = f"{destination} -> {origin} (không có tuyến thuận, hiển thị tuyến ngược)"
        lines.append(f"Danh sách chuyến bay ({route_title}):")
        for idx, flight in enumerate(flights, start=1):
            lines.append(
                f"{idx}. {flight['airline']} | {flight['departure']}-{flight['arrival']} | "
                f"{flight['class']} | {_vnd(int(flight['price']))}"
            )
        return "\n".join(lines)
    except Exception as exc:
        return f"Lỗi khi tìm chuyến bay: {exc}"


@tool
def search_hotels(city: str, max_price_per_night: int = 99_999_999) -> str:
    """Tìm kiếm khách sạn theo thành phố và mức giá tối đa mỗi đêm."""
    try:
        city_name = city.strip()
        hotels = HOTELS_DB.get(city_name, [])
        filtered = [h for h in hotels if int(h["price_per_night"]) <= int(max_price_per_night)]
        filtered = sorted(filtered, key=lambda x: x["rating"], reverse=True)

        if not filtered:
            return (
                f"Không tìm thấy khách sạn tại {city_name} với giá dưới {_vnd(int(max_price_per_night))}/đêm. "
                "Hãy thử tăng ngân sách."
            )

        lines = [f"Khách sạn tại {city_name} (<= {_vnd(int(max_price_per_night))}/đêm):"]
        for idx, hotel in enumerate(filtered, start=1):
            lines.append(
                f"{idx}. {hotel['name']} | {hotel['stars']} sao | {_vnd(int(hotel['price_per_night']))}/đêm | "
                f"{hotel['area']} | rating {hotel['rating']}"
            )
        return "\n".join(lines)
    except Exception as exc:
        return f"Lỗi khi tìm khách sạn: {exc}"


@tool
def calculate_budget(total_budget: int, expenses: str) -> str:
    """Tính ngân sách còn lại sau khi trừ các khoản chi phí."""
    try:
        if not isinstance(expenses, str) or not expenses.strip():
            return "Lỗi định dạng expenses. Ví dụ hợp lệ: 've_may_bay:890000,khach_san:650000'"

        expense_map: dict[str, int] = {}
        for part in expenses.split(","):
            part = part.strip()
            if not part:
                continue
            if ":" not in part:
                return f"Lỗi định dạng khoản chi '{part}'. Mỗi khoản phải có dạng ten:so_tien."
            name, amount_str = part.split(":", 1)
            name = name.strip()
            amount_str = amount_str.strip()
            if not name or not amount_str.isdigit():
                return f"Lỗi định dạng khoản chi '{part}'. Số tiền phải là số nguyên dương."
            expense_map[name] = int(amount_str)

        if not expense_map:
            return "Không có khoản chi hợp lệ để tính toán."

        total_expenses = sum(expense_map.values())
        remaining = int(total_budget) - total_expenses

        lines = ["Bảng chi phí:"]
        for key, value in expense_map.items():
            nice_name = key.replace("_", " ").strip().title()
            lines.append(f"- {nice_name}: {_vnd(value)}")
        lines.extend(
            [
                "---",
                f"Tổng chi: {_vnd(total_expenses)}",
                f"Ngân sách: {_vnd(int(total_budget))}",
                f"Còn lại: {_vnd(remaining)}",
            ]
        )

        if remaining < 0:
            lines.append(f"Cảnh báo: Vượt ngân sách {_vnd(abs(remaining))}! Cần điều chỉnh.")

        return "\n".join(lines)
    except Exception as exc:
        return f"Lỗi khi tính ngân sách: {exc}"
