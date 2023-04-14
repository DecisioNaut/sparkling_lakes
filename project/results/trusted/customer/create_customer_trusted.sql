CREATE EXTERNAL TABLE `customer_trusted`(
  `serialnumber` string COMMENT 'from deserializer', 
  `sharewithpublicasofdate` bigint COMMENT 'from deserializer', 
  `birthday` string COMMENT 'from deserializer', 
  `registrationdate` bigint COMMENT 'from deserializer', 
  `sharewithresearchasofdate` bigint COMMENT 'from deserializer', 
  `customername` string COMMENT 'from deserializer', 
  `email` string COMMENT 'from deserializer', 
  `lastupdatedate` bigint COMMENT 'from deserializer', 
  `phone` string COMMENT 'from deserializer', 
  `sharewithfriendsasofdate` bigint COMMENT 'from deserializer')
ROW FORMAT SERDE 
  'org.openx.data.jsonserde.JsonSerDe' 
STORED AS INPUTFORMAT 
  'org.apache.hadoop.mapred.TextInputFormat' 
OUTPUTFORMAT 
  'org.apache.hadoop.hive.ql.io.HiveIgnoreKeyTextOutputFormat'
LOCATION
  's3://sparkling-lakes/customer/trusted/'
TBLPROPERTIES (
  'CreatedByJob'='customer_landing_to_trusted', 
  'CreatedByJobRun'='jr_7825fecb49c307a4a8bad670c7596a00874124e9f8114d1a9b588311477e4e8e', 
  'classification'='json')