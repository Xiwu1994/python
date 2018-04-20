create external table if not exists `ods_mongo.ods_beeper_beeper2__to_customer_feedbacks`(
  `comment` string comment '',
  `fdid` bigint comment '',
  `cts` timestamp comment '',
  `driver` string comment '',
  `st` bigint comment '',
  `customer` string comment '',
  `__v` bigint comment '',
  `fdts` timestamp comment '',
  `type` bigint comment '',
)
comment "xxx"
partitioned by(p_day string)
stored as orc ;