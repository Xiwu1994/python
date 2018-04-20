create external table if not exists `ods_mongo.ods_beeper_beeper2__subsidy_by_checkins`(
  `subsidy` string comment '',
  `city` string comment '',
  `__v` bigint comment '',
  `cts` timestamp comment '',
)
comment "xxx"
partitioned by(p_day string)
stored as orc ;