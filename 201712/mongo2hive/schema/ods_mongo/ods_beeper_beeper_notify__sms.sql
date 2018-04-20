create external table if not exists `ods_mongo.ods_beeper_beeper_notify__sms`(
  `templateData` string comment '',
  `created` timestamp comment '',
  `workerId` bigint comment '',
  `templateName` string comment '',
  `platform` string comment '',
  `__v` bigint comment '',
  `isSent` boolean comment '',
  `sendTime` timestamp comment '',
  `sendResult` string comment '',
  `mobiles` string comment '',
)
comment "xxx"
partitioned by(p_day string)
stored as orc ;