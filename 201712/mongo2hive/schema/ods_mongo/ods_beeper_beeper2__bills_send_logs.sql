create external table if not exists `ods_mongo.ods_beeper_beeper2__bills_send_logs`(
  `status` bigint comment '',
  `settlement_start_date` timestamp comment '',
  `err` string comment '',
  `settlement_end_date` timestamp comment '',
  `email_title` string comment '',
  `csv_file` string comment '',
  `ts` timestamp comment '',
  `settlement_method` bigint comment '',
  `bslid` bigint comment '',
  `__v` bigint comment '',
  `cuid` bigint comment '',
  `email` string comment '',
)
comment "xxx"
partitioned by(p_day string)
stored as orc ;