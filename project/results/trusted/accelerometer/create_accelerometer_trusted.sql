CREATE EXTERNAL TABLE `accelerometer_trusted`(
  `z` double COMMENT 'from deserializer', 
  `timestamp` bigint COMMENT 'from deserializer', 
  `user` string COMMENT 'from deserializer', 
  `y` double COMMENT 'from deserializer', 
  `x` double COMMENT 'from deserializer')
ROW FORMAT SERDE 
  'org.openx.data.jsonserde.JsonSerDe' 
STORED AS INPUTFORMAT 
  'org.apache.hadoop.mapred.TextInputFormat' 
OUTPUTFORMAT 
  'org.apache.hadoop.hive.ql.io.HiveIgnoreKeyTextOutputFormat'
LOCATION
  's3://sparkling-lakes/accelerometer/trusted/'
TBLPROPERTIES (
  'CreatedByJob'='accelerometer_landing_to_trusted', 
  'CreatedByJobRun'='jr_981e52eebe26d33853d22f084ad424e2ecc93e66b408c3f057b0dee83d8e39a6', 
  'classification'='json')