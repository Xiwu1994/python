create external table if not exists `ods_mongo.ods_beeper_beeper2__field_control_clerks_tasks`(
  `lid` bigint comment '',
  `wid` bigint comment '',
  `cts` timestamp comment '',
  `did` bigint comment '',
  `fccid` bigint comment '',
  `check_in_st` bigint comment '',
  `pcid` bigint comment '',
  `e_wh_arrival_hm` string comment '',
  `__v` bigint comment '',
  `ftid` bigint comment '',
  `cuid` bigint comment '',
  `date` string comment '',
  `check_in_ts` timestamp comment '',
)
comment "xxx"
partitioned by(p_day string)
stored as orc ;