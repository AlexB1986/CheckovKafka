from typing import Any, Dict
from checkov.common.models.enums import CheckCategories, CheckResult
from checkov.kubernetes.checks.resource.base_spec_check import BaseK8Check


class KafkaAllowEveryoneIfNoAclFoundCheck(BaseK8Check):

    def __init__(self):
        """
        If a resource has no associated ACLs and allow.everyone.if.no.acl.found=true, then anyone is allowed to access that resource.
        If allow.everyone.if.no.acl.found=false, then no one is allowed to access that resource except super users.
        Use of the allow.everyone.if.no.acl.found configuration option in production environments is strongly discouraged.
        - If you specify this option based on the assumption that you have ACLs, but then your last ACL is deleted, you essentially open up your Kafka clusters to all users.
        - If you’re using this option to disable ACLs, exercise caution: if someone adds an ACL, all the users who previously had access will lose that access.
        https://docs.confluent.io/platform/current/kafka/authorization.html
        https://kafka.apache.org/documentation/#security_authz

        """
        name = "Ensure that allowEveryoneIfNoAclFoundCheck is set to false or unused"
        id = "CKV_KAFKA_1"
        supported_kind = ['StatefulSet']
        categories = [CheckCategories.KUBERNETES]
        super().__init__(name=name, id=id, categories=categories, supported_entities=supported_kind)

    def scan_spec_conf(self, conf) -> CheckResult:
        try:
            for container in conf["spec"]["template"]["spec"]["containers"]:
                for env in container["env"]:
                    if env["name"] == "KAFKA_CFG_ALLOW_EVERYONE_IF_NO_ACL_FOUND" and env["value"] == "true":
                        return CheckResult.FAILED
        except KeyError:
            return CheckResult.PASSED
        return CheckResult.PASSED

check = KafkaAllowEveryoneIfNoAclFoundCheck()