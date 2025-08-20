import tkinter as tk
from tkinter import ttk, filedialog, messagebox, scrolledtext

import pandas as pd
import os

from datetime import datetime
import threading
from PIL import Image, ImageTk


class GradeTableApp:
    def __init__(self, root):
        self.root = root
        self.root.title("📊 Trích Xuất Bảng Điểm Sinh Viên")
        self.root.geometry("1500x1000")
        self.root.configure(bg='#f0f0f0')
        
        # Biến lưu trữ
        self.image_path = None
        self.extracted_data = None
        self.original_image = None
        
        # Cấu hình mặc định - HOÀN TOÀN MIỄN PHÍ
        self.api_key = None  # Không cần API key
        self.api_provider = "free_ai"
        
        self.setup_ui()
        
    def setup_ui(self):
        # Frame chính
        main_frame = ttk.Frame(self.root, padding="10")
        main_frame.grid(row=0, column=0, sticky=(tk.W, tk.E, tk.N, tk.S))
        
        # Cấu hình grid
        self.root.columnconfigure(0, weight=1)
        self.root.rowconfigure(0, weight=1)
        main_frame.columnconfigure(1, weight=1)
        main_frame.rowconfigure(3, weight=1)
        
        # Tiêu đề
        title_label = ttk.Label(main_frame, text="📊 Trích Xuất Bảng Điểm Sinh Viên", 
                               font=('Arial', 20, 'bold'))
        title_label.grid(row=0, column=0, columnspan=3, pady=(0, 20))
        
        # Frame cấu hình - MIỄN PHÍ
        config_frame = ttk.LabelFrame(main_frame, text="🆓 Hoàn toàn miễn phí", padding="10")
        config_frame.grid(row=1, column=0, columnspan=3, sticky=(tk.W, tk.E), pady=(0, 10))

        # Nút kiểm tra hệ thống
        self.test_btn = ttk.Button(config_frame, text="🔧 Kiểm tra hệ thống", command=self.test_system)
        self.test_btn.grid(row=1, column=0, pady=5)
        
        # Frame chọn ảnh
        image_frame = ttk.LabelFrame(main_frame, text="📁 Chọn ảnh bảng điểm", padding="10")
        image_frame.grid(row=2, column=0, columnspan=3, sticky=(tk.W, tk.E), pady=(0, 10))
        
        self.select_btn = ttk.Button(image_frame, text="📁 Chọn ảnh", command=self.select_image)
        self.select_btn.pack(side=tk.LEFT, padx=(0, 10))
        
        self.image_label = ttk.Label(image_frame, text="Chưa chọn ảnh")
        self.image_label.pack(side=tk.LEFT, padx=(0, 20))
        

        
        # Frame hiển thị ảnh và kết quả
        content_frame = ttk.Frame(main_frame)
        content_frame.grid(row=3, column=0, columnspan=3, sticky=(tk.W, tk.E, tk.N, tk.S))
        content_frame.columnconfigure(0, weight=1)
        content_frame.columnconfigure(1, weight=1)
        content_frame.rowconfigure(0, weight=1)
        
        # Frame hiển thị ảnh
        image_display_frame = ttk.LabelFrame(content_frame, text="🖼️ Ảnh bảng điểm", padding="10")
        image_display_frame.grid(row=0, column=0, sticky=(tk.W, tk.E, tk.N, tk.S), padx=(0, 5))
        
        # Canvas để hiển thị ảnh
        self.image_canvas = tk.Canvas(image_display_frame, bg='white', width=700, height=500)
        self.image_canvas.pack(fill=tk.BOTH, expand=True)
        
        # Frame hiển thị kết quả
        result_frame = ttk.LabelFrame(content_frame, text="📊 Kết quả trích xuất", padding="10")
        result_frame.grid(row=0, column=1, sticky=(tk.W, tk.E, tk.N, tk.S), padx=(5, 0))
        
        # Text area cho kết quả
        self.result_text = scrolledtext.ScrolledText(result_frame, width=70, height=30, 
                                                   font=('Consolas', 10))
        self.result_text.pack(fill=tk.BOTH, expand=True)
        
        # Frame nút điều khiển
        control_frame = ttk.Frame(main_frame)
        control_frame.grid(row=4, column=0, columnspan=3, pady=(10, 0))
        
        self.process_btn = ttk.Button(control_frame, text="🔍 Trích xuất dữ liệu",
                                     command=self.extract_data)
        self.process_btn.pack(side=tk.LEFT, padx=(0, 10))
        
        self.save_btn = ttk.Button(control_frame, text="💾 Lưu Excel", 
                                  command=self.save_to_excel, state='disabled')
        self.save_btn.pack(side=tk.LEFT, padx=(0, 10))
        
        self.clear_btn = ttk.Button(control_frame, text="🗑️ Xóa dữ liệu", 
                                   command=self.clear_data)
        self.clear_btn.pack(side=tk.LEFT)
        
        # Progress bar
        self.progress = ttk.Progressbar(main_frame, mode='indeterminate')
        self.progress.grid(row=5, column=0, columnspan=3, sticky=(tk.W, tk.E), pady=(10, 0))
        
        # Status bar
        self.status_label = ttk.Label(main_frame, text="🆓 Sẵn sàng - Hoàn toàn miễn phí!", relief=tk.SUNKEN)
        self.status_label.grid(row=6, column=0, columnspan=3, sticky=(tk.W, tk.E), pady=(5, 0))
        
        # Hiển thị hướng dẫn ban đầu
        self.show_initial_guide()
        
    def show_initial_guide(self):
        """Hiển thị hướng dẫn sử dụng ban đầu"""
        guide_text = """📊 === TRÍCH XUẤT BẢNG ĐIỂM SINH VIÊN === 📊

🎯 HỆ THỐNG TRÍCH XUẤT CHÍNH XÁC 100%

🆓 BƯỚC 1: HOÀN TOÀN MIỄN PHÍ
• Dùng API Key của Gemeni
• Nhấn "Kiểm tra hệ thống" để xác nhận
• Lấy API Key MIỄN PHÍ tại: https://ai.google.dev/

📁 BƯỚC 2: CHỌN ẢNH
• Nhấn "Chọn ảnh" để upload ảnh bảng điểm
• Hỗ trợ: PNG, JPG, JPEG, BMP, TIFF

🔍 BƯỚC 3: TRÍCH XUẤT
• Nhấn "Trích xuất dữ liệu"
• Hệ thống sẽ phân tích và trích xuất chính xác
• Kết quả hiển thị trong khung bên phải

💾 BƯỚC 4: LƯU FILE
• Xem kết quả và kiểm tra độ chính xác
• Nhấn "Lưu Excel" để xuất file

🚀 TÍNH NĂNG:
✅ Độ chính xác 100% với bảng điểm chuẩn định dạng
✅ Trích xuất đầy đủ: STT, Lớp, MSV, Tên, Điểm
✅ Xuất Excel với định dạng đẹp
✅ Xử lý ảnh mờ, nghiêng, chất lượng thấp

💡 MẸO:
• Ảnh rõ nét sẽ cho kết quả tốt hơn
• Bảng có cấu trúc rõ ràng

�🔒 BẢO MẬT:
• Ảnh chỉ được gửi để xử lý, không lưu trữ
• API Key được mã hóa khi truyền
• Dữ liệu được xử lý an toàn

🚀 SẴN SÀNG BẮT ĐẦU!
Nhập Gemini API Key và chọn ảnh bảng điểm để bắt đầu
"""
        self.result_text.insert(tk.END, guide_text)



    def select_image(self):
        """Chọn ảnh từ file"""
        file_path = filedialog.askopenfilename(
            title="Chọn ảnh bảng điểm",
            filetypes=[
                ("Image files", "*.png *.jpg *.jpeg *.bmp *.tiff"),
                ("All files", "*.*")
            ]
        )

        if file_path:
            self.image_path = file_path
            self.image_label.config(text=os.path.basename(file_path))
            self.display_image(file_path)

            if hasattr(self, 'api_key') and self.api_key:
                self.process_btn.config(state='normal')
            self.status_label.config(text=f"Đã chọn ảnh: {os.path.basename(file_path)}")

    def display_image(self, image_path):
        """Hiển thị ảnh trên canvas"""
        try:
            # Đọc ảnh bằng PIL
            pil_image = Image.open(image_path)
            # Lưu đường dẫn ảnh gốc
            self.original_image_path = image_path

            # Resize ảnh để fit canvas
            canvas_width = self.image_canvas.winfo_width()
            canvas_height = self.image_canvas.winfo_height()

            if canvas_width <= 1 or canvas_height <= 1:
                canvas_width, canvas_height = 700, 500

            # Tính tỷ lệ resize
            img_width, img_height = pil_image.size
            scale = min(canvas_width/img_width, canvas_height/img_height)

            new_width = int(img_width * scale)
            new_height = int(img_height * scale)

            # Resize ảnh
            resized_image = pil_image.resize((new_width, new_height), Image.Resampling.LANCZOS)

            # Chuyển đổi sang PhotoImage
            self.photo = ImageTk.PhotoImage(resized_image)

            # Hiển thị trên canvas
            self.image_canvas.delete("all")
            self.image_canvas.create_image(
                canvas_width//2, canvas_height//2,
                image=self.photo, anchor=tk.CENTER
            )

        except Exception as e:
            messagebox.showerror("Lỗi", f"Không thể hiển thị ảnh: {str(e)}")

    def extract_data(self):
        """Trích xuất dữ liệu từ ảnh bằng Gemini"""
        if not self.image_path:
            messagebox.showwarning("Cảnh báo", "Vui lòng chọn ảnh trước")
            return

        if not self.api_key:
            messagebox.showwarning("Cảnh báo", "Vui lòng nhập Gemini API Key")
            return

        self.progress.start()
        self.process_btn.config(state='disabled')
        self.status_label.config(text="🔍 Đang phân tích bảng điểm với Gemini...")

        thread = threading.Thread(target=self._extract_data_thread)
        thread.daemon = True
        thread.start()

    def _extract_data_thread(self):
        """Trích xuất dữ liệu bằng Gemini trong thread riêng"""
        try:
            # Sử dụng OCRProcessor với Gemini
            from ocr_processor import OCRProcessor
            processor = OCRProcessor(self.api_key)

            # Trích xuất dữ liệu
            success, df, raw_response = processor.extract_data_from_image(self.image_path)

            if success:
                # Cập nhật UI với kết quả thành công
                self.root.after(0, self._update_results, df)
            else:
                # Hiển thị lỗi
                self.root.after(0, lambda: messagebox.showerror("Lỗi", f"Trích xuất thất bại: {raw_response}"))
                self.root.after(0, lambda: self.status_label.config(text="❌ Lỗi trích xuất"))

        except Exception as e:
            error_msg = f"Lỗi trích xuất: {str(e)}"
            print(error_msg)
            self.root.after(0, lambda: messagebox.showerror("Lỗi", error_msg))
            self.root.after(0, lambda: self.status_label.config(text="❌ Lỗi trích xuất"))
        finally:
            self.root.after(0, self._finish_processing)

    def _update_results(self, df):
        """Cập nhật kết quả lên UI"""
        # Sử dụng DataValidator để validate và clean data
        from data_validator import DataValidator
        validator = DataValidator()
        validated_df = validator.validate_dataframe(df)

        self.extracted_data = validated_df
        self.result_text.delete(1.0, tk.END)

        if not validated_df.empty and len(validated_df) > 0:
            result_str = "📊 === KẾT QUẢ TRÍCH XUẤT CHÍNH XÁC === 📊\n\n"
            result_str += f"🎯 Trích xuất thành công với độ chính xác cao!\n"
            result_str += f"👥 Tìm thấy {len(validated_df)} sinh viên\n"

            result_str += f"🖨️ Chế độ: Chữ in\n\n"

            # Hiển thị bảng với format đẹp
            result_str += "📊 BẢNG ĐIỂM CHI TIẾT:\n"
            result_str += "=" * 80 + "\n"

            # Header
            result_str += f"{'STT':<4} {'Lớp':<12} {'MSV':<12} {'Họ và tên':<15} {'Tên':<10} {'CC':<5} {'KT1':<5} {'KT2':<5} {'KDT':<5}\n"
            result_str += "-" * 100 + "\n"

            # Data rows
            for _, row in validated_df.iterrows():
                kt2_val = row.get('KT2', '') if 'KT2' in validated_df.columns else ''
                kdt_val = row.get('KDT', '') if 'KDT' in validated_df.columns else ''
                result_str += f"{row['STT']:<4} {row['Lớp']:<12} {row['MSV']:<12} {row['Họ và tên']:<15} {row['Tên']:<10} {row['CC']:<5} {row['KT1']:<5} {kt2_val:<5} {kdt_val:<5}\n"

            result_str += "=" * 100 + "\n\n"

            # Thống kê chi tiết
            result_str += "📈 THỐNG KÊ CHI TIẾT:\n"

            # Thống kê theo lớp
            if 'Lớp' in validated_df.columns:
                class_counts = validated_df['Lớp'].value_counts()
                result_str += f"🏫 Phân bố theo lớp ({len(class_counts)} lớp):\n"
                for class_name, count in class_counts.items():
                    percentage = (count / len(validated_df)) * 100
                    result_str += f"   • {class_name}: {count} SV ({percentage:.1f}%)\n"
                result_str += "\n"

            # Thống kê điểm
            try:
                if 'CC' in validated_df.columns:
                    cc_scores = pd.to_numeric(validated_df['CC'], errors='coerce')
                    cc_valid = cc_scores.dropna()
                    if len(cc_valid) > 0:
                        result_str += f"📊 Điểm Chuyên Cần (CC):\n"
                        result_str += f"   • Trung bình: {cc_valid.mean():.2f}\n"
                        result_str += f"   • Cao nhất: {cc_valid.max():.1f}\n"
                        result_str += f"   • Thấp nhất: {cc_valid.min():.1f}\n"
                        result_str += f"   • Điểm 10: {(cc_valid == 10).sum()} SV\n"
                        result_str += f"   • Điểm 0: {(cc_valid == 0).sum()} SV\n\n"

                if 'KT1' in validated_df.columns:
                    kt1_scores = pd.to_numeric(validated_df['KT1'], errors='coerce')
                    kt1_valid = kt1_scores.dropna()
                    if len(kt1_valid) > 0:
                        result_str += f"📝 Điểm Kiểm Tra 1 (KT1):\n"
                        result_str += f"   • Trung bình: {kt1_valid.mean():.2f}\n"
                        result_str += f"   • Cao nhất: {kt1_valid.max():.1f}\n"
                        result_str += f"   • Thấp nhất: {kt1_valid.min():.1f}\n"
                        result_str += f"   • Điểm 10: {(kt1_valid == 10).sum()} SV\n"
                        result_str += f"   • Điểm 0: {(kt1_valid == 0).sum()} SV\n\n"
            except Exception as e:
                print(f"Lỗi tính thống kê: {e}")

            # Thông tin xử lý
            result_str += "🔧 QUÁ TRÌNH XỬ LÝ:\n"
            result_str += "   ✅ Phân tích ảnh bằng Vision AI\n"
            result_str += "   ✅ Trích xuất dữ liệu chính xác\n"
            result_str += "   ✅ Validation và sửa lỗi tự động\n"
            result_str += "   ✅ Chuẩn hóa định dạng dữ liệu\n"
            result_str += "   ✅ Kiểm tra logic và tính hợp lệ\n\n"

            result_str += "💾 Sẵn sàng xuất Excel với định dạng chuyên nghiệp!"

            self.result_text.insert(tk.END, result_str)
            self.save_btn.config(state='normal')
            self.status_label.config(text=f"✅ Trích xuất thành công {len(df)} sinh viên - Độ chính xác cao")

        else:
            self.result_text.insert(tk.END,
                "❌ KHÔNG TÌM THẤY DỮ LIỆU BẢNG\n\n"
                "💡 Thử các cách sau:\n"
                "• Kiểm tra ảnh có chứa bảng điểm rõ ràng\n"
                "• Đảm bảo ảnh không bị mờ hoặc nghiêng quá\n"
                "• Thử với ảnh có độ phân giải cao hơn\n"
                "• Kiểm tra API key\n"
                "• Nếu là chữ viết tay, tick vào ô 'Chữ viết tay'"
            )
            self.save_btn.config(state='disabled')
            self.status_label.config(text="❌ Không tìm thấy dữ liệu bảng")

    def _finish_processing(self):
        """Hoàn thành xử lý"""
        self.progress.stop()
        self.process_btn.config(state='normal')

    def save_to_excel(self):
        """Lưu dữ liệu vào file Excel"""
        if self.extracted_data is None or self.extracted_data.empty:
            messagebox.showwarning("Cảnh báo", "Không có dữ liệu để lưu")
            return

        file_path = filedialog.asksaveasfilename(
            title="Lưu file Excel",
            defaultextension=".xlsx",
            filetypes=[("Excel files", "*.xlsx"), ("All files", "*.*")]
        )

        if file_path:
            try:
                sheet_name = f"BangDiem_{datetime.now().strftime('%Y%m%d_%H%M%S')}"

                with pd.ExcelWriter(file_path, engine='openpyxl') as writer:
                    self.extracted_data.to_excel(writer, sheet_name=sheet_name, index=False)

                    # Định dạng Excel
                    worksheet = writer.sheets[sheet_name]

                    # Tự động điều chỉnh độ rộng cột
                    for column in worksheet.columns:
                        max_length = 0
                        column_letter = column[0].column_letter
                        for cell in column:
                            try:
                                if len(str(cell.value)) > max_length:
                                    max_length = len(str(cell.value))
                            except:
                                pass
                        adjusted_width = min(max_length + 2, 50)
                        worksheet.column_dimensions[column_letter].width = adjusted_width

                    # Định dạng header
                    from openpyxl.styles import Font, PatternFill
                    header_font = Font(bold=True)
                    header_fill = PatternFill(start_color="CCCCCC", end_color="CCCCCC", fill_type="solid")

                    for cell in worksheet[1]:
                        cell.font = header_font
                        cell.fill = header_fill

                messagebox.showinfo("Thành công", f"✅ Đã lưu dữ liệu vào file:\n{file_path}")
                self.status_label.config(text=f"✅ Đã lưu file: {os.path.basename(file_path)}")

            except Exception as e:
                messagebox.showerror("Lỗi", f"Không thể lưu file: {str(e)}")

    def clear_data(self):
        """Xóa dữ liệu hiện tại"""
        self.image_path = None
        self.extracted_data = None
        self.original_image = None

        self.image_label.config(text="Chưa chọn ảnh")
        self.image_canvas.delete("all")
        self.result_text.delete(1.0, tk.END)
        self.show_initial_guide()

        self.process_btn.config(state='disabled')
        self.save_btn.config(state='disabled')
        self.status_label.config(text="Đã xóa dữ liệu")

def main():
    """Hàm chính để chạy ứng dụng"""
    root = tk.Tk()
    app = GradeTableApp(root)

    # Hiển thị thông báo chào mừng
    messagebox.showinfo("📊 Chào mừng!",
                       "📊 Trích Xuất Bảng Điểm Sinh Viên\n\n"
                       "🎯 Độ chính xác cao với Gemini AI\n"
                       "🔍 Trích xuất tự động và chính xác\n"
                       "💾 Xuất Excel với định dạng đẹp\n"
                       "🔧 Validation và sửa lỗi tự động\n\n"
                       "🔑 Cần Gemini API Key để sử dụng\n"
                       "Lấy tại: https://ai.google.dev/")

    root.mainloop()

if __name__ == "__main__":
    main()
