create external table if not exists `ods_mongo.ods_beeper_beeper2__admin_urge_drivers`(
  `cts` timestamp comment '',
  `udid` bigint comment '',
  `dd` string comment '',
  `did` bigint comment '',
  `__v` bigint comment '',
  `tid` bigint comment '',
  `id` bigint comment '',
)
comment "xxx"
partitioned by(p_day string)
stored as orc ;