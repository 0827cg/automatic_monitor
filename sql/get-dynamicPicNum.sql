/*
    author: cg
    time: 2018-04-24
    description: 获取规定时间内动态项中上传了的图片总数
*/

SELECT
	ROUND(sum((LENGTH(files)-LENGTH(replace(files,'http', ''))) / 4),0) AS dynamicPicNum
FROM
	htg_record
WHERE
	appendtime > %d
AND appendtime <= %d
AND effect = 1
AND active = 1
AND tags is null
