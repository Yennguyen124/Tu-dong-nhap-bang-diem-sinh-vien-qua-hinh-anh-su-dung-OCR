# database_manager.py - Quản lý kết nối và thao tác với SQL Server

import pyodbc
import pandas as pd
from datetime import datetime
import logging
from typing import List, Dict, Optional, Tuple
import json

class DatabaseManager:
    """Lớp quản lý kết nối và thao tác với SQL Server"""
    
    def __init__(self, server_name: str = None, database_name: str = None):
        """
        Khởi tạo DatabaseManager
        
        Args:
            server_name: Tên SQL Server (mặc định: localhost)
            database_name: Tên database (mặc định: GradeManagement)
        """
        self.server_name = server_name or "localhost"
        self.database_name = database_name or "GradeManagement"
        self.connection = None
        self.connection_string = None
        
        # Thiết lập logging
        logging.basicConfig(level=logging.INFO)
        self.logger = logging.getLogger(__name__)
        
        # Tạo connection string cho Windows Authentication
        self._build_connection_string()
    
    def _build_connection_string(self):
        """Tạo connection string cho Windows Authentication"""
        # Sử dụng Windows Authentication (Trusted_Connection=yes)
        self.connection_string = (
            f"DRIVER={{ODBC Driver 17 for SQL Server}};"
            f"SERVER={self.server_name};"
            f"DATABASE={self.database_name};"
            f"Trusted_Connection=yes;"
            f"TrustServerCertificate=yes;"
        )
        
        self.logger.info(f"Connection string created for server: {self.server_name}, database: {self.database_name}")
    
    def test_connection(self) -> Tuple[bool, str]:
        """
        Test kết nối đến SQL Server
        
        Returns:
            Tuple[bool, str]: (success, message)
        """
        try:
            # Thử kết nối đến master database trước
            master_connection_string = (
                f"DRIVER={{ODBC Driver 17 for SQL Server}};"
                f"SERVER={self.server_name};"
                f"DATABASE=master;"
                f"Trusted_Connection=yes;"
                f"TrustServerCertificate=yes;"
            )
            
            with pyodbc.connect(master_connection_string, timeout=10) as conn:
                cursor = conn.cursor()
                cursor.execute("SELECT @@VERSION")
                version = cursor.fetchone()[0]
                self.logger.info(f"Connected to SQL Server: {version}")
                
                # Kiểm tra xem database có tồn tại không
                cursor.execute(f"SELECT database_id FROM sys.databases WHERE name = '{self.database_name}'")
                db_exists = cursor.fetchone()
                
                if not db_exists:
                    return False, f"Database '{self.database_name}' không tồn tại. Bạn có muốn tạo database mới không?"
                
                # Test kết nối đến database cụ thể
                with pyodbc.connect(self.connection_string, timeout=10) as db_conn:
                    db_cursor = db_conn.cursor()
                    db_cursor.execute("SELECT GETDATE()")
                    current_time = db_cursor.fetchone()[0]
                    
                return True, f"Kết nối thành công! Server time: {current_time}"
                
        except pyodbc.Error as e:
            error_msg = f"Lỗi kết nối SQL Server: {str(e)}"
            self.logger.error(error_msg)
            return False, error_msg
        except Exception as e:
            error_msg = f"Lỗi không xác định: {str(e)}"
            self.logger.error(error_msg)
            return False, error_msg
    
    def connect(self) -> bool:
        """
        Kết nối đến database
        
        Returns:
            bool: True nếu kết nối thành công
        """
        try:
            if self.connection:
                self.disconnect()
            
            self.connection = pyodbc.connect(self.connection_string, timeout=30)
            self.connection.autocommit = False  # Sử dụng transaction
            self.logger.info("Đã kết nối đến database thành công")
            return True
            
        except pyodbc.Error as e:
            self.logger.error(f"Lỗi kết nối database: {str(e)}")
            return False
    
    def disconnect(self):
        """Ngắt kết nối database"""
        if self.connection:
            try:
                self.connection.close()
                self.connection = None
                self.logger.info("Đã ngắt kết nối database")
            except Exception as e:
                self.logger.error(f"Lỗi khi ngắt kết nối: {str(e)}")
    
    def create_database(self) -> Tuple[bool, str]:
        """
        Tạo database mới

        Returns:
            Tuple[bool, str]: (success, message)
        """
        try:
            # Kết nối đến master database để tạo database mới
            master_connection_string = (
                f"DRIVER={{ODBC Driver 17 for SQL Server}};"
                f"SERVER={self.server_name};"
                f"DATABASE=master;"
                f"Trusted_Connection=yes;"
                f"TrustServerCertificate=yes;"
            )

            with pyodbc.connect(master_connection_string, autocommit=True) as conn:
                cursor = conn.cursor()

                # Kiểm tra xem database đã tồn tại chưa
                cursor.execute(f"SELECT database_id FROM sys.databases WHERE name = '{self.database_name}'")
                if cursor.fetchone():
                    return False, f"Database '{self.database_name}' đã tồn tại"

                # Tạo database mới (không cần commit vì autocommit=True)
                create_db_sql = f"CREATE DATABASE [{self.database_name}] COLLATE Vietnamese_CI_AS"
                cursor.execute(create_db_sql)

                self.logger.info(f"Đã tạo database '{self.database_name}' thành công")
                return True, f"Database '{self.database_name}' đã được tạo thành công"

        except pyodbc.Error as e:
            error_msg = f"Lỗi tạo database: {str(e)}"
            self.logger.error(error_msg)
            return False, error_msg
    
    def create_tables(self) -> Tuple[bool, str]:
        """
        Tạo các bảng cần thiết cho ứng dụng
        
        Returns:
            Tuple[bool, str]: (success, message)
        """
        if not self.connect():
            return False, "Không thể kết nối đến database"
        
        try:
            cursor = self.connection.cursor()
            
            # Tạo bảng Students (Sinh viên)
            create_students_table = """
            IF NOT EXISTS (SELECT * FROM sysobjects WHERE name='Students' AND xtype='U')
            CREATE TABLE Students (
                StudentID INT IDENTITY(1,1) PRIMARY KEY,
                MSV NVARCHAR(20) UNIQUE NOT NULL,
                [Họ và đệm] NVARCHAR(100) NOT NULL,
                [Tên] NVARCHAR(50) NOT NULL,
                [Lớp] NVARCHAR(50),
                CreatedDate DATETIME DEFAULT GETDATE(),
                UpdatedDate DATETIME DEFAULT GETDATE()
            )
            """
            
            # Tạo bảng Grades (Điểm số)
            create_grades_table = """
            IF NOT EXISTS (SELECT * FROM sysobjects WHERE name='Grades' AND xtype='U')
            CREATE TABLE Grades (
                GradeID INT IDENTITY(1,1) PRIMARY KEY,
                StudentID INT FOREIGN KEY REFERENCES Students(StudentID),
                MSV NVARCHAR(20) NOT NULL,
                CC FLOAT,
                KT1 FLOAT,
                KT2 FLOAT,
                KDT FLOAT,
                Subject NVARCHAR(100),
                Semester NVARCHAR(20),
                Year INT,
                CreatedDate DATETIME DEFAULT GETDATE(),
                UpdatedDate DATETIME DEFAULT GETDATE()
            )
            """
            
            # Tạo bảng OCR_Sessions (Phiên OCR)
            create_sessions_table = """
            IF NOT EXISTS (SELECT * FROM sysobjects WHERE name='OCR_Sessions' AND xtype='U')
            CREATE TABLE OCR_Sessions (
                SessionID INT IDENTITY(1,1) PRIMARY KEY,
                SessionName NVARCHAR(200),
                ImagePath NVARCHAR(500),
                ProcessedDate DATETIME DEFAULT GETDATE(),
                TotalStudents INT,
                SuccessCount INT,
                ErrorCount INT,
                Notes NVARCHAR(1000)
            )
            """
            
            # Thực thi các câu lệnh tạo bảng
            cursor.execute(create_students_table)
            cursor.execute(create_grades_table)
            cursor.execute(create_sessions_table)
            
            self.connection.commit()
            self.logger.info("Đã tạo tất cả bảng thành công")
            return True, "Tất cả bảng đã được tạo thành công"
            
        except pyodbc.Error as e:
            self.connection.rollback()
            error_msg = f"Lỗi tạo bảng: {str(e)}"
            self.logger.error(error_msg)
            return False, error_msg
        finally:
            self.disconnect()
    
    def insert_student(self, msv: str, ho: str, ten: str, lop: str = None) -> Tuple[bool, str]:
        """
        Thêm sinh viên mới
        
        Args:
            msv: Mã số sinh viên
            ho: Họ và tên đệm
            ten: Tên
            lop: Lớp
            
        Returns:
            Tuple[bool, str]: (success, message)
        """
        if not self.connect():
            return False, "Không thể kết nối đến database"
        
        try:
            cursor = self.connection.cursor()
            
            # Kiểm tra xem sinh viên đã tồn tại chưa
            cursor.execute("SELECT StudentID FROM Students WHERE MSV = ?", (msv,))
            if cursor.fetchone():
                return False, f"Sinh viên với MSV {msv} đã tồn tại"
            
            # Thêm sinh viên mới
            insert_sql = """
            INSERT INTO Students (MSV, Ho, Ten, Lop)
            VALUES (?, ?, ?, ?)
            """
            cursor.execute(insert_sql, (msv, ho, ten, lop))
            self.connection.commit()
            
            self.logger.info(f"Đã thêm sinh viên {msv} - {ho} {ten}")
            return True, f"Đã thêm sinh viên {msv} thành công"
            
        except pyodbc.Error as e:
            self.connection.rollback()
            error_msg = f"Lỗi thêm sinh viên: {str(e)}"
            self.logger.error(error_msg)
            return False, error_msg
        finally:
            self.disconnect()
    
    def insert_grades_dynamic(self, grades_data: List[Dict]) -> Tuple[bool, str, int]:
        """
        Thêm điểm số với cấu trúc động - chỉ lưu các cột có dữ liệu

        Args:
            grades_data: List các dict chứa thông tin điểm

        Returns:
            Tuple[bool, str, int]: (success, message, inserted_count)
        """
        if not self.connect():
            return False, "Không thể kết nối đến database", 0

        try:
            cursor = self.connection.cursor()
            inserted_count = 0
            errors = []

            # Phát hiện các cột điểm có trong dữ liệu
            score_columns = []
            if grades_data:
                first_record = grades_data[0]
                possible_scores = ['CC', 'KT1', 'KT2', 'KDT', 'TX1', 'TX2', 'GK', 'CK']
                score_columns = [col for col in possible_scores if col in first_record and first_record[col] is not None]
                print(f"Các cột điểm được phát hiện: {score_columns}")

            for grade_info in grades_data:
                try:
                    msv = grade_info.get('MSV', '')
                    ho = grade_info.get('Họ và đệm', '')
                    ten = grade_info.get('Tên', '')
                    lop = grade_info.get('Lớp', '')

                    # Thêm hoặc cập nhật sinh viên
                    cursor.execute("SELECT StudentID FROM Students WHERE MSV = ?", (msv,))
                    student = cursor.fetchone()

                    if not student:
                        # Thêm sinh viên mới
                        cursor.execute("""
                            INSERT INTO Students (MSV, [Họ và đệm], [Tên], [Lớp])
                            VALUES (?, ?, ?, ?)
                        """, (msv, ho, ten, lop))

                        cursor.execute("SELECT @@IDENTITY")
                        student_id = cursor.fetchone()[0]
                    else:
                        student_id = student[0]
                        # Cập nhật thông tin sinh viên
                        cursor.execute("""
                            UPDATE Students
                            SET [Họ và đệm] = ?, [Tên] = ?, [Lớp] = ?, UpdatedDate = GETDATE()
                            WHERE StudentID = ?
                        """, (ho, ten, lop, student_id))

                    # Tạo câu lệnh INSERT động cho điểm
                    if score_columns:
                        columns_str = ', '.join(score_columns)
                        placeholders = ', '.join(['?' for _ in score_columns])
                        values = [grade_info.get(col) for col in score_columns]

                        # Kiểm tra xem điểm đã tồn tại chưa
                        cursor.execute("SELECT GradeID FROM Grades WHERE StudentID = ? AND MSV = ?", (student_id, msv))
                        existing_grade = cursor.fetchone()

                        if existing_grade:
                            # Cập nhật điểm hiện có
                            update_str = ', '.join([f"{col} = ?" for col in score_columns])
                            cursor.execute(f"""
                                UPDATE Grades
                                SET {update_str}, UpdatedDate = GETDATE()
                                WHERE StudentID = ? AND MSV = ?
                            """, values + [student_id, msv])
                        else:
                            # Thêm điểm mới
                            cursor.execute(f"""
                                INSERT INTO Grades (StudentID, MSV, {columns_str})
                                VALUES (?, ?, {placeholders})
                            """, [student_id, msv] + values)

                    inserted_count += 1

                except Exception as e:
                    errors.append(f"Lỗi với MSV {msv}: {str(e)}")
                    continue

            self.connection.commit()

            if errors:
                error_msg = f"Đã thêm {inserted_count} bản ghi. Lỗi: {'; '.join(errors[:3])}"
                return True, error_msg, inserted_count
            else:
                return True, f"Đã thêm {inserted_count} bản ghi thành công với các cột: {', '.join(score_columns)}", inserted_count

        except pyodbc.Error as e:
            self.connection.rollback()
            error_msg = f"Lỗi thêm điểm: {str(e)}"
            self.logger.error(error_msg)
            return False, error_msg, 0
        finally:
            self.disconnect()

    def insert_grades(self, grades_data: List[Dict]) -> Tuple[bool, str, int]:
        """
        Thêm điểm số cho nhiều sinh viên
        
        Args:
            grades_data: List các dict chứa thông tin điểm
            
        Returns:
            Tuple[bool, str, int]: (success, message, inserted_count)
        """
        if not self.connect():
            return False, "Không thể kết nối đến database", 0
        
        try:
            cursor = self.connection.cursor()
            inserted_count = 0
            errors = []
            
            for grade_info in grades_data:
                try:
                    msv = grade_info.get('MSV', '')
                    ho = grade_info.get('Họ và đệm', '')
                    ten = grade_info.get('Tên', '')
                    lop = grade_info.get('Lớp', '')
                    cc = grade_info.get('CC', None)
                    kt1 = grade_info.get('KT1', None)
                    kt2 = grade_info.get('KT2', None)
                    kdt = grade_info.get('KDT', None)
                    
                    # Thêm hoặc cập nhật sinh viên
                    cursor.execute("SELECT StudentID FROM Students WHERE MSV = ?", (msv,))
                    student = cursor.fetchone()
                    
                    if not student:
                        # Thêm sinh viên mới
                        cursor.execute("""
                            INSERT INTO Students (MSV, Ho, Ten, Lop)
                            VALUES (?, ?, ?, ?)
                        """, (msv, ho, ten, lop))
                        
                        cursor.execute("SELECT @@IDENTITY")
                        student_id = cursor.fetchone()[0]
                    else:
                        student_id = student[0]
                        # Cập nhật thông tin sinh viên
                        cursor.execute("""
                            UPDATE Students 
                            SET Ho = ?, Ten = ?, Lop = ?, UpdatedDate = GETDATE()
                            WHERE StudentID = ?
                        """, (ho, ten, lop, student_id))
                    
                    # Kiểm tra xem điểm đã tồn tại chưa (tránh trùng lặp)
                    cursor.execute("""
                        SELECT GradeID FROM Grades
                        WHERE StudentID = ? AND MSV = ?
                    """, (student_id, msv))

                    existing_grade = cursor.fetchone()

                    if existing_grade:
                        # Cập nhật điểm hiện có
                        cursor.execute("""
                            UPDATE Grades
                            SET CC = ?, KT1 = ?, KT2 = ?, KDT = ?, UpdatedDate = GETDATE()
                            WHERE StudentID = ? AND MSV = ?
                        """, (cc, kt1, kt2, kdt, student_id, msv))
                    else:
                        # Thêm điểm mới
                        cursor.execute("""
                            INSERT INTO Grades (StudentID, MSV, CC, KT1, KT2, KDT)
                            VALUES (?, ?, ?, ?, ?, ?)
                        """, (student_id, msv, cc, kt1, kt2, kdt))
                    
                    inserted_count += 1
                    
                except Exception as e:
                    errors.append(f"Lỗi với MSV {msv}: {str(e)}")
                    continue
            
            self.connection.commit()
            
            if errors:
                error_msg = f"Đã thêm {inserted_count} bản ghi. Lỗi: {'; '.join(errors[:3])}"
                return True, error_msg, inserted_count
            else:
                return True, f"Đã thêm {inserted_count} bản ghi thành công", inserted_count
                
        except pyodbc.Error as e:
            self.connection.rollback()
            error_msg = f"Lỗi thêm điểm: {str(e)}"
            self.logger.error(error_msg)
            return False, error_msg, 0
        finally:
            self.disconnect()

    def clean_duplicate_grades(self) -> Tuple[bool, str]:
        """
        Xóa các bản ghi điểm trùng lặp, chỉ giữ lại bản ghi mới nhất

        Returns:
            Tuple[bool, str]: (success, message)
        """
        if not self.connect():
            return False, "Không thể kết nối đến database"

        try:
            cursor = self.connection.cursor()

            # Xóa các bản ghi trùng lặp, chỉ giữ lại GradeID lớn nhất (mới nhất)
            delete_duplicates_sql = """
            DELETE g1 FROM Grades g1
            INNER JOIN Grades g2
            WHERE g1.StudentID = g2.StudentID
            AND g1.MSV = g2.MSV
            AND g1.GradeID < g2.GradeID
            """

            cursor.execute(delete_duplicates_sql)
            deleted_count = cursor.rowcount
            self.connection.commit()

            self.logger.info(f"Đã xóa {deleted_count} bản ghi trùng lặp")
            return True, f"Đã xóa {deleted_count} bản ghi trùng lặp"

        except Exception as e:
            error_msg = f"Lỗi xóa dữ liệu trùng lặp: {str(e)}"
            self.logger.error(error_msg)
            return False, error_msg
        finally:
            self.disconnect()

    def get_students(self, limit: int = 100) -> Tuple[bool, str, pd.DataFrame]:
        """
        Lấy danh sách sinh viên
        
        Args:
            limit: Số lượng bản ghi tối đa
            
        Returns:
            Tuple[bool, str, pd.DataFrame]: (success, message, dataframe)
        """
        if not self.connect():
            return False, "Không thể kết nối đến database", pd.DataFrame()
        
        try:
            query = f"""
            SELECT TOP {limit}
                s.MSV, s.Ho, s.Ten, s.Lop, s.CreatedDate,
                COUNT(g.GradeID) as TotalGrades
            FROM Students s
            LEFT JOIN Grades g ON s.StudentID = g.StudentID
            GROUP BY s.MSV, s.Ho, s.Ten, s.Lop, s.CreatedDate
            ORDER BY s.CreatedDate DESC
            """
            
            df = pd.read_sql(query, self.connection)
            return True, f"Đã lấy {len(df)} sinh viên", df
            
        except pyodbc.Error as e:
            error_msg = f"Lỗi lấy danh sách sinh viên: {str(e)}"
            self.logger.error(error_msg)
            return False, error_msg, pd.DataFrame()
        finally:
            self.disconnect()
    
    def get_grades_by_msv(self, msv: str) -> Tuple[bool, str, pd.DataFrame]:
        """
        Lấy điểm của sinh viên theo MSV
        
        Args:
            msv: Mã số sinh viên
            
        Returns:
            Tuple[bool, str, pd.DataFrame]: (success, message, dataframe)
        """
        if not self.connect():
            return False, "Không thể kết nối đến database", pd.DataFrame()
        
        try:
            query = """
            SELECT 
                s.MSV, s.Ho, s.Ten, s.Lop,
                g.CC, g.KT1, g.KT2, g.KDT,
                g.Subject, g.Semester, g.Year,
                g.CreatedDate
            FROM Students s
            INNER JOIN Grades g ON s.StudentID = g.StudentID
            WHERE s.MSV = ?
            ORDER BY g.CreatedDate DESC
            """
            
            df = pd.read_sql(query, self.connection, params=[msv])
            return True, f"Đã lấy {len(df)} bản ghi điểm", df
            
        except pyodbc.Error as e:
            error_msg = f"Lỗi lấy điểm sinh viên: {str(e)}"
            self.logger.error(error_msg)
            return False, error_msg, pd.DataFrame()
        finally:
            self.disconnect()
    
    def __del__(self):
        """Destructor - đảm bảo ngắt kết nối khi object bị hủy"""
        self.disconnect()
