# data_validator.py - Validation và làm sạch dữ liệu

import re
import pandas as pd
from config import *

class DataValidator:
    """Class xử lý validation và làm sạch dữ liệu"""
    
    def __init__(self):
        self.corrections_applied = []
    
    def validate_and_clean_dataframe(self, df):
        """Kiểm tra và làm sạch DataFrame"""
        if df.empty:
            return df
            
        print("🔍 Đang validation và làm sạch dữ liệu...")
        self.corrections_applied = []
        
        for idx, row in df.iterrows():
            # Validate STT
            df.at[idx, 'STT'] = self._validate_stt(row['STT'], idx)
            
            # Validate MSV
            original_msv = str(row['MSV']).strip()
            cleaned_msv = self._validate_msv(original_msv)
            if cleaned_msv != original_msv:
                self._log_correction(f"MSV hàng {idx}", original_msv, cleaned_msv)
            df.at[idx, 'MSV'] = cleaned_msv
            
            # Validate Class
            original_class = str(row['Lớp']).strip()
            cleaned_class = self._validate_class(original_class)
            if cleaned_class != original_class:
                self._log_correction(f"Lớp hàng {idx}", original_class, cleaned_class)
            df.at[idx, 'Lớp'] = cleaned_class
            
            # Validate Names
            original_ho = str(row['Họ và đệm']).strip()
            original_ten = str(row['Tên']).strip()
            cleaned_ho = self._validate_vietnamese_name(original_ho)
            cleaned_ten = self._validate_vietnamese_name(original_ten)

            if cleaned_ho != original_ho:
                self._log_correction(f"Họ hàng {idx}", original_ho, cleaned_ho)
            if cleaned_ten != original_ten:
                self._log_correction(f"Tên hàng {idx}", original_ten, cleaned_ten)

            df.at[idx, 'Họ và đệm'] = cleaned_ho
            df.at[idx, 'Tên'] = cleaned_ten
            
            # Validate Scores
            for col in ['CC', 'KT1', 'KT2', 'KDT']:
                if col in df.columns:  # Kiểm tra cột có tồn tại không
                    original_score = str(row[col]).strip()
                    cleaned_score = self._validate_score(original_score)
                    if cleaned_score != original_score:
                        self._log_correction(f"{col} hàng {idx}", original_score, cleaned_score)
                    df.at[idx, col] = cleaned_score
        
        print(f"✅ Hoàn thành validation. Đã sửa {len(self.corrections_applied)} lỗi.")
        return df
    
    def _validate_stt(self, stt, row_index):
        """Validate số thứ tự"""
        stt_str = str(stt).strip()
        if not stt_str.isdigit() or int(stt_str) < 1 or int(stt_str) > 100:
            return str(row_index + 1)
        return stt_str
    
    def _validate_msv(self, msv):
        """Validate mã số sinh viên"""
        # Apply OCR corrections
        corrected_msv = msv
        for wrong, correct in OCR_NUMBER_CORRECTIONS.items():
            corrected_msv = corrected_msv.replace(wrong, correct)
        
        # Remove non-digits
        digits_only = re.sub(r'[^\d]', '', corrected_msv)
        
        # Check MSV pattern
        if len(digits_only) >= MIN_MSV_LENGTH:
            # Validate prefix
            if not any(digits_only.startswith(prefix) for prefix in VALID_MSV_PREFIXES):
                if digits_only.startswith('1'):
                    if digits_only[1] in '567':
                        digits_only = '1' + digits_only[1] + digits_only[2:]
                    else:
                        digits_only = '17' + digits_only[2:]
                else:
                    digits_only = '17' + digits_only[2:]
        
        # Ensure correct length
        if len(digits_only) < MAX_MSV_LENGTH:
            digits_only = digits_only.zfill(MAX_MSV_LENGTH)
        elif len(digits_only) > MAX_MSV_LENGTH:
            digits_only = digits_only[:MAX_MSV_LENGTH]
        
        return digits_only
    
    def _validate_class(self, class_name):
        """Validate tên lớp"""
        original = class_name
        class_name = class_name.upper().strip()
        
        # Apply class corrections
        for wrong, correct in OCR_CLASS_CORRECTIONS.items():
            if wrong in class_name:
                class_name = class_name.replace(wrong, correct)
        
        # Fix number errors
        class_name = class_name.replace('l7', '17').replace('I7', '17').replace('1?', '17')
        class_name = class_name.replace('l5', '15').replace('I5', '15').replace('O', '0')
        
        # Extract numbers
        numbers = re.findall(r'\d+', class_name)
        
        if len(numbers) >= 2:
            year = numbers[0]
            class_num = numbers[1]
            
            # Validate year
            if year not in VALID_MSV_PREFIXES:
                year = '17'  # Default
            
            # Validate class number
            if not class_num.isdigit() or int(class_num) < 1 or int(class_num) > 10:
                class_num = '02'
            else:
                class_num = class_num.zfill(2)
            
            return f"CNTT {year}-{class_num}"
            
        elif len(numbers) == 1:
            year = numbers[0]
            if year not in VALID_MSV_PREFIXES:
                year = '17'
            return f"CNTT {year}-02"
        
        return DEFAULT_CLASS
    
    def _validate_vietnamese_name(self, name):
        """Validate tên tiếng Việt - Phiên bản nâng cao"""
        if not name or name.strip() == "":
            return ""

        # Import các hàm từ config
        from config import fix_vietnamese_name_advanced, suggest_name_correction

        # Sử dụng hàm sửa lỗi nâng cao
        corrected_name = fix_vietnamese_name_advanced(name)

        # Đảm bảo format đúng (Title Case)
        return corrected_name.title() if corrected_name else ""
    
    def _validate_score(self, score):
        """Validate điểm số"""
        # Apply OCR corrections for numbers
        corrected_score = score
        for wrong, correct in OCR_NUMBER_CORRECTIONS.items():
            corrected_score = corrected_score.replace(wrong, correct)
        
        # Keep only digits and dots
        corrected_score = re.sub(r'[^\d\.]', '', corrected_score)
        
        # Ensure only one decimal point
        parts = corrected_score.split('.')
        if len(parts) > 2:
            corrected_score = parts[0] + '.' + ''.join(parts[1:])
        
        try:
            score_val = float(corrected_score)
            if VALID_SCORE_RANGE[0] <= score_val <= VALID_SCORE_RANGE[1]:
                return f"{score_val:.1f}"
        except:
            pass
        
        return DEFAULT_SCORE
    
    def _log_correction(self, field, original, corrected):
        """Ghi log các sửa đổi"""
        correction = f"{field}: {original} → {corrected}"
        self.corrections_applied.append(correction)
        print(f"  ✏️ {correction}")
    
    def get_corrections_summary(self):
        """Lấy tóm tắt các sửa đổi"""
        return self.corrections_applied
