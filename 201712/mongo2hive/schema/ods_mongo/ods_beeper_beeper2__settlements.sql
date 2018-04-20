create external table if not exists `ods_mongo.ods_beeper_beeper2__settlements`(
  `cts` timestamp comment '',
  `money` bigint comment '',
  `st` bigint comment '',
  `__v` bigint comment '',
  `t` bigint comment '',
  `cids` string comment '',
)
comment "xxx"
partitioned by(p_day string)
stored as orc ;