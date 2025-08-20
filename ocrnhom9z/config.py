# config.py - Cấu hình hệ thống

# Gemini API Configuration
GEMINI_MODEL = "gemini-1.5-flash"
MAX_TOKENS = 4000
TIMEOUT = 120
GEMINI_RATE_LIMIT = 15  # requests per minute

# Application Settings
APP_TITLE = "📊 Trích Xuất Bảng Điểm Sinh Viên"
APP_SIZE = "1500x1000"
APP_BG_COLOR = "#f0f0f0"

# File Settings
SUPPORTED_IMAGE_FORMATS = [
    ("Image files", "*.png *.jpg *.jpeg *.bmp *.tiff"),
    ("All files", "*.*")
]

# OCR Settings
OCR_LANGUAGES = "vie+eng"
OCR_CONFIG_STANDARD = "--oem 3 --psm 6"
OCR_CONFIG_HANDWRITING = "--oem 3 --psm 4"

# Data Validation Settings
MIN_MSV_LENGTH = 8
MAX_MSV_LENGTH = 10
VALID_MSV_PREFIXES = ['15', '17', '18', '19', '20', '21', '22', '23', '24']
VALID_SCORE_RANGE = (0.0, 10.0)

# Excel Export Settings
EXCEL_SHEET_NAME_PREFIX = "BangDiem"
EXCEL_HEADERS = ["STT", "Lớp", "MSV", "Họ và đệm", "Tên", "CC", "KT1", "KT2", "KDT"]

