CREATE EXTERNAL TABLE `steptrainer_trusted`(
  `serialnumber` string COMMENT 'from deserializer', 
  `sensorreadingtime` bigint COMMENT 'from deserializer', 
  `distancefromobject` bigint COMMENT 'from deserializer')
ROW FORMAT SERDE 
  'org.openx.data.jsonserde.JsonSerDe' 
STORED AS INPUTFORMAT 
  'org.apache.hadoop.mapred.TextInputFormat' 
OUTPUTFORMAT 
  'org.apache.hadoop.hive.ql.io.HiveIgnoreKeyTextOutputFormat'
LOCATION
  's3://sparkling-lakes/steptrainer/trusted/'
TBLPROPERTIES (
  'CreatedByJob'='steptrainer_landing_to_trusted', 
  'CreatedByJobRun'='jr_ef80f64275de9ec76688f1263c853aa06e7e4bad33b92e2131064f96522e74a9', 
  'classification'='json')