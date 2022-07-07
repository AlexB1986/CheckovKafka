from typing import Any, Dict
from checkov.common.models.enums import CheckCategories, CheckResult
from checkov.kubernetes.checks.resource.base_spec_check import BaseK8Check


class KafkaAllowEveryoneIfNoAclFoundCheck(BaseK8Check):

    def __init__(self):
        """
        https://docs.confluent.io/platform/current/kafka/authorization.html

        """
        name = "Ensure that allowEveryoneIfNoAclFoundCheck is set to false or unused"
        id = "CKV_KAFKA_1"
        supported_kind = ['StatefulSet']
        categories = [CheckCategories.KUBERNETES]
        super().__init__(name=name, id=id, categories=categories, supported_entities=supported_kind)

    def scan_spec_conf(self, conf):
        try:
            for container in conf["spec"]["template"]["spec"]["containers"]:
                for env in container["env"]:
                    if env["name"] == "KAFKA_CFG_ALLOW_EVERYONE_IF_NO_ACL_FOUND" and env["value"] == "true":
                        return CheckResult.FAILED
        except KeyError:
            return CheckResult.PASSED
        return CheckResult.PASSED

check = KafkaAllowEveryoneIfNoAclFoundCheck()