import psycopg2
from psycopg2 import sql
import os
from uuid import UUID

# --- ⚠️ 데이터베이스 접속 정보 설정 ⚠️ ---
# 실제 환경에 맞게 정보를 수정하세요.
DB_NAME = "your_db_name"
DB_USER = "your_db_user"
DB_PASSWORD = "your_db_password"
DB_HOST = "localhost" # 또는 실제 DB 호스트 IP
DB_PORT = "5432"

TABLE_NAME = "books"

# 헬퍼 함수: 데이터베이스 연결 설정
def get_db_connection():
    """데이터베이스 연결 객체를 반환합니다."""
    try:
        conn = psycopg2.connect(
            dbname=DB_NAME,
            user=DB_USER,
            password=DB_PASSWORD,
            host=DB_HOST,
            port=DB_PORT
        )
        return conn
    except Exception as e:
        print(f"❌ 데이터베이스 연결 실패: {e}")
        return None

# 1. books 테이블 생성 함수
def create_books_table():
    """books 테이블을 생성합니다."""
    conn = get_db_connection()
    if conn is None:
        return

    # UUID 확장을 위한 SQL (PostgreSQL에서 UUID 기본값 설정을 위해 필요)
    sql_create_extension = "CREATE EXTENSION IF NOT EXISTS \"uuid-ossp\""
    
    # books 테이블 생성 SQL
    sql_create_table = f"""
    CREATE TABLE IF NOT EXISTS {TABLE_NAME} (
        id UUID PRIMARY KEY DEFAULT uuid_generate_v4(),
        title VARCHAR(100) NOT NULL,
        price INT NOT NULL
    )
    """
    
    try:
        with conn.cursor() as cur:
            print(f"➡️ SQL 실행: {sql_create_extension}")
            cur.execute(sql_create_extension)
            
            print(f"➡️ SQL 실행: {sql_create_table.strip()}")
            cur.execute(sql_create_table)
            
            conn.commit()
            print("✅ books 테이블이 생성되었습니다.")
            
    except Exception as e:
        conn.rollback()
        print(f"❌ 테이블 생성 중 오류 발생: {e}")
    finally:
        if conn:
            conn.close()

# 2. 도서 데이터 삽입 함수
def insert_books(data):
    """주어진 테스트 데이터를 books 테이블에 삽입합니다."""
    conn = get_db_connection()
    if conn is None:
        return

    sql_insert = sql.SQL(
        "INSERT INTO {table} (title, price) VALUES (%s, %s)"
    ).format(table=sql.Identifier(TABLE_NAME))
    
    try:
        with conn.cursor() as cur:
            count = 0
            for item in data:
                title = item['title']
                price = item['price']
                
                print(f"➡️ SQL 실행: {sql_insert.as_string(conn)} with ('{title}', {price})")
                cur.execute(sql_insert, (title, price))
                count += 1
            
            conn.commit()
            print(f"✅ {count}개 도서가 삽입되었습니다.")
            
    except Exception as e:
        conn.rollback()
        print(f"❌ 데이터 삽입 중 오류 발생: {e}")
    finally:
        if conn:
            conn.close()

# 3. 전체 도서 목록 조회 함수
def get_all_books():
    """전체 도서 목록을 조회합니다."""
    conn = get_db_connection()
    if conn is None:
        return []

    sql_select = f"SELECT id, title, price FROM {TABLE_NAME} ORDER BY title"
    results = []

    try:
        with conn.cursor() as cur:
            print(f"➡️ SQL 실행: {sql_select}")
            cur.execute(sql_select)
            results = cur.fetchall()
            
            print(f"✅ 전체 도서 목록 ({len(results)}개):")
            for book in results:
                print(f"   ID: {book[0]}, 제목: {book[1]}, 가격: {book[2]}원")
            
    except Exception as e:
        print(f"❌ 전체 도서 조회 중 오류 발생: {e}")
    finally:
        if conn:
            conn.close()
    return results

# 4. 가격이 25000원 이상인 도서 조회 함수
def get_expensive_books():
    """가격이 25000원 이상인 도서 목록을 조회합니다."""
    conn = get_db_connection()
    if conn is None:
        return []

    sql_select = f"SELECT id, title, price FROM {TABLE_NAME} WHERE price >= 25000 ORDER BY price DESC"
    results = []

    try:
        with conn.cursor() as cur:
            print(f"➡️ SQL 실행: {sql_select}")
            cur.execute(sql_select)
            results = cur.fetchall()
            
            print(f"✅ 가격 25000원 이상 도서 목록 ({len(results)}개):")
            for book in results:
                print(f"   ID: {book[0]}, 제목: {book[1]}, 가격: {book[2]}원")
            
    except Exception as e:
        print(f"❌ 고가 도서 조회 중 오류 발생: {e}")
    finally:
        if conn:
            conn.close()
    return results

# 5. 특정 title에 해당하는 도서 조회 함수
def get_book_by_title(title):
    """특정 제목에 해당하는 도서를 조회합니다."""
    conn = get_db_connection()
    if conn is None:
        return None

    sql_select = f"SELECT id, title, price FROM {TABLE_NAME} WHERE title = %s"
    result = None

    try:
        with conn.cursor() as cur:
            print(f"➡️ SQL 실행: {sql_select} with ('{title}')")
            cur.execute(sql_select, (title,))
            result = cur.fetchone()
            
            if result:
                print(f"✅ 제목 '{title}' 도서: ID: {result[0]}, 가격: {result[2]}원")
            else:
                print(f"ℹ️ 제목 '{title}'에 해당하는 도서가 없습니다.")
            
    except Exception as e:
        print(f"❌ 특정 도서 조회 중 오류 발생: {e}")
    finally:
        if conn:
            conn.close()
    return result

