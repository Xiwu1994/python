create external table if not exists `ods_mongo.ods_beeper_beeper2__subsidy_by_cartypes`(
  `city` string comment '',
  `cts` timestamp comment '',
  `sp` double comment '',
  `st` bigint comment '',
  `__v` bigint comment '',
  `sid` bigint comment '',
  `entry` string comment '',
  `ctid` bigint comment '',
  `desc` string comment '',
)
comment "xxx"
partitioned by(p_day string)
stored as orc ;