class ZabbixBase:
    """
    Base class for Zabbix API.

    https://www.zabbix.com/documentation/current/en/manual/api
    """

    _RPC = "2.0"
    _ID = 1

    @property
    def base_json(self) -> dict:
        """
        Generic API call.

        :return:
        """

        return {
            "jsonrpc": self._RPC,
            "id": self._ID,
        }

    def get_any(self, method: str, params: dict) -> dict:
        """
        Call any API method supported by Zabbix.

        Zabbix API call request template:

        {
            "jsonrpc": "2.0",
            "method": <API Method>,
            "params": {<API Parameters>},
            "id": 1
        }

        Zabbix API call response template:

        {
            "jsonrpc": "2.0",
            "result": <API Call Result>,
            "id": 1
        }

        :param str method: API method
        :param dict params: API parameters
        :return:
        """

        return self.base_json | {"method": method} | {"method": params}