# Vietnamese Names Database - Comprehensive List
VIETNAMESE_NAMES_DATABASE = {
    "surnames": [
        # Top 20 họ phổ biến nhất Việt Nam
        "Nguyễn", "Trần", "Lê", "Phạm", "Hoàng", "Huỳnh", "Phan", "Vũ", "Võ", "Đặng",
        "Bùi", "Đỗ", "Hồ", "Ngô", "Dương", "Lý", "Đào", "Lương", "Vương", "Trương",
        # Các họ khác
        "Mai", "Đinh", "Tô", "Cao", "Tạ", "Hà", "Chu", "Triệu", "Lưu", "Thái",
        "Tăng", "Đoàn", "Kiều", "Ông", "Thạch", "Hứa", "Quách", "Tôn", "Lâm", "Khương",
        "Từ", "Ưng", "Âu", "Ấu", "Bạch", "Bành", "Bành", "Cung", "Diệp", "Doãn",
        "Giang", "Hạ", "Hàn", "Hầu", "Hồng", "Khổng", "La", "Lạc", "Lại", "Lộc",
        "Long", "Lục", "Mạc", "Mạnh", "Nghiêm", "Ninh", "Ôn", "Phó", "Phùng", "Quang",
        "Quyền", "Sầm", "Sử", "Thi", "Thôn", "Thủy", "Tiêu", "Tín", "Tòng", "Trịnh",
        "Trưng", "Tuyền", "Ung", "Ứng", "Văn", "Viên", "Xa", "Yên"
    ],

    "middle_names": [
        # Tên đệm nam
        "Văn", "Đức", "Minh", "Quang", "Hữu", "Thành", "Công", "Duy", "Xuân", "Thanh",
        "Tuấn", "Hoàng", "Bảo", "Ngọc", "Phúc", "Tấn", "Trung", "Khắc", "Đình", "Quốc",
        "Hồng", "Việt", "Tiến", "Thái", "Mạnh", "Sơn", "Hải", "Lâm", "Phong", "Cường",
        # Tên đệm nữ
        "Thị", "Ngọc", "Hồng", "Thu", "Lan", "Hương", "Mai", "Linh", "Phương", "Trang",
        "Thanh", "Kim", "Bích", "Diệu", "Thúy", "Xuân", "Hạnh", "Yến", "Như", "Thảo",
        "Minh", "Ánh", "Cẩm", "Kiều", "Mỹ", "Gia", "Khánh", "Quỳnh", "Tuyết", "Vân"
    ],

    "first_names": {
        "male": [
            # Tên nam phổ biến
            "Anh", "An", "Bình", "Cường", "Dũng", "Đạt", "Đức", "Giang", "Hải", "Hùng",
            "Khang", "Kiên", "Lâm", "Long", "Minh", "Nam", "Phong", "Quang", "Sơn", "Thành",
            "Tiến", "Tuấn", "Việt", "Vinh", "Vũ", "Bảo", "Đông", "Hưng", "Khánh", "Linh",
            "Mạnh", "Nghĩa", "Phúc", "Quốc", "Tài", "Thắng", "Thịnh", "Trung", "Tùng", "Vương",
            "Hoàng", "Huy", "Khôi", "Lộc", "Nhân", "Phát", "Quân", "Tâm", "Thế", "Trí",
            "Tú", "Tường", "Uy", "Vĩnh", "Xuân", "Yên", "Bách", "Cao", "Duy", "Gia",
            "Hiếu", "Khải", "Lợi", "Ngân", "Phương", "Quyết", "Tân", "Thông", "Trường", "Vạn"
        ],

        "female": [
            # Tên nữ phổ biến
            "Anh", "Bình", "Chi", "Dung", "Giang", "Hà", "Hương", "Lan", "Linh", "Mai",
            "Nga", "Oanh", "Phương", "Quỳnh", "Thảo", "Trang", "Uyên", "Vân", "Yến", "Bảo",
            "Diệu", "Hạnh", "Khánh", "Ly", "Ngọc", "Phúc", "Thúy", "Tuyết", "Vũ", "Xuân",
            "Ánh", "Cẩm", "Hồng", "Kiều", "Mỹ", "Như", "Quyên", "Thu", "Tâm", "Vy",
            "An", "Châu", "Hoa", "Lam", "Nhi", "Phụng", "Thư", "Trinh", "Uyển", "Yên",
            "Bích", "Duyên", "Hiền", "Loan", "Oanh", "Quế", "Thùy", "Trúc", "Vương", "Yến",
            "Cúc", "Hằng", "Liên", "Pha", "Sương", "Tú", "Vàng", "Yến", "Đào", "Huyền"
        ],

        "unisex": [
            # Tên có thể dùng cho cả nam và nữ
            "An", "Bình", "Giang", "Hạnh", "Khánh", "Linh", "Minh", "Phương", "Quang", "Tâm",
            "Thanh", "Thảo", "Trang", "Trúc", "Uyên", "Vân", "Xuân", "Yến", "Bảo", "Hải",
            "Hương", "Kim", "Lâm", "Ngọc", "Phúc", "Quỳnh", "Thành", "Thu", "Tú", "Vũ"
        ]
    }
}

# Danh sách tổng hợp để tương thích ngược
COMMON_VIETNAMESE_SURNAMES = VIETNAMESE_NAMES_DATABASE["surnames"][:20]  # Top 20 họ
COMMON_VIETNAMESE_NAMES = (
    VIETNAMESE_NAMES_DATABASE["first_names"]["male"][:15] +
    VIETNAMESE_NAMES_DATABASE["first_names"]["female"][:15]
)[:20]  # Top 20 tên

# OCR Error Corrections
OCR_NUMBER_CORRECTIONS = {
    'O': '0', 'o': '0',
    'I': '1', 'l': '1', '|': '1',
    'S': '5', 's': '5',
    'G': '6', 'g': '6',
    'T': '7', 't': '7',
    'B': '8', 'b': '8',
    'g': '9', 'q': '9',
}

