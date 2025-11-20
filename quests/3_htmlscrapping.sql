-- ======================================
-- CREATE TABLE
-- ======================================
CREATE TABLE scraping_html_results (
    id INT PRIMARY KEY,
    page_title VARCHAR(500),
    page_url VARCHAR(500),
    html_length INT,
    status_code INT
);

-- ======================================
-- INSERT — 데이터 3개 추가
-- ======================================
INSERT INTO scraping_html_results (id, page_title, page_url, html_length, status_code)
VALUES
(1, '홈페이지', 'https://site.com', 15700, 200),
(2, '블로그', 'https://blog.com', 9800, 200),
(3, '404 페이지', 'https://site.com/notfound', 0, 404);

-- ======================================
-- SELECT — status_code가 200인 페이지만 조회
-- ======================================
SELECT *
FROM scraping_html_results
WHERE status_code = 200;

-- ======================================
-- UPDATE — "블로그" html_length = 12000
-- ======================================
UPDATE scraping_html_results
SET html_length = 12000
WHERE id = 2;

-- ======================================
-- DELETE — status_code가 404인 데이터 삭제
-- ======================================
DELETE FROM scraping_html_results
WHERE status_code = 404;
