/*
    author: cg
    time: 2017-12-14
    description: 获取规定之间内所有(出了578)使用了设备的校区的图片到达率
*/

SELECT
  htg_org.id AS 'org_id',
  htg_org.NAME AS 'org_name',
  htg_shop.id AS 'shop_id',
  htg_shop.NAME AS 'shop_name',
  pic_to_ed AS 'pic_to_ed',
  pic_to_all AS 'pic_to_all',
  (pic_to_all - pic_to_ed) AS 'pic_to_not',
  pic_to_ed/pic_to_all*100 AS rate

FROM
  (
  SELECT
    org_id,
    shop_id,
    SUM( htg_sign_pic_tmp_1.pic_url_ii ) AS pic_to_ed,
    count( htg_sign_pic_tmp_1.org_id ) AS pic_to_all 
  FROM
    (
    SELECT
      org_id,
      shop_id,
    IF
      ( pic_url IS NULL, 0, 1 ) AS pic_url_ii 
    FROM
      htg_sign_pic 
    WHERE
      append_time >= %d
      AND append_time <= %d
      AND  shop_id != 578
    ) htg_sign_pic_tmp_1 
  GROUP BY
    htg_sign_pic_tmp_1.org_id,
    htg_sign_pic_tmp_1.shop_id 
  ) htg_sign_pic_tmp_2
  LEFT JOIN htg_org ON htg_org.id = htg_sign_pic_tmp_2.org_id
LEFT JOIN htg_shop ON htg_shop.id = htg_sign_pic_tmp_2.shop_id
ORDER BY rate;