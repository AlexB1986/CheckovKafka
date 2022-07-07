# CheckovKafka
Custom Checkov policy to check Kafka configurations generated based on [Kafka Helm charts by Bitnami
](https://github.com/bitnami/charts/tree/master/bitnami/kafka)

## Usefull commands

Helm commands to get and render templates on local machine
```sh
helm repo add bitnami https://charts.bitnami.com/bitnami
helm pull --untar bitnami/kafka
helm template --output-dir ./yamls ./kafka
```

Checkov commands
```sh
checkov -d ./kafka --framework helm -c CKV_KAFKA_1 --external-checks-dir ./KafkaPolicy
```