CREATE EXTERNAL TABLE `machine_learning_curated`(
  `serialnumber` string COMMENT 'from deserializer', 
  `z` double COMMENT 'from deserializer', 
  `timestamp` bigint COMMENT 'from deserializer', 
  `y` double COMMENT 'from deserializer', 
  `user` string COMMENT 'from deserializer', 
  `x` double COMMENT 'from deserializer', 
  `distancefromobject` int COMMENT 'from deserializer')
ROW FORMAT SERDE 
  'org.openx.data.jsonserde.JsonSerDe' 
STORED AS INPUTFORMAT 
  'org.apache.hadoop.mapred.TextInputFormat' 
OUTPUTFORMAT 
  'org.apache.hadoop.hive.ql.io.HiveIgnoreKeyTextOutputFormat'
LOCATION
  's3://sparkling-lakes/machinelearning/curated/'
TBLPROPERTIES (
  'CreatedByJob'='machine_learning_trusted_to_curated', 
  'CreatedByJobRun'='jr_7aebc7c8ce34b18ea6d65778b334eb0ef8c37c790ea28ca650f4d99cdd018816', 
  'classification'='json')