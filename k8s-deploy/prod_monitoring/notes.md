# k8s metrics and queries 

This is copied from the google cloud console, cluster observability dashboard. 

https://console.cloud.google.com/kubernetes/clusters/details/europe-west2-a/tilde-cluster/observability?project=umuzi-prod&pageState=(%22nav%22:(%22section%22:%22cpu%22))

## CPU Request % Used (Top 5 Namespaces)  

```MQL

fetch k8s_container
| filter
    resource.project_id == "umuzi-prod"
&& resource.cluster_name == "tilde-cluster"
&& resource.location == "europe-west2-a"
| { metric kubernetes.io/container/cpu/core_usage_time
     | rate
     | every 1m
     | align next_older(2m);
    metric kubernetes.io/container/cpu/request_cores
     | align next_older(2m)
  }
| group_by [resource.namespace_name], .sum()
| outer_join 0
| div
| top 5
| scale "%"
```


## Memory Request % Used (Top 5 Namespaces) 

```mql

fetch k8s_container
| filter
    resource.project_id == "umuzi-prod"
&& resource.cluster_name == "tilde-cluster"
&& resource.location == "europe-west2-a"
| {
    metric kubernetes.io/container/memory/used_bytes;
    metric kubernetes.io/container/memory/request_bytes
  }
| align next_older(2m)
| group_by [resource.namespace_name], .sum()
| outer_join 0
| div
| top 5
| scale "%"

```

## Container Restarts/Min. (Top 5 Namespaces) 

```json


  {"xyChart": {
    "dataSets": [
      {
        "legendTemplate": "${resource.labels.namespace_name}",
        "plotType": "LINE",
        "targetAxis": "Y1",
        "timeSeriesQuery": {
          "apiSource": "DEFAULT_CLOUD",
          "timeSeriesFilter": {
            "aggregation": {
              "alignmentPeriod": "60s",
              "crossSeriesReducer": "REDUCE_SUM",
              "groupByFields": [
                "resource.namespace_name"
              ],
              "perSeriesAligner": "ALIGN_DELTA"
            },
            "filter": "resource.type=\"k8s_container\" resource.label.project_id=\"umuzi-prod\" resource.label.cluster_name=\"tilde-cluster\" metric.type=\"kubernetes.io/container/restart_count\"",
            "pickTimeSeriesFilter": {
              "direction": "TOP",
              "numTimeSeries": 5,
              "rankingMethod": "METHOD_MAX"
            },
            "secondaryAggregation": {
              "alignmentPeriod": "60s",
              "crossSeriesReducer": "REDUCE_NONE",
              "perSeriesAligner": "ALIGN_MEAN"
            }
          }
        }
      }
    ]
  }
}

```

## Pod Warning Events (Top 5 Namespaces) 

```mql

fetch k8s_pod
| metric 'logging.googleapis.com/log_entry_count'
| filter
    resource.project_id == '129011911914'
    && (resource.cluster_name == 'tilde-cluster')
    &&
    (metric.log == 'events'
     && metric.severity =~ 'WARNING|ERROR|CRITICAL|ALERT|EMERGENCY')
| align delta(1m)
| every 1m
| group_by [resource.namespace_name],
    [value_log_entry_count_aggregate: aggregate(value.log_entry_count)]

```

## Container Error Logs/Sec. (Top 5 Namespaces)

```mql

fetch k8s_container
| metric 'logging.googleapis.com/log_entry_count'
| filter
    resource.project_id == '129011911914'
    && (resource.cluster_name == 'tilde-cluster')
    && (metric.severity =~ 'ERROR|CRITICAL|ALERT|EMERGENCY')
| align rate(1m)
| every 1m
| group_by [resource.namespace_name],
    [value_log_entry_count_aggregate: aggregate(value.log_entry_count)]

```

## Ephemeral Storage % Used 

```mql
fetch k8s_node
| filter
    resource.project_id == "umuzi-prod"
&& resource.cluster_name == "tilde-cluster"
&& resource.location == "europe-west2-a"
| { metric kubernetes.io/node/ephemeral_storage/used_bytes
| every 1m
| align next_older(2m)
; metric kubernetes.io/node/ephemeral_storage/allocatable_bytes
| every 1m
| align next_older(2m) }
| group_by [resource.cluster_name], .sum()
| ratio
| scale "%"
```

kubernetes.io:node-ephemeral_storage-used_bytes
kubernetes_io:node-ephemeral_storage-allocatable_bytes
container_ephemeral_storage_used_bytes

## Other things...

node/cpu/allocatable_utilization GA
The fraction of the allocatable CPU that is currently in use on the instance. Sampled every 60 seconds. After sampling, data is not visible for up to 240 seconds.


node/memory/allocatable_utilization

sum by (pod_name) (kubernetes_io:container_memory_used_bytes/(1024*1024))