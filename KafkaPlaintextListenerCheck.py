from typing import Any, Dict
from checkov.common.models.enums import CheckCategories, CheckResult
from checkov.kubernetes.checks.resource.base_spec_check import BaseK8Check


class KafkaPlaintextListenerCheck(BaseK8Check):

    def __init__(self):
        """
        ALLOW_PLAINTEXT_LISTENER is used to allow to use the PLAINTEXT listener.

        """
        name = "Ensure that allowPlaintextListener is set to false"
        id = "CKV_KAFKA_3"
        supported_kind = ['StatefulSet']
        categories = [CheckCategories.KUBERNETES]
        super().__init__(name=name, id=id, categories=categories, supported_entities=supported_kind)

    def scan_spec_conf(self, conf) -> CheckResult:
        try:
            for container in conf["spec"]["template"]["spec"]["containers"]:
                for env in container["env"]:
                    if env["name"] == "ALLOW_PLAINTEXT_LISTENER":
                        if env["value"] == None:
                            return CheckResult.FAILED
                        elif env["value"].lower() == "no":
                            return CheckResult.PASSED
                        else:
                            return CheckResult.FAILED
        except KeyError:
            return CheckResult.UNKNOWN
        return CheckResult.UNKNOWN

check = KafkaPlaintextListenerCheck()