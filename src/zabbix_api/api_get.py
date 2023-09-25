from zabbix_api.api_base import ZabbixBase


class ZabbixGetCalls(ZabbixBase):
    """
    Zabbix API GET calls.
    """

    def get_host_group(self, name: str) -> dict:
        """
        Get Hostgroup.
        https://www.zabbix.com/documentation/current/en/manual/api/reference/hostgroup/get

        :param str name:
        :return:
        """

        method = "hostgroup.get"
        params = {"params": {"output": "extend", "filter": {"name": [name]}}}
        return self.base_json | {"method": method} | params

    def get_host(self, name: str) -> dict:
        """
        Get Host.
        https://www.zabbix.com/documentation/current/en/manual/api/reference/host/get

        :param str name:
        :return:
        """

        method = "host.get"
        params = {"params": {"output": "extend", "filter": {"name": [name]}}}
        return self.base_json | {"method": method} | params

    def get_item(self, name: str) -> dict:
        """
        Get Item.
        https://www.zabbix.com/documentation/current/en/manual/api/reference/item/get

        :param str name:
        :return:
        """

        method = "item.get"
        params = {"params": {"output": "extend", "filter": {"name": [name]}}}
        return self.base_json | {"method": method} | params

    def get_items(self, names: list) -> dict:
        """
        Get Items.
        https://www.zabbix.com/documentation/current/en/manual/api/reference/item/get

        :param list names:
        :return:
        """

        method = "item.get"
        params = {
            "params": {
                "output": ["itemid", "hostid", "name"],
                "filter": {"name": names},
            }
        }
        return self.base_json | {"method": method} | params

    def get_templates(self, names: list) -> dict:
        """
        Get Templates.
        https://www.zabbix.com/documentation/current/en/manual/api/reference/template/get

        :param list names:
        :return:
        """

        method = "template.get"
        params = {"params": {"output": "extend", "filter": {"name": names}}}
        return self.base_json | {"method": method} | params
