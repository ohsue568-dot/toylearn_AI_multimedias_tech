-- ======================================
-- CREATE TABLE
-- ======================================
CREATE TABLE shop_products (
    id INT PRIMARY KEY,
    name VARCHAR(500),
    price INT,
    stock INT,
    category VARCHAR(500)
);

-- ======================================
-- INSERT — 데이터 추가
-- ======================================
INSERT INTO shop_products (id, name, price, stock, category)
VALUES
(1, 'USB 메모리', 12000, 50, '전자제품'),
(2, '블루투스 스피커', 45000, 20, '전자제품'),
(3, '물병', 5000, 100, '생활용품');

-- ======================================
-- SELECT — price가 10000 이상 조회
-- ======================================
SELECT *
FROM shop_products
WHERE price >= 10000;

-- ======================================
-- UPDATE — "물병" stock = 80
-- ======================================
UPDATE shop_products
SET stock = 80
WHERE id = 3;

-- ======================================
-- DELETE — "블루투스 스피커" 삭제
-- ======================================
DELETE FROM shop_products
WHERE id = 2;
