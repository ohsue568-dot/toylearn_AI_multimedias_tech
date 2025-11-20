-- ======================================
-- CREATE TABLE
-- (row 식별용 id 컬럼 포함)
-- ======================================
CREATE TABLE web_links (
    id INT PRIMARY KEY,
    link_text VARCHAR(500),
    link_url VARCHAR(500),
    category VARCHAR(500)
);

-- ======================================
-- INSERT — 데이터 3개 추가
-- ======================================
INSERT INTO web_links (id, link_text, link_url, category)
VALUES
(1, '네이버', 'https://naver.com', 'portal'),
(2, '구글', 'https://google.com', 'portal'),
(3, '깃허브', 'https://github.com', 'dev');

-- ======================================
-- SELECT — category가 "portal"인 링크 조회
-- ======================================
SELECT *
FROM web_links
WHERE category = 'portal';

-- ======================================
-- UPDATE — "깃허브" category를 "code"로 변경
-- ======================================
UPDATE web_links
SET category = 'code'
WHERE id = 3;

-- ======================================
-- DELETE — "네이버" 데이터 삭제
-- ======================================
DELETE FROM web_links
WHERE id = 1;

-- 완료
