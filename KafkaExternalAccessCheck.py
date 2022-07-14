from typing import Any, Dict
from checkov.common.models.enums import CheckCategories, CheckResult
from checkov.kubernetes.checks.resource.base_spec_check import BaseK8Check


class KafkaExternalAccessCheck(BaseK8Check):

    def __init__(self):
        """
        Param externalAccess.enabled enables Kubernetes external cluster access to Kafka brokers
        """
        name = "Ensure that externalAccess.enabled for Kafka is set to false or external access is implemented based on the principle of least privilege"
        id = "CKV_KAFKA_4"
        supported_kind = ['Service']
        categories = [CheckCategories.KUBERNETES]
        super().__init__(name=name, id=id, categories=categories, supported_entities=supported_kind)

    def scan_spec_conf(self, conf) -> CheckResult:
        try:
            if conf["metadata"]["labels"]["app.kubernetes.io/name"] == "kafka":
                if conf["spec"]["type"] == "LoadBalancer" or conf["spec"]["type"] == "NodePort":
                    for port in conf["spec"]["ports"]:
                        if port["name"] == "tcp-kafka" and port["targetPort"] == "kafka-external":
                            return CheckResult.FAILED
                else:
                    return CheckResult.PASSED
            else:
                CheckResult.UNKNOWN
        except KeyError:
            return CheckResult.UNKNOWN
        return CheckResult.UNKNOWN

check = KafkaExternalAccessCheck()