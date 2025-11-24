import psycopg2
from psycopg2 import sql
import sys

# ==============================================================================
# ⚠️ PostgreSQL 연결 정보 설정
# 이 값들을 사용자의 PostgreSQL 설정에 맞게 변경해주세요.
# ==============================================================================
DB_HOST = "localhost"
DB_NAME = "your_db_name"  # 데이터베이스 이름으로 변경
DB_USER = "your_db_user"  # 사용자 이름으로 변경
DB_PASSWORD = "your_db_password" # 비밀번호로 변경

def get_db_connection():
    """데이터베이스 연결 객체를 반환합니다."""
    try:
        conn = psycopg2.connect(
            host=DB_HOST,
            database=DB_NAME,
            user=DB_USER,
            password=DB_PASSWORD
        )
        return conn
    except psycopg2.OperationalError as e:
        print(f"ERROR: 데이터베이스 연결 실패. 연결 정보를 확인하세요: {e}")
        # 프로그램 종료를 위해 sys.exit() 사용
        sys.exit(1)

# 📌 문제 1 — 테이블 생성 함수 만들기
def create_books_table():
    """'books' 테이블을 생성합니다. (UUID, title, price)"""
    conn = None
    try:
        conn = get_db_connection()
        cur = conn.cursor()

        # UUID 생성을 위한 extension이 있는지 확인하고 생성합니다.
        cur.execute(sql.SQL('CREATE EXTENSION IF NOT EXISTS "uuid-ossp"'))

        # 테이블이 이미 존재한다면 삭제하여 깨끗한 상태로 시작합니다.
        cur.execute(sql.SQL("DROP TABLE IF EXISTS books;"))

        # books 테이블 생성
        cur.execute(
            sql.SQL("""
                CREATE TABLE books (
                    id UUID PRIMARY KEY DEFAULT uuid_generate_v4(),
                    title VARCHAR(100) NOT NULL,
                    price INT NOT NULL
                );
            """)
        )
        conn.commit()
        print("books 테이블이 생성되었습니다.")

    except Exception as e:
        print(f"테이블 생성 중 오류 발생: {e}")
    finally:
        if conn:
            conn.close()

# 📌 문제 2 — INSERT 함수 만들기
def insert_books():
    """테스트용 데이터를 'books' 테이블에 삽입합니다."""
    books_data = [
        ("파이썬 입문", 19000),
        ("알고리즘 기초", 25000),
        ("네트워크 이해", 30000),
    ]

    conn = None
    try:
        conn = get_db_connection()
        cur = conn.cursor()

        insert_query = sql.SQL("INSERT INTO books (title, price) VALUES (%s, %s)")
        
        # executemany를 사용하여 여러 행을 효율적으로 삽입합니다.
        cur.executemany(insert_query, books_data)
        conn.commit()

        print(f"{cur.rowcount}개 도서가 삽입되었습니다.")

    except Exception as e:
        print(f"데이터 삽입 중 오류 발생: {e}")
    finally:
        if conn:
            conn.close()

# 📌 문제 3 — SELECT 함수 만들기

def print_books_results(title, results):
    """조회 결과를 예쁘게 출력하는 도우미 함수"""
    print(f"\n--- {title} ---")
    if not results:
        print("조회된 데이터가 없습니다.")
        return
    
    # 헤더 출력
    print(f"{'ID (UUID)':<40} | {'Title':<15} | {'Price':>8}")
    print("-" * 68)
    
    # 데이터 출력
    for row in results:
        # UUID는 36자리이므로 출력 공간을 36으로 설정
        print(f"{str(row[0]):<40} | {row[1]:<15} | {row[2]:>8,}")


# 3-1. 전체 조회 함수
def get_all_books():
    """books 테이블의 모든 데이터를 조회합니다."""
    conn = None
    results = []
    try:
        conn = get_db_connection()
        cur = conn.cursor()
        cur.execute(sql.SQL("SELECT id, title, price FROM books ORDER BY title;"))
        results = cur.fetchall()
        print_books_results("전체 도서 목록", results)
    except Exception as e:
        print(f"전체 조회 중 오류 발생: {e}")
    finally:
        if conn:
            conn.close()


# 3-2. 가격이 25000원 이상인 데이터 조회 함수
def get_expensive_books():
    """가격이 25000원 이상인 도서를 조회합니다."""
    conn = None
    results = []
    try:
        conn = get_db_connection()
        cur = conn.cursor()
        cur.execute(sql.SQL("SELECT id, title, price FROM books WHERE price >= 25000 ORDER BY price DESC;"))
        results = cur.fetchall()
        print_books_results("가격 25,000원 이상 도서", results)
    except Exception as e:
        print(f"가격 조회 중 오류 발생: {e}")
    finally:
        if conn:
            conn.close()


