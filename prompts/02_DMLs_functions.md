```
{
  "task": "PostgreSQL 연동 Python 함수 작성",
  "goal": "문제 1~5 요구사항에 맞춰 books 테이블 생성, INSERT, SELECT, UPDATE, DELETE 기능을 구현한 Python 코드를 작성하라.",
  "requirements": {
    "database": "PostgreSQL",
    "table_name": "books",
    "table_columns": {
      "id": "UUID PRIMARY KEY DEFAULT uuid_generate_v4()",
      "title": "VARCHAR(100)",
      "price": "INT"
    },
    "functions": [
      {
        "name": "create_books_table",
        "description": "books 테이블을 생성하는 Python 함수",
        "expected_output": "books 테이블이 생성되었습니다."
      },
      {
        "name": "insert_books",
        "description": "주어진 테스트 데이터를 INSERT하는 함수 (id는 자동 생성)",
        "test_data": [
          {"title": "파이썬 입문", "price": 19000},
          {"title": "알고리즘 기초", "price": 25000},
          {"title": "네트워크 이해", "price": 30000}
        ],
        "expected_output": "3개 도서가 삽입되었습니다."
      },
      {
        "name": "get_all_books",
        "description": "전체 도서 목록 조회 함수"
      },
      {
        "name": "get_expensive_books",
        "description": "가격이 25000원 이상인 도서 조회 함수"
      },
      {
        "name": "get_book_by_title",
        "params": ["title"],
        "description": "특정 title에 해당하는 도서 조회"
      },
      {
        "name": "update_second_book_price",
        "description": "저장된 순서 두 번째 도서의 가격을 27000으로 수정",
        "expected_output": "두 번째 도서 가격이 27000으로 수정되었습니다."
      },
      {
        "name": "delete_third_book",
        "description": "저장된 순서 세 번째 도서 삭제",
        "expected_output": "세 번째 도서가 삭제되었습니다."
      }
    ]
  },
  "additional_instructions": [
    "SQL 실행 시 필요한 커넥션 코드(psycopg2 등) 포함",
    "각 함수는 try-except로 구성",
    "중요 SQL 실행 부분은 print로 확인 가능하게 작성"
  ]
}
```

