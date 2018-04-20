create external table if not exists `ods_mongo.ods_beeper_beeper2__customer_checkin_dates`(
  `date` string comment '',
  `cuid` bigint comment '',
)
comment "xxx"
partitioned by(p_day string)
stored as orc ;