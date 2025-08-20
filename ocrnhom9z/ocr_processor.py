# ocr_processor.py - Xử lý OCR và Gemini Vision

import json
import pandas as pd
import google.generativeai as genai
from PIL import Image
from config import *
from prompt_manager import PromptManager

class OCRProcessor:
    """Class xử lý OCR và Gemini Vision API"""

    def __init__(self, api_key):
        self.api_key = api_key
        self.last_response = None
        self.prompt_manager = PromptManager()
        if api_key:
            genai.configure(api_key=api_key)
            self.model = genai.GenerativeModel(GEMINI_MODEL)
    
    def test_api_connection(self):
        """Kiểm tra kết nối Gemini API"""
        try:
            if not self.api_key:
                return False, "API Key không được để trống"

            # Cấu hình Gemini
            genai.configure(api_key=self.api_key)
            self.model = genai.GenerativeModel(GEMINI_MODEL)

            # Test với prompt đơn giản
            response = self.model.generate_content("Hello, test connection")

            if response and response.text:
                return True, "Kết nối Gemini API thành công! 🆓 Hoàn toàn miễn phí!"
            else:
                return False, "Không nhận được response từ Gemini"

        except Exception as e:
            error_msg = str(e)
            if "API_KEY_INVALID" in error_msg:
                return False, "API Key không hợp lệ - Vui lòng kiểm tra lại"
            elif "QUOTA_EXCEEDED" in error_msg:
                return False, "Vượt quá quota - Vui lòng thử lại sau"
            else:
                return False, f"Lỗi kết nối Gemini: {error_msg}"
    
    def extract_data_from_image(self, image_path):
        """Trích xuất dữ liệu từ ảnh bằng Gemini"""
        try:
            print(f"🔍 Bắt đầu trích xuất: {image_path}")

            # Mở ảnh bằng PIL
            image = Image.open(image_path)
            print(f"📸 Đã mở ảnh thành công: {image.size}")

            # Tạo prompt
            prompt = self._create_prompt()
            print(f"📝 Đã tạo prompt")

            # Gọi Gemini Vision API
            response_text = self._call_gemini_vision_api(image, prompt)
            print(f"🤖 Gemini response length: {len(response_text)} chars")

            # Parse kết quả thành DataFrame
            df = self._parse_response_to_dataframe(response_text)
            print(f"📊 Parsed DataFrame: {len(df)} rows")

            return True, df, response_text

        except Exception as e:
            print(f"❌ Lỗi trích xuất: {str(e)}")
            return False, pd.DataFrame(), f"Lỗi trích xuất: {str(e)}"
    
    def _call_gemini_vision_api(self, image, prompt):
        """Gọi Gemini Vision API"""
        try:
            # Tạo content với ảnh và prompt
            response = self.model.generate_content([prompt, image])

            if response and response.text:
                return response.text
            else:
                raise Exception("Không nhận được response từ Gemini")

        except Exception as e:
            raise Exception(f"Lỗi Gemini API: {str(e)}")
    
    def _create_prompt(self):
        """Tạo prompt cho Gemini từ template hiện tại"""
        return self.prompt_manager.get_current_prompt()
    

    

    
    def _parse_response_to_dataframe(self, response_text):
        """Parse response thành DataFrame"""
        try:
            # Tìm JSON trong response
            json_start = response_text.find('{')
            json_end = response_text.rfind('}') + 1
            
            if json_start != -1 and json_end > json_start:
                json_str = response_text[json_start:json_end]
                data = json.loads(json_str)
                
                if 'students' in data and data['students']:
                    students = data['students']
                    
                    # Lấy cấu trúc cột từ template hiện tại
                    columns_config = self.prompt_manager.get_current_columns()

                    # Tạo DataFrame với cấu trúc động
                    df_data = []
                    for i, student in enumerate(students):
                        row = []

                        # Xử lý từng cột theo cấu hình
                        for col_config in columns_config:
                            col_key = col_config.get('key', '')
                            value = student.get(col_key, '').strip()

                            # Xử lý đặc biệt cho tên (nếu có cả ho và ten)
                            if col_key == 'ho' and 'ten' in [c.get('key') for c in columns_config]:
                                ho = student.get('ho', '').strip()
                                ten = student.get('ten', '').strip()

                                # DEBUG: In ra để kiểm tra
                                print(f"Student {i+1}: ho='{ho}', ten='{ten}'")

                                # VALIDATION: Kiểm tra phân chia tên
                                if ho and ten:
                                    ho_words = ho.split()
                                    ten_words = ten.split()

                                    # Kiểm tra các trường hợp lỗi phân chia tên
                                    needs_fix = False

                                    # Trường hợp 1: ho có 1 từ, ten có nhiều từ
                                    if len(ho_words) == 1 and len(ten_words) > 1:
                                        print(f"⚠️ PHÁT HIỆN LỖI PHÂN CHIA TÊN (Type 1): ho='{ho}' (1 từ), ten='{ten}' ({len(ten_words)} từ)")
                                        needs_fix = True

                                    # Trường hợp 2: ten có nhiều từ (bất kể ho có bao nhiêu từ)
                                    elif len(ten_words) > 1:
                                        print(f"⚠️ PHÁT HIỆN LỖI PHÂN CHIA TÊN (Type 2): ten='{ten}' có {len(ten_words)} từ (phải chỉ có 1 từ)")
                                        needs_fix = True

                                    # Trường hợp 3: ho trống nhưng ten có nhiều từ
                                    elif not ho and len(ten_words) > 1:
                                        print(f"⚠️ PHÁT HIỆN LỖI PHÂN CHIA TÊN (Type 3): ho trống, ten='{ten}' có {len(ten_words)} từ")
                                        needs_fix = True

                                    if needs_fix:
                                        # Tự động sửa: ghép lại và phân chia đúng
                                        full_name = f"{ho} {ten}".strip()
                                        name_parts = full_name.split()
                                        if len(name_parts) >= 2:
                                            ho = " ".join(name_parts[:-1])  # Tất cả trừ từ cuối
                                            ten = name_parts[-1]  # Từ cuối
                                            print(f"✅ ĐÃ SỬA: ho='{ho}', ten='{ten}'")
                                            # Cập nhật lại trong student data
                                            student['ho'] = ho
                                            student['ten'] = ten
                                        elif len(name_parts) == 1:
                                            # Chỉ có 1 từ - để làm tên, ho để trống
                                            ho = ""
                                            ten = name_parts[0]
                                            print(f"✅ ĐÃ SỬA (1 từ): ho='', ten='{ten}'")
                                            student['ho'] = ho
                                            student['ten'] = ten

                                value = ho

                            row.append(value)

                        df_data.append(row)

                    # Tạo headers từ cấu hình cột
                    headers = [col.get('name', col.get('key', '')) for col in columns_config]

                    df = pd.DataFrame(df_data, columns=headers)

                    # Làm sạch tên cột - loại bỏ dấu ngoặc kép thừa
                    df.columns = [col.replace('"', '').strip() for col in df.columns]

                    print(f"📊 DataFrame columns: {list(df.columns)}")
                    return df
                    
        except Exception as e:
            print(f"Lỗi parse JSON: {e}")
            print(f"Response: {response_text}")
        
        # Fallback - tạo DataFrame trống
        return pd.DataFrame()
    


    def get_last_response(self):
        """Lấy response cuối cùng từ API"""
        return self.last_response
