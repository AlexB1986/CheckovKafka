from typing import Any, Dict
from checkov.common.models.enums import CheckCategories, CheckResult
from checkov.kubernetes.checks.resource.base_spec_check import BaseK8Check


class KafkaCheckAuthorizer(BaseK8Check):

    def __init__(self):
        """
        Kafka ships with a pluggable Authorizer and an out-of-box authorizer implementation that uses zookeeper to store all the ACLs. 
        The Authorizer is configured by setting authorizer.class.name. To enable the out of the box implementation you should specify it,
        e.g. authorizer.class.name=kafka.security.authorizer.AclAuthorizer
        https://kafka.apache.org/documentation/#security_authz

        """
        name = "Ensure that pluggable authorizer (ACL) or an out-of-box authorizer implementation is used"
        id = "CKV_KAFKA_2"
        supported_kind = ['StatefulSet']
        categories = [CheckCategories.KUBERNETES]
        super().__init__(name=name, id=id, categories=categories, supported_entities=supported_kind)

    def scan_spec_conf(self, conf) -> CheckResult:
        try:
            for container in conf["spec"]["template"]["spec"]["containers"]:
                for env in container["env"]:
                    if env["name"] == "KAFKA_CFG_AUTHORIZER_CLASS_NAME":
                        if  env["value"] == "" or env["value"] == None:
                            return CheckResult.FAILED
                        else:
                            return CheckResult.PASSED
        except KeyError:
            return CheckResult.UNKNOWN
        return CheckResult.UNKNOWN

check = KafkaCheckAuthorizer()