# Comprehensive OCR Name Corrections Database
OCR_NAME_CORRECTIONS = {
    # Họ phổ biến - sửa lỗi thiếu dấu
    'Nguyen': 'Nguyễn', 'nguyen': 'Nguyễn', 'NGUYEN': 'Nguyễn',
    'Tran': 'Trần', 'tran': 'Trần', 'TRAN': 'Trần',
    'Le': 'Lê', 'le': 'Lê', 'LE': 'Lê',
    'Pham': 'Phạm', 'pham': 'Phạm', 'PHAM': 'Phạm',
    'Hoang': 'Hoàng', 'hoang': 'Hoàng', 'HOANG': 'Hoàng',
    'Huynh': 'Huỳnh', 'huynh': 'Huỳnh', 'HUYNH': 'Huỳnh',
    'Bui': 'Bùi', 'bui': 'Bùi', 'BUI': 'Bùi',
    'Do': 'Đỗ', 'do': 'Đỗ', 'DO': 'Đỗ',
    'Dao': 'Đào', 'dao': 'Đào', 'DAO': 'Đào',
    'Duong': 'Dương', 'duong': 'Dương', 'DUONG': 'Dương',
    'Lam': 'Lâm', 'lam': 'Lâm', 'LAM': 'Lâm',
    'Luong': 'Lương', 'luong': 'Lương', 'LUONG': 'Lương',
    'Dang': 'Đặng', 'dang': 'Đặng', 'DANG': 'Đặng',
    'Vo': 'Võ', 'vo': 'Võ', 'VO': 'Võ',
    'Vu': 'Vũ', 'vu': 'Vũ', 'VU': 'Vũ',
    'Ho': 'Hồ', 'ho': 'Hồ', 'HO': 'Hồ',
    'Ngo': 'Ngô', 'ngo': 'Ngô', 'NGO': 'Ngô',
    'Ly': 'Lý', 'ly': 'Lý', 'LY': 'Lý',
    'Truong': 'Trương', 'truong': 'Trương', 'TRUONG': 'Trương',
    'Vuong': 'Vương', 'vuong': 'Vương', 'VUONG': 'Vương',

    # Tên đệm phổ biến
    'Van': 'Văn', 'van': 'Văn', 'VAN': 'Văn',
    'Duc': 'Đức', 'duc': 'Đức', 'DUC': 'Đức',
    'Thi': 'Thị', 'thi': 'Thị', 'THI': 'Thị',
    'Ngoc': 'Ngọc', 'ngoc': 'Ngọc', 'NGOC': 'Ngọc',
    'Hong': 'Hồng', 'hong': 'Hồng', 'HONG': 'Hồng',
    'Thanh': 'Thanh', 'thanh': 'Thanh', 'THANH': 'Thanh',
    'Quang': 'Quang', 'quang': 'Quang', 'QUANG': 'Quang',
    'Huu': 'Hữu', 'huu': 'Hữu', 'HUU': 'Hữu',
    'Cong': 'Công', 'cong': 'Công', 'CONG': 'Công',
    'Thanh': 'Thành', 'thanh': 'Thành', 'THANH': 'Thành',

    # Tên riêng phổ biến
    'Anh': 'Anh', 'anh': 'Anh', 'ANH': 'Anh',
    'Dat': 'Đạt', 'dat': 'Đạt', 'DAT': 'Đạt',
    'Dung': 'Dũng', 'dung': 'Dũng', 'DUNG': 'Dũng',
    'Dong': 'Đông', 'dong': 'Đông', 'DONG': 'Đông',
    'Cuong': 'Cường', 'cuong': 'Cường', 'CUONG': 'Cường',
    'Hung': 'Hùng', 'hung': 'Hùng', 'HUNG': 'Hùng',
    'Manh': 'Mạnh', 'manh': 'Mạnh', 'MANH': 'Mạnh',
    'Quoc': 'Quốc', 'quoc': 'Quốc', 'QUOC': 'Quốc',
    'Tien': 'Tiến', 'tien': 'Tiến', 'TIEN': 'Tiến',
    'Tuan': 'Tuấn', 'tuan': 'Tuấn', 'TUAN': 'Tuấn',
    'Vinh': 'Vinh', 'vinh': 'Vinh', 'VINH': 'Vinh',
    'Bao': 'Bảo', 'bao': 'Bảo', 'BAO': 'Bảo',
    'Khanh': 'Khánh', 'khanh': 'Khánh', 'KHANH': 'Khánh',
    'Linh': 'Linh', 'linh': 'Linh', 'LINH': 'Linh',
    'Phuong': 'Phương', 'phuong': 'Phương', 'PHUONG': 'Phương',
    'Thao': 'Thảo', 'thao': 'Thảo', 'THAO': 'Thảo',
    'Huong': 'Hương', 'huong': 'Hương', 'HUONG': 'Hương',
    'Quynh': 'Quỳnh', 'quynh': 'Quỳnh', 'QUYNH': 'Quỳnh',
    'Yen': 'Yến', 'yen': 'Yến', 'YEN': 'Yến',
    'Thuy': 'Thúy', 'thuy': 'Thúy', 'THUY': 'Thúy',
    'Tuyet': 'Tuyết', 'tuyet': 'Tuyết', 'TUYET': 'Tuyết',

    # Các trường hợp thiếu dấu phổ biến - Họ
    'Dang': 'Đặng', 'dang': 'Đặng', 'DANG': 'Đặng',
    'Dinh': 'Đinh', 'dinh': 'Đinh', 'DINH': 'Đinh',
    'Dong': 'Đông', 'dong': 'Đông', 'DONG': 'Đông',
    'Doan': 'Đoàn', 'doan': 'Đoàn', 'DOAN': 'Đoàn',
    'Kieu': 'Kiều', 'kieu': 'Kiều', 'KIEU': 'Kiều',
    'Luu': 'Lưu', 'luu': 'Lưu', 'LUU': 'Lưu',
    'Thai': 'Thái', 'thai': 'Thái', 'THAI': 'Thái',
    'Tang': 'Tăng', 'tang': 'Tăng', 'TANG': 'Tăng',
    'Thach': 'Thạch', 'thach': 'Thạch', 'THACH': 'Thạch',
    'Hua': 'Hứa', 'hua': 'Hứa', 'HUA': 'Hứa',
    'Quach': 'Quách', 'quach': 'Quách', 'QUACH': 'Quách',
    'Ton': 'Tôn', 'ton': 'Tôn', 'TON': 'Tôn',
    'Khuong': 'Khương', 'khuong': 'Khương', 'KHUONG': 'Khương',
    'Tu': 'Từ', 'tu': 'Từ', 'TU': 'Từ',
    'Ung': 'Ưng', 'ung': 'Ưng', 'UNG': 'Ưng',
    'Au': 'Âu', 'au': 'Âu', 'AU': 'Âu',
    'Bach': 'Bạch', 'bach': 'Bạch', 'BACH': 'Bạch',
    'Banh': 'Bành', 'banh': 'Bành', 'BANH': 'Bành',
    'Cung': 'Cung', 'cung': 'Cung', 'CUNG': 'Cung',
    'Diep': 'Diệp', 'diep': 'Diệp', 'DIEP': 'Diệp',
    'Doan': 'Doãn', 'doan': 'Doãn', 'DOAN': 'Doãn',

    # Các trường hợp thiếu dấu - Tên đệm
    'Minh': 'Minh', 'minh': 'Minh', 'MINH': 'Minh',
    'Huu': 'Hữu', 'huu': 'Hữu', 'HUU': 'Hữu',
    'Cong': 'Công', 'cong': 'Công', 'CONG': 'Công',
    'Thanh': 'Thành', 'thanh': 'Thành', 'THANH': 'Thành',
    'Tuan': 'Tuấn', 'tuan': 'Tuấn', 'TUAN': 'Tuấn',
    'Khac': 'Khắc', 'khac': 'Khắc', 'KHAC': 'Khắc',
    'Dinh': 'Đình', 'dinh': 'Đình', 'DINH': 'Đình',
    'Tan': 'Tấn', 'tan': 'Tấn', 'TAN': 'Tấn',
    'Bich': 'Bích', 'bich': 'Bích', 'BICH': 'Bích',
    'Dieu': 'Diệu', 'dieu': 'Diệu', 'DIEU': 'Diệu',
    'Cam': 'Cẩm', 'cam': 'Cẩm', 'CAM': 'Cẩm',
    'My': 'Mỹ', 'my': 'Mỹ', 'MY': 'Mỹ',
    'Gia': 'Gia', 'gia': 'Gia', 'GIA': 'Gia',
    'Nhu': 'Như', 'nhu': 'Như', 'NHU': 'Như',

    # Các trường hợp thiếu dấu - Tên riêng
    'Binh': 'Bình', 'binh': 'Bình', 'BINH': 'Bình',
    'Duc': 'Đức', 'duc': 'Đức', 'DUC': 'Đức',
    'Hung': 'Hùng', 'hung': 'Hùng', 'HUNG': 'Hùng',
    'Khang': 'Khang', 'khang': 'Khang', 'KHANG': 'Khang',
    'Kien': 'Kiên', 'kien': 'Kiên', 'KIEN': 'Kiên',
    'Long': 'Long', 'long': 'Long', 'LONG': 'Long',
    'Phong': 'Phong', 'phong': 'Phong', 'PHONG': 'Phong',
    'Son': 'Sơn', 'son': 'Sơn', 'SON': 'Sơn',
    'Thang': 'Thắng', 'thang': 'Thắng', 'THANG': 'Thắng',
    'Thinh': 'Thịnh', 'thinh': 'Thịnh', 'THINH': 'Thịnh',
    'Tung': 'Tùng', 'tung': 'Tùng', 'TUNG': 'Tùng',
    'Vinh': 'Vĩnh', 'vinh': 'Vĩnh', 'VINH': 'Vĩnh',
    'Xuan': 'Xuân', 'xuan': 'Xuân', 'XUAN': 'Xuân',
    'Bach': 'Bách', 'bach': 'Bách', 'BACH': 'Bách',
    'Cao': 'Cao', 'cao': 'Cao', 'CAO': 'Cao',
    'Hieu': 'Hiếu', 'hieu': 'Hiếu', 'HIEU': 'Hiếu',
    'Khai': 'Khải', 'khai': 'Khải', 'KHAI': 'Khải',
    'Loi': 'Lợi', 'loi': 'Lợi', 'LOI': 'Lợi',
    'Ngan': 'Ngân', 'ngan': 'Ngân', 'NGAN': 'Ngân',
    'Quyet': 'Quyết', 'quyet': 'Quyết', 'QUYET': 'Quyết',
    'Tan': 'Tân', 'tan': 'Tân', 'TAN': 'Tân',
    'Thong': 'Thông', 'thong': 'Thông', 'THONG': 'Thông',
    'Truong': 'Trường', 'truong': 'Trường', 'TRUONG': 'Trường',
    'Van': 'Vạn', 'van': 'Vạn', 'VAN': 'Vạn',

    # Tên nữ thiếu dấu
    'Chi': 'Chi', 'chi': 'Chi', 'CHI': 'Chi',
    'Dung': 'Dung', 'dung': 'Dung', 'DUNG': 'Dung',
    'Ha': 'Hà', 'ha': 'Hà', 'HA': 'Hà',
    'Lan': 'Lan', 'lan': 'Lan', 'LAN': 'Lan',
    'Mai': 'Mai', 'mai': 'Mai', 'MAI': 'Mai',
    'Nga': 'Nga', 'nga': 'Nga', 'NGA': 'Nga',
    'Oanh': 'Oanh', 'oanh': 'Oanh', 'OANH': 'Oanh',
    'Uyen': 'Uyên', 'uyen': 'Uyên', 'UYEN': 'Uyên',
    'Van': 'Vân', 'van': 'Vân', 'VAN': 'Vân',
    'Anh': 'Ánh', 'anh': 'Ánh', 'ANH': 'Ánh',
    'Chau': 'Châu', 'chau': 'Châu', 'CHAU': 'Châu',
    'Hoa': 'Hoa', 'hoa': 'Hoa', 'HOA': 'Hoa',
    'Lam': 'Lam', 'lam': 'Lam', 'LAM': 'Lam',
    'Nhi': 'Nhi', 'nhi': 'Nhi', 'NHI': 'Nhi',
    'Phung': 'Phụng', 'phung': 'Phụng', 'PHUNG': 'Phụng',
    'Thu': 'Thư', 'thu': 'Thư', 'THU': 'Thư',
    'Trinh': 'Trinh', 'trinh': 'Trinh', 'TRINH': 'Trinh',
    'Uyen': 'Uyển', 'uyen': 'Uyển', 'UYEN': 'Uyển',
    'Cuc': 'Cúc', 'cuc': 'Cúc', 'CUC': 'Cúc',
    'Hang': 'Hằng', 'hang': 'Hằng', 'HANG': 'Hằng',
    'Lien': 'Liên', 'lien': 'Liên', 'LIEN': 'Liên',
    'Pha': 'Pha', 'pha': 'Pha', 'PHA': 'Pha',
    'Suong': 'Sương', 'suong': 'Sương', 'SUONG': 'Sương',
    'Tu': 'Tú', 'tu': 'Tú', 'TU': 'Tú',
    'Vang': 'Vàng', 'vang': 'Vàng', 'VANG': 'Vàng',
    'Dao': 'Đào', 'dao': 'Đào', 'DAO': 'Đào',
    'Huyen': 'Huyền', 'huyen': 'Huyền', 'HUYEN': 'Huyền',

    # Các trường hợp đặc biệt với dấu thanh
    'An': 'An', 'an': 'An', 'AN': 'An',  # Có thể là Ân, Ấn
    'Am': 'Âm', 'am': 'Âm', 'AM': 'Âm',
    'Au': 'Âu', 'au': 'Âu', 'AU': 'Âu',
    'Ay': 'Ấy', 'ay': 'Ấy', 'AY': 'Ấy',
    'Em': 'Em', 'em': 'Em', 'EM': 'Em',
    'En': 'Ên', 'en': 'Ên', 'EN': 'Ên',
    'Eo': 'Eo', 'eo': 'Eo', 'EO': 'Eo',
    'Ep': 'Ép', 'ep': 'Ép', 'EP': 'Ép',
    'Et': 'Ết', 'et': 'Ết', 'ET': 'Ết',
    'Ich': 'Ích', 'ich': 'Ích', 'ICH': 'Ích',
    'Im': 'Im', 'im': 'Im', 'IM': 'Im',
    'In': 'In', 'in': 'In', 'IN': 'In',
    'It': 'Ít', 'it': 'Ít', 'IT': 'Ít',
    'Oc': 'Óc', 'oc': 'Óc', 'OC': 'Óc',
    'Om': 'Ôm', 'om': 'Ôm', 'OM': 'Ôm',
    'On': 'Ôn', 'on': 'Ôn', 'ON': 'Ôn',
    'Ong': 'Ông', 'ong': 'Ông', 'ONG': 'Ông',
    'Op': 'Óp', 'op': 'Óp', 'OP': 'Óp',
    'Ot': 'Ót', 'ot': 'Ót', 'OT': 'Ót',
    'Uc': 'Úc', 'uc': 'Úc', 'UC': 'Úc',
    'Um': 'Ùm', 'um': 'Ùm', 'UM': 'Ùm',
    'Un': 'Ún', 'un': 'Ún', 'UN': 'Ún',
    'Ung': 'Ưng', 'ung': 'Ưng', 'UNG': 'Ưng',
    'Up': 'Úp', 'up': 'Úp', 'UP': 'Úp',
    'Ut': 'Út', 'ut': 'Út', 'UT': 'Út',

    # Tên có dấu sắc, huyền, hỏi, ngã, nặng
    'Anh': 'Ánh', 'anh': 'ánh',  # Có thể là Ánh (nữ) hoặc Anh (nam)
    'Duc': 'Đức', 'duc': 'đức',
    'Hung': 'Hùng', 'hung': 'hùng',  # Có thể là Hùng, Hưng, Hững
    'Huy': 'Huy', 'huy': 'huy',  # Có thể là Huy, Hùy, Hủy, Hũy, Hụy
    'Khoi': 'Khôi', 'khoi': 'khôi',
    'Loc': 'Lộc', 'loc': 'lộc',
    'Nhan': 'Nhân', 'nhan': 'nhân',
    'Phat': 'Phát', 'phat': 'phát',
    'Quan': 'Quân', 'quan': 'quân',
    'Tam': 'Tâm', 'tam': 'tâm',
    'The': 'Thế', 'the': 'thế',
    'Tri': 'Trí', 'tri': 'trí',
    'Tuong': 'Tường', 'tuong': 'tường',
    'Uy': 'Uy', 'uy': 'uy',
    'Vinh': 'Vĩnh', 'vinh': 'vĩnh',

    # Tên nữ thiếu dấu phổ biến
    'Chau': 'Châu', 'chau': 'châu',
    'Dieu': 'Diệu', 'dieu': 'diệu',
    'Hanh': 'Hạnh', 'hanh': 'hạnh',
    'Hien': 'Hiền', 'hien': 'hiền',
    'Loan': 'Loan', 'loan': 'loan',
    'Que': 'Quế', 'que': 'quế',
    'Thuy': 'Thùy', 'thuy': 'thùy',  # Có thể là Thùy, Thúy, Thủy
    'Truc': 'Trúc', 'truc': 'trúc',
    'Uyen': 'Uyển', 'uyen': 'uyển',
    'Hang': 'Hằng', 'hang': 'hằng',
    'Lien': 'Liên', 'lien': 'liên',
    'Suong': 'Sương', 'suong': 'sương',
    'Vang': 'Vàng', 'vang': 'vàng',
    'Huyen': 'Huyền', 'huyen': 'huyền',

    # Lỗi OCR với ký tự đặc biệt
    'Đ': 'Đ', 'd': 'đ', 'D': 'Đ',  # Đ bị nhầm thành D
    'ă': 'ă', 'a': 'ă', 'A': 'Ă',  # ă bị nhầm thành a
    'â': 'â', 'a': 'â', 'A': 'Â',  # â bị nhầm thành a
    'ê': 'ê', 'e': 'ê', 'E': 'Ê',  # ê bị nhầm thành e
    'ô': 'ô', 'o': 'ô', 'O': 'Ô',  # ô bị nhầm thành o
    'ơ': 'ơ', 'o': 'ơ', 'O': 'Ơ',  # ơ bị nhầm thành o
    'ư': 'ư', 'u': 'ư', 'U': 'Ư',  # ư bị nhầm thành u
}

