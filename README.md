# CheckovKafka
Custom [Checkov](https://github.com/bridgecrewio/checkov) policy to check Kafka configurations generated based on [Kafka Helm charts by Bitnami
](https://github.com/bitnami/charts/tree/master/bitnami/kafka)

## Usefull commands

### Helm commands
Helm commands to get and render templates on local machine
```sh
helm repo add bitnami https://charts.bitnami.com/bitnami
helm pull --untar bitnami/kafka
helm template --output-dir ./yamls ./kafka
helm template --output-dir ./yamls ./kafka --values ./kafka/values_ACL.yaml 
```

### Checkov commands
Checkov command to check template with custom policy
```sh
checkov -d ./kafka --framework helm -c CKV_KAFKA_1 --external-checks-dir ./KafkaPolicy
```

## Testing environment: Kafka on minikube
```sh
minikube start --force # start minikube
helm repo add bitnami https://charts.bitnami.com/bitnami # add repo
helm pull --untar bitnami/kafka # download and untar Kafka chart
```
To expose ports outside use this [guide](https://docs.bitnami.com/kubernetes/infrastructure/kafka/administration/external-access/).
```sh
## values_ext.yaml
...
externalAccess:
 
  enabled: true
....

  service:
 
    type: NodePort
 
...
 
    nodePorts: [30001]
...
```

Start Kafka using Helm and updated values
```sh
kubectl create namespace kafka-system
helm install kafka bitnami/kafka --namespace kafka-system -f ./kafka/values_ext.yaml 
```

Verify that service is exposed:
```sh
>kubectl get svc -n kafka-system
NAME                       TYPE        CLUSTER-IP     EXTERNAL-IP   PORT(S)                      AGE
kafka                      ClusterIP   10.106.78.77   <none>        9092/TCP                     62s
kafka-0-external           NodePort    10.97.145.3    <none>        9094:30001/TCP               62s
kafka-headless             ClusterIP   None           <none>        9092/TCP,9093/TCP            62s
kafka-zookeeper            ClusterIP   10.96.91.58    <none>        2181/TCP,2888/TCP,3888/TCP   62s
kafka-zookeeper-headless   ClusterIP   None           <none>        2181/TCP,2888/TCP,3888/TCP   62s 

>kubectl get pods -n kafka-system
NAME                READY   STATUS    RESTARTS       AGE
kafka-0             1/1     Running   2 (2m8s ago)   2m36s
kafka-zookeeper-0   1/1     Running   0              2m36s
```

Expose service with minikube using this [guide](https://github.com/kubernetes/minikube/issues/877#issuecomment-719937009):

```sh
service_name=kafka-0-external
service_port=$(minikube service $service_name --url -n kafka-system | cut -d':' -f3)
ssh -i ~/.minikube/machines/minikube/id_rsa docker@$(minikube ip) -NL \*:${service_port}:0.0.0.0:${service_port}
```

Use [kafkacat](https://github.com/edenhill/kcat) to test from remote host:
```sh
remote$ kcat -b 84.201.140.235:30001 -L
Metadata for all topics (from broker 0: 84.201.140.235:30001/0):
 1 brokers:
  broker 0 at 84.201.140.235:30001 (controller)
 3 topics:
  topic "test" with 1 partitions:
    partition 0, leader 0, replicas: 0, isrs: 0
....

Remote$ kcat -b 84.201.140.235:30001 -t test -C -o begining
test1
test2
test3
123
....
% Reached end of topic test [0] at offset 12
```
 Stop port forwarding
 ```sh
 lsof -ti:30001 | xargs kill -9
 ```

 Delete release and namespace
 ```sh
$ helm uninstall kafka -n kafka-system
release "kafka" uninstalled
$ kubectl delete namespace kafka-system
namespace "kafka-system" deleted
 ```

## Implemented checks

| ID| Type| Entity | Policy| Description | IaC Policy|
| :--- | :--- | :---| :---|:---|:---|
| CKV_KAFKA_1 | resource |StatefulSet| Ensure that `allowEveryoneIfNoAclFoundCheck` is set to false or unused |If a resource has no associated ACLs and [allow.everyone.if.no.acl.found](https://kafka.apache.org/documentation/#security_authz)=true, then anyone is allowed to access that resource. If `allow.everyone.if.no.acl.found=false`, then no one is allowed to access that resource except super users. Use of the `allow.everyone.if.no.acl.found` configuration option in production environments is strongly [discouraged](https://docs.confluent.io/platform/current/kafka/authorization.html): 1) If you specify this option based on the assumption that you have ACLs, but then your last ACL is deleted, you essentially open up your Kafka clusters to all users; 2) If you’re using this option to disable ACLs, exercise caution: if someone adds an ACL, all the users who previously had access will lose that access.|Kubernetes|
| CKV_KAFKA_2 | resource |StatefulSet| Ensure that pluggable authorizer (ACL) or an out-of-box authorizer implementation is used |Kafka ships with a pluggable Authorizer and an out-of-box authorizer implementation that uses zookeeper to store all the ACLs. The Authorizer is configured by setting [authorizer.class.name](https://kafka.apache.org/documentation/#security_authz). To enable the out of the box implementation you should specify it, e.g. `authorizer.class.name=kafka.security.authorizer.AclAuthorizer`|Kubernetes|
| CKV_KAFKA_3 | resource |StatefulSet| Ensure that `allowPlaintextListener` is set to false | This settings allows to use the plaintext listeners|Kubernetes|



