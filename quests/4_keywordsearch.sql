-- ======================================
-- CREATE TABLE
-- ======================================
CREATE TABLE keyword_search_logs (
    id INT PRIMARY KEY,
    keyword VARCHAR(500),
    result_count INT,
    search_time VARCHAR(500)
);

-- ======================================
-- INSERT — 데이터 3개 추가
-- ======================================
INSERT INTO keyword_search_logs (id, keyword, result_count, search_time)
VALUES
(1, 'python', 120, '2025-11-19 10:00:00'),
(2, 'chatgpt', 300, '2025-11-19 10:05:00'),
(3, 'docker', 90, '2025-11-19 10:10:00');

-- ======================================
-- SELECT — result_count가 100 이상
-- ======================================
SELECT *
FROM keyword_search_logs
WHERE result_count >= 100;

-- ======================================
-- UPDATE — "docker" result_count = 150
-- ======================================
UPDATE keyword_search_logs
SET result_count = 150
WHERE id = 3;

-- ======================================
-- DELETE — "python" 로그 삭제
-- ======================================
DELETE FROM keyword_search_logs
WHERE id = 1;