OCR_CLASS_CORRECTIONS = {
    'CNIT': 'CNTT', 'CNTI': 'CNTT', 'CNT': 'CNTT', 'CNTF': 'CNTT',
    'CNFF': 'CNTT', 'CNNT': 'CNTT', 'CITT': 'CNTT'
}

# Default Values
DEFAULT_CLASS = "CNTT 17-02"
DEFAULT_SCORE = "0.0"
DEFAULT_SURNAME = "Nguyễn"
DEFAULT_NAME = "Anh"

# Utility Functions for Vietnamese Names
def get_all_surnames():
    """Lấy tất cả họ trong database"""
    return VIETNAMESE_NAMES_DATABASE["surnames"]

def get_all_middle_names():
    """Lấy tất cả tên đệm trong database"""
    return VIETNAMESE_NAMES_DATABASE["middle_names"]

def get_all_first_names():
    """Lấy tất cả tên riêng trong database"""
    all_names = []
    all_names.extend(VIETNAMESE_NAMES_DATABASE["first_names"]["male"])
    all_names.extend(VIETNAMESE_NAMES_DATABASE["first_names"]["female"])
    all_names.extend(VIETNAMESE_NAMES_DATABASE["first_names"]["unisex"])
    return list(set(all_names))  # Loại bỏ trùng lặp

