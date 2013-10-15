curl -XPUT 'localhost:9200/uber' -d'
{
   "settings" : {
     "number_of_shards" : 1,
     "number_of_replicas" : 0,
     "_timestamp" : {
         "enabled" : true
     }

   }
}'

curl -XPUT 'http://localhost:9200/uber/trips/_mapping' -d '
{
  "trips": {
    "properties" : {
       "location" : {
         "type":"geo_point",
         "lat_lon" : true
       },
       "fare" : {
           "type" : "float",
           "null_value" : 0.0
       }
     }
  }
}'

