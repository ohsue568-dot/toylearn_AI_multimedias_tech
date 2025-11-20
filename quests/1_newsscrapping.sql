-- ===============================
-- CREATE TABLE
-- ===============================
CREATE TABLE news_articles (
    id INT PRIMARY KEY,
    title VARCHAR(500),
    url VARCHAR(500),
    author VARCHAR(500),
    published_at VARCHAR(500)
);

-- ===============================
-- INSERT
-- ===============================
INSERT INTO news_articles (id, title, url, author, published_at)
VALUES
(1, 'AI 시대 도래', 'https://news.com/ai', '홍길동', '2025-01-01'),
(2, '경제 성장률 상승', 'https://news.com/economy', '이영희', '2025-01-05');

-- ===============================
-- SELECT
-- ===============================
SELECT *
FROM news_articles
WHERE author = '홍길동';

-- ===============================
-- UPDATE
-- ===============================
UPDATE news_articles
SET title = 'AI 혁신의 시작'
WHERE id = 1;

-- ===============================
-- DELETE
-- ===============================
DELETE FROM news_articles
WHERE id = 2;

-- 완료
