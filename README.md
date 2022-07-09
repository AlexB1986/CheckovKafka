# CheckovKafka
Custom [Checkov](https://github.com/bridgecrewio/checkov) policy to check Kafka configurations generated based on [Kafka Helm charts by Bitnami
](https://github.com/bitnami/charts/tree/master/bitnami/kafka)

## Usefull commands

Helm commands to get and render templates on local machine
```sh
helm repo add bitnami https://charts.bitnami.com/bitnami
helm pull --untar bitnami/kafka
helm template --output-dir ./yamls ./kafka
helm template --output-dir ./yamls ./kafka --values ./kafka/values_ACL.yaml 
```

Checkov commands
```sh
checkov -d ./kafka --framework helm -c CKV_KAFKA_1 --external-checks-dir ./KafkaPolicy
```

## Implemented checks

| ID| Type| Entity | Policy| Description | IaC Policy|
| :--- | :--- | :---| :---|:---|:---|
| CKV_KAFKA_1 | resource |StatefulSet| Ensure that allowEveryoneIfNoAclFoundCheck is set to false or unused |If a resource has no associated ACLs and [allow.everyone.if.no.acl.found](https://kafka.apache.org/documentation/#security_authz)=true, then anyone is allowed to access that resource. If `allow.everyone.if.no.acl.found=false`, then no one is allowed to access that resource except super users. Use of the `allow.everyone.if.no.acl.found` configuration option in production environments is strongly [discouraged](https://docs.confluent.io/platform/current/kafka/authorization.html): 1) If you specify this option based on the assumption that you have ACLs, but then your last ACL is deleted, you essentially open up your Kafka clusters to all users; 2) If you’re using this option to disable ACLs, exercise caution: if someone adds an ACL, all the users who previously had access will lose that access.|Kubernetes|
| CKV_KAFKA_2 | resource |StatefulSet| Ensure that pluggable authorizer (ACL) or an out-of-box authorizer implementation is used |Kafka ships with a pluggable Authorizer and an out-of-box authorizer implementation that uses zookeeper to store all the ACLs. The Authorizer is configured by setting [authorizer.class.name](https://kafka.apache.org/documentation/#security_authz). To enable the out of the box implementation you should specify it, e.g. `authorizer.class.name=kafka.security.authorizer.AclAuthorizer`|Kubernetes|
| CKV_KAFKA_3 | resource |StatefulSet| Ensure that ALLOW_PLAINTEXT_LISTENER is set to NO | This settings allows to use the PLAINTEXT listener and should be set to NO|Kubernetes|
