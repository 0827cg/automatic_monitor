/*

-- 这个sql是获取积分使用详情,所有校区及各校区使用积分数

SELECT
	htg_integral_user_relation.org_id,
	htg_integral_user_relation.shop_id,
	htg_org.`name` AS org_name,
	htg_shop.`name` AS shop_name,
	count AS integralSit
FROM
	(
		SELECT
			org_id,
			shop_id,
			COUNT(id) AS count
		FROM
			htg_integral_user_relation
		WHERE
			append_time >= 1524499200
		AND append_time <= 1524574861
		GROUP BY
			org_id,
			shop_id
		ORDER BY
			count DESC
	) htg_integral_user_relation
LEFT JOIN htg_org ON htg_org.id = htg_integral_user_relation.org_id
LEFT JOIN htg_shop ON htg_shop.id = htg_integral_user_relation.shop_id;

*/

/*
    author: cg
    time: 2018-04-25
    description: 获取积分使用情况

	totalShopNum: 在规定时间内使用了积分的校区总数
	totalIntegralNum: 在规定时间内所有校区使用的积分总数
*/

SELECT
	count(htg_integral_user_relation.shop_id) AS totalShopNum,
	SUM(count) AS totalIntegralNum
FROM
	(
		SELECT
			org_id,
			shop_id,
			COUNT(id) AS count
		FROM
			htg_integral_user_relation
		WHERE
			append_time >= %d
		AND append_time <= %d
		GROUP BY
			org_id,
			shop_id
		ORDER BY
			count DESC
	) htg_integral_user_relation
LEFT JOIN htg_org ON htg_org.id = htg_integral_user_relation.org_id
LEFT JOIN htg_shop ON htg_shop.id = htg_integral_user_relation.shop_id;