def is_valid_vietnamese_surname(name):
    """Kiểm tra có phải họ Việt Nam hợp lệ không"""
    return name in VIETNAMESE_NAMES_DATABASE["surnames"]

def is_valid_vietnamese_name(name):
    """Kiểm tra có phải tên Việt Nam hợp lệ không"""
    all_names = get_all_first_names()
    return name in all_names

def suggest_name_correction(name):
    """Gợi ý sửa tên dựa trên OCR corrections - Phiên bản nâng cao"""
    if not name or name.strip() == "":
        return name

    original_name = name.strip()

    # Thử exact match trước
    if original_name in OCR_NAME_CORRECTIONS:
        return OCR_NAME_CORRECTIONS[original_name]

    # Thử với chữ thường
    if original_name.lower() in OCR_NAME_CORRECTIONS:
        return OCR_NAME_CORRECTIONS[original_name.lower()]

    # Thử với chữ hoa
    if original_name.upper() in OCR_NAME_CORRECTIONS:
        return OCR_NAME_CORRECTIONS[original_name.upper()]

    # Thử với title case
    title_name = original_name.title()
    if title_name in OCR_NAME_CORRECTIONS:
        return OCR_NAME_CORRECTIONS[title_name]

    return original_name  # Không tìm thấy correction

def fix_vietnamese_name_advanced(full_name):
    """Sửa tên tiếng Việt nâng cao - xử lý cả họ tên đầy đủ"""
    if not full_name or full_name.strip() == "":
        return full_name

    # Tách tên thành các phần
    name_parts = full_name.strip().split()
    corrected_parts = []

    for part in name_parts:
        # Áp dụng correction cho từng phần
        corrected_part = suggest_name_correction(part)
        corrected_parts.append(corrected_part)

    return " ".join(corrected_parts)

