create external table if not exists `ods_mongo.ods_beeper_beeper_vehicle_routing__routing_logs`(
  `solution_text` string comment '',
  `requested_at` timestamp comment '',
  `problem_text` string comment '',
  `solution` string comment '',
  `solved_at` timestamp comment '',
  `correlation_id` string comment '',
  `reply_to` string comment '',
  `problem` string comment '',
)
comment "xxx"
partitioned by(p_day string)
stored as orc ;