# 3-3. title 이 “파이썬 입문”인 데이터 조회 함수
def get_book_by_title(title):
    """특정 title을 가진 도서를 조회합니다."""
    conn = None
    results = []
    try:
        conn = get_db_connection()
        cur = conn.cursor()
        cur.execute(sql.SQL("SELECT id, title, price FROM books WHERE title = %s;"), (title,))
        results = cur.fetchall()
        print_books_results(f"'{title}' 조회 결과", results)
    except Exception as e:
        print(f"제목 조회 중 오류 발생: {e}")
    finally:
        if conn:
            conn.close()


# 📌 문제 4 — UPDATE 함수 만들기
def update_second_book_price():
    """저장된 순서에서 두 번째 도서의 가격을 27000으로 변경합니다."""
    conn = None
    try:
        conn = get_db_connection()
        cur = conn.cursor()

        # 1. 저장된 순서 (INSERT 순서)에서 두 번째 도서의 UUID를 SELECT로 가져옵니다.
        # UUID는 생성된 순서가 비교적 일관되므로 id로 정렬하여 순서를 결정합니다.
        # OFFSET 1은 두 번째 레코드를 의미합니다.
        select_uuid_query = sql.SQL("SELECT id FROM books ORDER BY id LIMIT 1 OFFSET 1;")
        cur.execute(select_uuid_query)
        
        # 단일 UUID 값을 가져옵니다.
        second_book_uuid = cur.fetchone()
        
        if not second_book_uuid:
            print("오류: 두 번째 도서를 찾을 수 없습니다.")
            return

        target_uuid = second_book_uuid[0]

        # 2. 해당 UUID를 사용하여 가격을 27000으로 UPDATE 합니다.
        update_query = sql.SQL("UPDATE books SET price = 27000 WHERE id = %s;")
        cur.execute(update_query, (target_uuid,))
        
        conn.commit()
        
        if cur.rowcount > 0:
            print("\n두 번째 도서 가격이 27000으로 수정되었습니다.")
        else:
            print("\n두 번째 도서 가격 수정에 실패했습니다.")


    except Exception as e:
        print(f"도서 가격 수정 중 오류 발생: {e}")
    finally:
        if conn:
            conn.close()


# 📌 문제 5 — DELETE 함수 만들기
def delete_third_book():
    """저장된 순서에서 세 번째 도서 데이터를 삭제합니다."""
    conn = None
    try:
        conn = get_db_connection()
        cur = conn.cursor()

        # 1. 저장된 순서 (INSERT 순서)에서 세 번째 도서의 UUID를 SELECT로 가져옵니다.
        # OFFSET 2는 세 번째 레코드를 의미합니다.
        select_uuid_query = sql.SQL("SELECT id FROM books ORDER BY id LIMIT 1 OFFSET 2;")
        cur.execute(select_uuid_query)
        
        third_book_uuid = cur.fetchone()
        
        if not third_book_uuid:
            print("오류: 세 번째 도서를 찾을 수 없습니다.")
            return

        target_uuid = third_book_uuid[0]

        # 2. 해당 UUID를 사용하여 도서 데이터를 DELETE 합니다.
        delete_query = sql.SQL("DELETE FROM books WHERE id = %s;")
        cur.execute(delete_query, (target_uuid,))
        
        conn.commit()
        
        if cur.rowcount > 0:
            print("\n세 번째 도서가 삭제되었습니다.")
        else:
            print("\n세 번째 도서 삭제에 실패했습니다.")

    except Exception as e:
        print(f"도서 삭제 중 오류 발생: {e}")
    finally:
        if conn:
            conn.close()


# ==============================================================================
# 메인 실행 블록: 모든 함수를 순서대로 호출
# ==============================================================================
if __name__ == "__main__":
    print("--- PostgreSQL 데이터베이스 작업 시작 ---")
    
    # 문제 1: 테이블 생성
    create_books_table()
    
    # 문제 2: 데이터 삽입
    insert_books()

    print("\n" + "="*75)
    print("문제 3: SELECT 함수 실행")
    print("="*75)

    # 문제 3-1: 전체 조회
    get_all_books()
    
    # 문제 3-2: 가격 25000원 이상 조회
    get_expensive_books()

    # 문제 3-3: 제목으로 조회
    get_book_by_title("파이썬 입문")
    
    print("\n" + "="*75)
    print("문제 4: UPDATE 함수 실행")
    print("="*75)

    # 문제 4: 두 번째 도서 가격 수정 (27000으로)
    update_second_book_price()
    
    # 수정 확인을 위한 전체 조회
    get_all_books()
    
    print("\n" + "="*75)
    print("문제 5: DELETE 함수 실행")
    print("="*75)

    # 문제 5: 세 번째 도서 삭제
    delete_third_book()

    # 삭제 확인을 위한 전체 조회
    get_all_books()
    
    print("\n--- PostgreSQL 데이터베이스 작업 완료 ---")