-- Idempotent: ลบข้อมูลของ logical_date นั้นก่อน แล้ว INSERT ใหม่
DELETE FROM `{project}.{dataset}.daily_transaction_summary`
WHERE CAST(date AS STRING) = '{logical_date}';

INSERT INTO `{project}.{dataset}.daily_transaction_summary`
  (date, transaction_type, user_tier, total_amount, transaction_count)
SELECT
    DATE(t.timestamp)                   AS date,
    t.transaction_type,
    u.user_tier,
    SUM(t.amount)                       AS total_amount,
    COUNT(t.transaction_id)             AS transaction_count
FROM `{project}.{dataset}.stg_raw_transactions` t
LEFT JOIN `{project}.{dataset}.dim_crm_users` u
    ON t.user_id = u.user_id
WHERE t.status = 'Completed'          -- Business Rule: เฉพาะ Completed
    AND u.kyc_status = 'Verified'     -- Risk Rule: เฉพาะ KYC ผ่าน
    AND CAST(DATE(t.timestamp) AS STRING) = '{logical_date}'  -- logical_date filter
GROUP BY 1, 2, 3;
