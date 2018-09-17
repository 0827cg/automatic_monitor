/*
    author: cg
    time: 2018-04-24
    description: 获取规定时间内食谱项中上传了的图片总数
*/
/*
SELECT
	ROUND(sum((LENGTH(files)-LENGTH(replace(files,'http', ''))) / 4),0) AS foodPicNum
FROM
	htg_record
WHERE
	appendtime > 1537113600
AND appendtime <= 1537151171
AND effect = 1
AND active = 1
AND tags is not null
*/

SELECT
	ROUND(sum((LENGTH(files)-LENGTH(replace(files,'http', ''))) / 4),0) AS foodPicNum
FROM
	htg_cookbook_record
WHERE
	pre_insert_time > %d
AND pre_insert_time <= %d
AND effect = 1
AND active = 1