from zabbix_api.api_base import ZabbixBase


class ZabbixDeleteCalls(ZabbixBase):
    """
    Zabbix API Delete calls.
    """

    def delete_templates(self, templateids: list) -> dict:
        method = "template.massremove"
        params = {"params": {"templateids": templateids}}
        return self.base_json | {"method": method} | params