# 6. 저장된 순서 두 번째 도서의 가격을 27000으로 수정
def update_second_book_price():
    """저장된 순서 두 번째 도서의 가격을 27000으로 수정합니다."""
    conn = get_db_connection()
    if conn is None:
        return

    # 첫 번째로, 저장된 순서(id 순)로 두 번째 도서의 id를 조회합니다.
    sql_select_id = f"SELECT id FROM {TABLE_NAME} ORDER BY id LIMIT 1 OFFSET 1"
    
    try:
        with conn.cursor() as cur:
            print(f"➡️ SQL 실행 (ID 조회): {sql_select_id}")
            cur.execute(sql_select_id)
            second_book_id_row = cur.fetchone()
            
            if not second_book_id_row:
                print("❌ 테이블에 두 번째 도서가 없습니다.")
                return

            second_book_id = second_book_id_row[0]
            
            # 두 번째로, 해당 id를 사용하여 가격을 업데이트합니다.
            new_price = 27000
            sql_update = f"UPDATE {TABLE_NAME} SET price = %s WHERE id = %s"
            
            print(f"➡️ SQL 실행 (업데이트): {sql_update} with ({new_price}, '{second_book_id}')")
            cur.execute(sql_update, (new_price, second_book_id))
            
            if cur.rowcount > 0:
                conn.commit()
                print(f"✅ 두 번째 도서 (ID: {second_book_id}) 가격이 {new_price}으로 수정되었습니다.")
            else:
                conn.rollback()
                print("❌ 가격 수정 실패 (해당 ID 도서 없음).")
            
    except Exception as e:
        conn.rollback()
        print(f"❌ 가격 수정 중 오류 발생: {e}")
    finally:
        if conn:
            conn.close()

# 7. 저장된 순서 세 번째 도서 삭제
def delete_third_book():
    """저장된 순서 세 번째 도서를 삭제합니다."""
    conn = get_db_connection()
    if conn is None:
        return

    # 첫 번째로, 저장된 순서(id 순)로 세 번째 도서의 id를 조회합니다.
    sql_select_id = f"SELECT id FROM {TABLE_NAME} ORDER BY id LIMIT 1 OFFSET 2"
    
    try:
        with conn.cursor() as cur:
            print(f"➡️ SQL 실행 (ID 조회): {sql_select_id}")
            cur.execute(sql_select_id)
            third_book_id_row = cur.fetchone()
            
            if not third_book_id_row:
                print("❌ 테이블에 세 번째 도서가 없습니다.")
                return

            third_book_id = third_book_id_row[0]
            
            # 두 번째로, 해당 id를 사용하여 도서를 삭제합니다.
            sql_delete = f"DELETE FROM {TABLE_NAME} WHERE id = %s"
            
            print(f"➡️ SQL 실행 (삭제): {sql_delete} with ('{third_book_id}')")
            cur.execute(sql_delete, (third_book_id,))
            
            if cur.rowcount > 0:
                conn.commit()
                print(f"✅ 세 번째 도서 (ID: {third_book_id})가 삭제되었습니다.")
            else:
                conn.rollback()
                print("❌ 도서 삭제 실패 (해당 ID 도서 없음).")
            
    except Exception as e:
        conn.rollback()
        print(f"❌ 도서 삭제 중 오류 발생: {e}")
    finally:
        if conn:
            conn.close()

# --- 테스트 실행 ---
if __name__ == "__main__":
    
    # ⚠️ 반드시 DB 접속 정보를 먼저 수정하세요!
    print("="*40)
    print("=== PostgreSQL Python 연동 테스트 시작 ===")
    print("="*40)

    # 1. 테이블 생성
    print("\n[1. books 테이블 생성]")
    create_books_table()

    # 테스트 데이터
    test_data = [
        {"title": "파이썬 입문", "price": 19000},
        {"title": "알고리즘 기초", "price": 25000},
        {"title": "네트워크 이해", "price": 30000}
    ]

    # 2. 데이터 삽입
    print("\n[2. 테스트 데이터 삽입]")
    insert_books(test_data)

    # 3. 전체 도서 목록 조회
    print("\n[3. 전체 도서 목록 조회]")
    get_all_books()

    # 4. 가격 25000원 이상 도서 조회
    print("\n[4. 가격 25000원 이상 도서 조회]")
    get_expensive_books()

    # 5. 특정 제목 도서 조회
    print("\n[5. 특정 제목 도서 조회: '파이썬 입문']")
    get_book_by_title("파이썬 입문")
    
    print("\n[5. 특정 제목 도서 조회: '클라우드 컴퓨팅' (없는 도서)]")
    get_book_by_title("클라우드 컴퓨팅")

    # 6. 두 번째 도서 가격 수정
    print("\n[6. 두 번째 도서 가격 수정 (-> 27000)]")
    update_second_book_price()
    
    # 수정 후 전체 조회로 확인
    print("\n[6-1. 수정 후 전체 도서 목록 조회 (확인)]")
    get_all_books()

    # 7. 세 번째 도서 삭제
    print("\n[7. 세 번째 도서 삭제]")
    delete_third_book()
    
    # 삭제 후 전체 조회로 확인
    print("\n[7-1. 삭제 후 전체 도서 목록 조회 (확인)]")
    get_all_books()
    
    print("\n="*40)
    print("=== PostgreSQL Python 연동 테스트 완료 ===")
    print("="*40)