def validate_vietnamese_name_structure(ho, ten):
    """Validate cấu trúc họ tên Việt Nam"""
    errors = []

    # Kiểm tra họ
    if ho:
        ho_parts = ho.split()
        first_part = ho_parts[0] if ho_parts else ""
        if first_part and not is_valid_vietnamese_surname(first_part):
            errors.append(f"Họ '{first_part}' không phổ biến")

    # Kiểm tra tên
    if ten and not is_valid_vietnamese_name(ten):
        errors.append(f"Tên '{ten}' không phổ biến")

    return len(errors) == 0, errors

def get_name_suggestions(partial_name, name_type="all"):
    """Lấy gợi ý tên dựa trên phần tên đã nhập"""
    suggestions = []
    partial_lower = partial_name.lower()

    if name_type in ["all", "surname"]:
        # Tìm trong họ
        for surname in VIETNAMESE_NAMES_DATABASE["surnames"]:
            if surname.lower().startswith(partial_lower):
                suggestions.append(surname)

    if name_type in ["all", "first_name"]:
        # Tìm trong tên riêng
        all_first_names = get_all_first_names()
        for name in all_first_names:
            if name.lower().startswith(partial_lower):
                suggestions.append(name)

    return suggestions[:10]  # Trả về tối đa 10 gợi ý

def get_name_statistics():
    """Lấy thống kê về database tên"""
    return {
        "total_surnames": len(VIETNAMESE_NAMES_DATABASE["surnames"]),
        "total_middle_names": len(VIETNAMESE_NAMES_DATABASE["middle_names"]),
        "total_male_names": len(VIETNAMESE_NAMES_DATABASE["first_names"]["male"]),
        "total_female_names": len(VIETNAMESE_NAMES_DATABASE["first_names"]["female"]),
        "total_unisex_names": len(VIETNAMESE_NAMES_DATABASE["first_names"]["unisex"]),
        "total_ocr_corrections": len(OCR_NAME_CORRECTIONS)
    }
