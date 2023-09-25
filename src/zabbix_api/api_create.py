from copy import deepcopy

from zabbix_api.api_base import ZabbixBase


class ZabbixCreateCalls(ZabbixBase):
    """
    Zabbix API Create calls.
    """

    def create_host_group(self, name: str) -> dict:
        """
        Create Host Group.
        https://www.zabbix.com/documentation/current/en/manual/api/reference/hostgroup/create

        :param str name:
        :return:
        """

        method = "hostgroup.create"
        params = {
            "params": {
                "name": name,
            }
        }
        return self.base_json | {"method": method} | params

    def create_template_group(self, name: str) -> dict:
        """
        Create Template Group.
        https://www.zabbix.com/documentation/current/en/manual/api/reference/templategroup/create

        :param str name:
        :return:
        """

        method = "templategroup.create"
        params = {
            "params": {
                "name": name,
            }
        }
        return self.base_json | {"method": method} | params

    def create_scripts(self, groupid: str) -> list[dict]:
        """
        Create Scripts.
        https://www.zabbix.com/documentation/current/en/manual/api/reference/script/create

        :param str groupid:
        :return:
        """

        scripts = []
        method = "script.create"
        params = {
            "params": {
                "host_access": "2",
                "usrgrpid": "0",
                "groupid": groupid,
                "type": "0",
                "execute_on": "0",
                "scope": "2",
                "menu_path": "Scripts",
            }
        }

        # Scan Radio
        script = deepcopy(params)
        script["params"]["name"] = "Scan Radio"
        script["params"]["command"] = "wl scan"
        scripts.append(self.base_json | {"method": method} | script)
        # Show LLDP
        script = deepcopy(params)
        script["params"]["name"] = "Show LLDP"
        script["params"]["command"] = "lldpcli show neighbors"
        scripts.append(self.base_json | {"method": method} | script)
        # Show Wi-Fi Status
        script = deepcopy(params)
        script["params"]["name"] = "Show WIFI Status"
        script["params"]["command"] = "wl status"
        scripts.append(self.base_json | {"method": method} | script)
        # Speedtest Iperf
        script = deepcopy(params)
        script["params"]["name"] = "Speedtest Iperf"
        script["params"]["command"] = "iperf3 -c 192.168.88.88 -R"
        scripts.append(self.base_json | {"method": method} | script)
        # View Wi-Fi Clients Metrics
        script = deepcopy(params)
        script["params"]["name"] = "View Wi-Fi Clients Metrics"
        script["params"]["command"] = "wl stalist"
        scripts.append(self.base_json | {"method": method} | script)

        return scripts

    def create_lld_rules(self, hostid: str, itemid5: str, itemid24: str) -> list[dict]:
        """
        Create Low Level Discovery Rules.
        https://www.zabbix.com/documentation/current/en/manual/api/reference/discoveryrule/create

        Template Host and Item IDs aren't visible in GUI.

        :param str hostid: Template Host ID
        :param str itemid5: Template Item ID for 5 GHz
        :param str itemid24: Template Item ID for 2.4 GHz
        :return:
        """

        rules = []
        method = "discoveryrule.create"
        params = {"params": {"hostid": hostid, "type": "18"}}

        # Discovery Wi-Fi Clients - host5
        rule = deepcopy(params)
        rule["params"]["name"] = "Discovery Wi-Fi Clients - host5"
        rule["params"]["key_"] = "MacHost5"
        rule["params"]["master_itemid"] = itemid5
        rules.append(self.base_json | {"method": method} | rule)
        # Discovery Wi-Fi Clients - host24
        rule = deepcopy(params)
        rule["params"]["name"] = "Discovery Wi-Fi Clients - host24"
        rule["params"]["key_"] = "MacHost24"
        rule["params"]["master_itemid"] = itemid24
        rules.append(self.base_json | {"method": method} | rule)

        return rules

    def create_host_prototype(self, prototype: dict) -> dict:
        """
        Create Host Prototepe
        https://www.zabbix.com/documentation/current/en/manual/api/reference/hostprototype/create

        :param dict prototype:
        :return:
        """

        method = "hostprototype.create"
        params = {
            "params": {
                "host": prototype.get("host"),
                "name": prototype.get("name"),
                "ruleid": prototype.get("ruleid"),
                "groupLinks": [{"groupid": prototype.get("groupid")}],
                "templates": [{"templateid": prototype.get("templateid")}],
            }
        }

        return self.base_json | {"method": method} | params

    def create_dashboard(
        self, wive_group: str, group_5: str, group_24: str, sum_clients: str
    ) -> dict:
        """
        Create Dashboard
        https://www.zabbix.com/documentation/current/en/manual/api/reference/dashboard/create

        :param str wive_group:
        :param str group_5:
        :param str group_24:
        :param str sum_clients:
        :return:
        """

        method = "dashboard.create"
        params = {
            "params": {
                "name": "CPE Wive-NG",
                "display_period": "10",
                "userid": "1",
                "private": "1",
                "auto_start": "1",
                "pages": self._create_dashboard_pages(
                    wive_group, group_5, group_24, sum_clients
                ),
                "users": [{"userid": "1", "permission": "2"}],
                "userGroups": [{"usrgrpid": "7", "permission": "2"}]
            }
        }

        return self.base_json | {"method": method} | params

    @staticmethod
    def _create_dashboard_pages(
        wive_group: str, group_5: str, group_24: str, sum_clients: str
    ) -> list:
        """
        Create Pages
        https://www.zabbix.com/documentation/current/en/manual/api/reference/dashboard/create

        :param str wive_group:
        :param str group_5:
        :param str group_24:
        :param str sum_clients:
        :return:
        """

        return [
            {
                "name": "",
                "display_period": "0",
                "widgets": [
                    {
                        "type": "hostavail",
                        "name": "Доступность узлов сети",
                        "x": "0",
                        "y": "0",
                        "width": "7",
                        "height": "2",
                        "view_mode": "0",
                        "fields": [
                            {"type": "0", "name": "rf_rate", "value": "10"},
                            {"type": "2", "name": "groupids", "value": wive_group},
                            {"type": "0", "name": "interface_type", "value": "2"}
                        ]
                    },
                    {
                        "type": "problemhosts",
                        "name": "",
                        "x": "0",
                        "y": "2",
                        "width": "7",
                        "height": "2",
                        "view_mode": "0",
                        "fields": [
                            {"type": "2", "name": "groupids", "value": wive_group},
                            {"type": "0", "name": "hide_empty_groups", "value": "1"},
                            {"type": "0", "name": "ext_ack", "value": "1"}
                        ]
                    },
                    {
                        "type": "tophosts",
                        "name": "Информация о точках доступа",
                        "x": "0",
                        "y": "4",
                        "width": "24",
                        "height": "3",
                        "view_mode": "0",
                        "fields": [
                            {"type": "2", "name": "groupids", "value": wive_group},
                            {"type": "1", "name": "columns.name.0", "value": "Ping"},
                            {"type": "0", "name": "columns.data.0", "value": "1"},
                            {
                                "type": "0",
                                "name": "columns.aggregate_function.0",
                                "value": "0"
                            },
                            {
                                "type": "0",
                                "name": "columns.decimal_places.0",
                                "value": "0"
                            },
                            {"type": "1", "name": "columns.base_color.0", "value": ""},
                            {"type": "1", "name": "columns.name.1", "value": "IP AP"},
                            {"type": "0", "name": "columns.data.1", "value": "2"},
                            {
                                "type": "0",
                                "name": "columns.aggregate_function.1",
                                "value": "0"
                            },
                            {
                                "type": "0",
                                "name": "columns.decimal_places.1",
                                "value": "2"
                            },
                            {"type": "1", "name": "columns.base_color.1", "value": ""},
                            {"type": "1", "name": "columns.name.2", "value": "MAC AP"},
                            {"type": "0", "name": "columns.data.2", "value": "1"},
                            {"type": "1", "name": "columns.item.2", "value": "LAN mac"},
                            {"type": "1", "name": "columns.timeshift.2", "value": ""},
                            {
                                "type": "0",
                                "name": "columns.aggregate_function.2",
                                "value": "0"
                            },
                            {
                                "type": "0",
                                "name": "columns.decimal_places.2",
                                "value": "0"
                            },
                            {"type": "0", "name": "columns.display.2", "value": "1"},
                            {"type": "0", "name": "columns.history.2", "value": "1"},
                            {"type": "1", "name": "columns.base_color.2", "value": ""},
                            {
                                "type": "1",
                                "name": "columns.name.3",
                                "value": "Клиенты на 2.4 GHz"
                            },
                            {"type": "0", "name": "columns.data.3", "value": "1"},
                            {
                                "type": "1",
                                "name": "columns.item.3",
                                "value": "WirlessClients24Numbers"
                            },
                            {"type": "1", "name": "columns.timeshift.3", "value": ""},
                            {
                                "type": "0",
                                "name": "columns.aggregate_function.3",
                                "value": "0"
                            },
                            {
                                "type": "0",
                                "name": "columns.decimal_places.3",
                                "value": "0"
                            },
                            {"type": "0", "name": "columns.display.3", "value": "1"},
                            {"type": "0", "name": "columns.history.3", "value": "1"},
                            {"type": "1", "name": "columns.base_color.3", "value": ""},
                            {
                                "type": "1",
                                "name": "columns.name.4",
                                "value": "Клиенты на 5 GHz"
                            },
                            {"type": "0", "name": "columns.data.4", "value": "1"},
                            {
                                "type": "1",
                                "name": "columns.item.4",
                                "value": "WirlessClients5Numbers"
                            },
                            {"type": "1", "name": "columns.timeshift.4", "value": ""},
                            {
                                "type": "0",
                                "name": "columns.aggregate_function.4",
                                "value": "0"
                            },
                            {
                                "type": "0",
                                "name": "columns.decimal_places.4",
                                "value": "0"
                            },
                            {"type": "0", "name": "columns.display.4", "value": "1"},
                            {"type": "0", "name": "columns.history.4", "value": "1"},
                            {"type": "1", "name": "columns.base_color.4", "value": ""},
                            {"type": "0", "name": "rf_rate", "value": "10"},
                            {
                                "type": "1",
                                "name": "columns.name.5",
                                "value": "Канал 2.4 GHz"
                            },
                            {"type": "0", "name": "columns.data.5", "value": "1"},
                            {
                                "type": "1",
                                "name": "columns.item.5",
                                "value": "Channel for 24"
                            },
                            {"type": "1", "name": "columns.timeshift.5", "value": ""},
                            {
                                "type": "0",
                                "name": "columns.aggregate_function.5",
                                "value": "0"
                            },
                            {
                                "type": "0",
                                "name": "columns.decimal_places.5",
                                "value": "0"
                            },
                            {"type": "0", "name": "columns.display.5", "value": "1"},
                            {"type": "0", "name": "columns.history.5", "value": "1"},
                            {"type": "1", "name": "columns.base_color.5", "value": ""},
                            {
                                "type": "1",
                                "name": "columns.name.6",
                                "value": "Канал 5 GHz"
                            },
                            {"type": "0", "name": "columns.data.6", "value": "1"},
                            {
                                "type": "1",
                                "name": "columns.item.6",
                                "value": "Channel for 5"
                            },
                            {"type": "1", "name": "columns.timeshift.6", "value": ""},
                            {
                                "type": "0",
                                "name": "columns.aggregate_function.6",
                                "value": "0"
                            },
                            {
                                "type": "0",
                                "name": "columns.decimal_places.6",
                                "value": "0"
                            },
                            {"type": "0", "name": "columns.display.6", "value": "1"},
                            {"type": "0", "name": "columns.history.6", "value": "1"},
                            {"type": "1", "name": "columns.base_color.6", "value": ""},
                            {"type": "0", "name": "count", "value": "50"},
                            {
                                "type": "1",
                                "name": "columns.name.7",
                                "value": "УШ 2.4 GHz"
                            },
                            {"type": "0", "name": "columns.data.7", "value": "1"},
                            {
                                "type": "1",
                                "name": "columns.item.7",
                                "value": "NoiseFloor24"
                            },
                            {"type": "1", "name": "columns.timeshift.7", "value": ""},
                            {
                                "type": "0",
                                "name": "columns.aggregate_function.7",
                                "value": "0"
                            },
                            {
                                "type": "0",
                                "name": "columns.decimal_places.7",
                                "value": "0"
                            },
                            {"type": "0", "name": "columns.display.7", "value": "1"},
                            {"type": "0", "name": "columns.history.7", "value": "1"},
                            {"type": "1", "name": "columns.base_color.7", "value": ""},
                            {
                                "type": "1",
                                "name": "columns.name.8",
                                "value": "УШ 5 GHz"
                            },
                            {"type": "0", "name": "columns.data.8", "value": "1"},
                            {
                                "type": "1",
                                "name": "columns.item.8",
                                "value": "NoiseFloor5"
                            },
                            {"type": "1", "name": "columns.timeshift.8", "value": ""},
                            {
                                "type": "0",
                                "name": "columns.aggregate_function.8",
                                "value": "0"
                            },
                            {
                                "type": "0",
                                "name": "columns.decimal_places.8",
                                "value": "0"
                            },
                            {"type": "0", "name": "columns.display.8", "value": "1"},
                            {"type": "0", "name": "columns.history.8", "value": "1"},
                            {"type": "1", "name": "columns.base_color.8", "value": ""},
                            {
                                "type": "1",
                                "name": "columns.name.9",
                                "value": "Исх.трафик"
                            },
                            {"type": "0", "name": "columns.data.9", "value": "1"},
                            {
                                "type": "1",
                                "name": "columns.item.9",
                                "value": "Interface eth2: Bits sent"
                            },
                            {"type": "1", "name": "columns.timeshift.9", "value": ""},
                            {
                                "type": "0",
                                "name": "columns.aggregate_function.9",
                                "value": "0"
                            },
                            {
                                "type": "0",
                                "name": "columns.decimal_places.9",
                                "value": "2"
                            },
                            {"type": "0", "name": "columns.display.9", "value": "1"},
                            {"type": "0", "name": "columns.history.9", "value": "1"},
                            {"type": "1", "name": "columns.base_color.9", "value": ""},
                            {
                                "type": "1",
                                "name": "columns.name.10",
                                "value": "Вх.трафик"
                            },
                            {"type": "0", "name": "columns.data.10", "value": "1"},
                            {
                                "type": "1",
                                "name": "columns.item.10",
                                "value": "Interface eth2: Bits received"
                            },
                            {"type": "1", "name": "columns.timeshift.10", "value": ""},
                            {
                                "type": "0",
                                "name": "columns.aggregate_function.10",
                                "value": "0"
                            },
                            {
                                "type": "0",
                                "name": "columns.decimal_places.10",
                                "value": "2"
                            },
                            {"type": "0", "name": "columns.display.10", "value": "1"},
                            {"type": "0", "name": "columns.history.10", "value": "1"},
                            {"type": "1", "name": "columns.base_color.10", "value": ""},
                            {
                                "type": "1",
                                "name": "columns.name.11",
                                "value": "Версия ПО"
                            },
                            {"type": "0", "name": "columns.data.11", "value": "1"},
                            {
                                "type": "1",
                                "name": "columns.item.11",
                                "value": "FWversion"
                            },
                            {"type": "1", "name": "columns.timeshift.11", "value": ""},
                            {
                                "type": "0",
                                "name": "columns.aggregate_function.11",
                                "value": "0"
                            },
                            {
                                "type": "0",
                                "name": "columns.decimal_places.11",
                                "value": "0"
                            },
                            {"type": "0", "name": "columns.display.11", "value": "1"},
                            {"type": "0", "name": "columns.history.11", "value": "1"},
                            {"type": "1", "name": "columns.base_color.11", "value": ""},
                            {
                                "type": "1",
                                "name": "columns.name.12",
                                "value": "Наличие обновления"
                            },
                            {"type": "0", "name": "columns.data.12", "value": "1"},
                            {
                                "type": "1",
                                "name": "columns.item.12",
                                "value": "AvaFWversion"
                            },
                            {"type": "1", "name": "columns.timeshift.12", "value": ""},
                            {
                                "type": "0",
                                "name": "columns.aggregate_function.12",
                                "value": "0"
                            },
                            {
                                "type": "0",
                                "name": "columns.decimal_places.12",
                                "value": "0"
                            },
                            {"type": "0", "name": "columns.display.12", "value": "1"},
                            {"type": "0", "name": "columns.history.12", "value": "1"},
                            {"type": "1", "name": "columns.base_color.12", "value": ""},
                            {
                                "type": "1",
                                "name": "columns.item.0",
                                "value": "Generic SNMP: ICMP ping"
                            },
                            {"type": "1", "name": "columns.timeshift.0", "value": ""},
                            {"type": "0", "name": "columns.display.0", "value": "1"},
                            {"type": "0", "name": "columns.history.0", "value": "1"},
                            {
                                "type": "1",
                                "name": "columnsthresholds.color.0.0",
                                "value": "FF465C"
                            },
                            {
                                "type": "1",
                                "name": "columnsthresholds.threshold.0.0",
                                "value": "0"
                            },
                            {
                                "type": "1",
                                "name": "columnsthresholds.color.0.1",
                                "value": "7CB342"
                            },
                            {
                                "type": "1",
                                "name": "columnsthresholds.threshold.0.1",
                                "value": "1"
                            },
                            {"type": "0", "name": "order", "value": "3"},
                            {
                                "type": "1",
                                "name": "columnsthresholds.color.7.0",
                                "value": "FF8A65"
                            },
                            {
                                "type": "1",
                                "name": "columnsthresholds.threshold.7.0",
                                "value": "-50"
                            },
                            {
                                "type": "1",
                                "name": "columns.name.13",
                                "value": "Время работы"
                            },
                            {"type": "0", "name": "columns.data.13", "value": "1"},
                            {
                                "type": "1",
                                "name": "columns.item.13",
                                "value": "Generic SNMP: Uptime (hardware)"
                            },
                            {"type": "1", "name": "columns.timeshift.13", "value": ""},
                            {
                                "type": "0",
                                "name": "columns.aggregate_function.13",
                                "value": "0"
                            },
                            {
                                "type": "0",
                                "name": "columns.decimal_places.13",
                                "value": "2"
                            },
                            {"type": "0", "name": "columns.display.13", "value": "1"},
                            {"type": "0", "name": "columns.history.13", "value": "1"},
                            {"type": "1", "name": "columns.base_color.13", "value": ""}
                        ]
                    },
                    {
                        "type": "item",
                        "name": "Общее количество Wi-Fi Клиентов",
                        "x": "17",
                        "y": "0",
                        "width": "7",
                        "height": "4",
                        "view_mode": "0",
                        "fields": [
                            {"type": "0", "name": "adv_conf", "value": "1"},
                            {"type": "0", "name": "decimal_places", "value": "0"},
                            {"type": "0", "name": "show", "value": "2"},
                            {"type": "0", "name": "show", "value": "4"},
                            {"type": "0", "name": "dynamic", "value": "1"},
                            {"type": "0", "name": "rf_rate", "value": "10"},
                            {"type": "4", "name": "itemid", "value": sum_clients}
                        ]
                    },
                    {
                        "type": "tophosts",
                        "name": "Информация о подключенных клиентах 2.4 GHz",
                        "x": "0",
                        "y": "7",
                        "width": "12",
                        "height": "5",
                        "view_mode": "0",
                        "fields": [
                            {"type": "2", "name": "groupids", "value": group_24},
                            {"type": "1", "name": "columns.name.0", "value": "IP AP"},
                            {"type": "0", "name": "columns.data.0", "value": "3"},
                            {
                                "type": "0",
                                "name": "columns.aggregate_function.0",
                                "value": "0"
                            },
                            {
                                "type": "0",
                                "name": "columns.decimal_places.0",
                                "value": "2"
                            },
                            {"type": "1", "name": "columns.base_color.0", "value": ""},
                            {"type": "0", "name": "rf_rate", "value": "10"},
                            {
                                "type": "1",
                                "name": "columns.name.1",
                                "value": "Mac WiFI Client"
                            },
                            {"type": "0", "name": "columns.data.1", "value": "2"},
                            {
                                "type": "0",
                                "name": "columns.aggregate_function.1",
                                "value": "0"
                            },
                            {
                                "type": "0",
                                "name": "columns.decimal_places.1",
                                "value": "2"
                            },
                            {"type": "1", "name": "columns.base_color.1", "value": ""},
                            {"type": "0", "name": "column", "value": "2"},
                            {
                                "type": "1",
                                "name": "columns.text.0",
                                "value": "{HOST.CONN}"
                            },
                            {
                                "type": "1",
                                "name": "columns.name.2",
                                "value": "Уровень сигнала"
                            },
                            {"type": "0", "name": "columns.data.2", "value": "1"},
                            {"type": "1", "name": "columns.item.2", "value": "RSSI24"},
                            {"type": "1", "name": "columns.timeshift.2", "value": ""},
                            {
                                "type": "0",
                                "name": "columns.aggregate_function.2",
                                "value": "0"
                            },
                            {
                                "type": "0",
                                "name": "columns.decimal_places.2",
                                "value": "0"
                            },
                            {"type": "0", "name": "columns.display.2", "value": "1"},
                            {"type": "0", "name": "columns.history.2", "value": "1"},
                            {"type": "1", "name": "columns.base_color.2", "value": ""},
                            {
                                "type": "1",
                                "name": "columnsthresholds.color.2.0",
                                "value": "FF0000"
                            },
                            {
                                "type": "1",
                                "name": "columnsthresholds.threshold.2.0",
                                "value": "-95"
                            },
                            {
                                "type": "1",
                                "name": "columnsthresholds.color.2.1",
                                "value": "FF8000"
                            },
                            {
                                "type": "1",
                                "name": "columnsthresholds.threshold.2.1",
                                "value": "-80"
                            },
                            {
                                "type": "1",
                                "name": "columnsthresholds.color.2.2",
                                "value": "FFFF00"
                            },
                            {
                                "type": "1",
                                "name": "columnsthresholds.threshold.2.2",
                                "value": "-75"
                            },
                            {
                                "type": "1",
                                "name": "columnsthresholds.color.2.3",
                                "value": "8BC34A"
                            },
                            {
                                "type": "1",
                                "name": "columnsthresholds.threshold.2.3",
                                "value": "-60"
                            },
                            {
                                "type": "1",
                                "name": "columnsthresholds.color.2.4",
                                "value": "43A047"
                            },
                            {
                                "type": "1",
                                "name": "columnsthresholds.threshold.2.4",
                                "value": "-10"
                            },
                            {"type": "0", "name": "count", "value": "100"},
                            {
                                "type": "1",
                                "name": "columns.name.3",
                                "value": "Сигнал/ШУМ"
                            },
                            {"type": "0", "name": "columns.data.3", "value": "1"},
                            {"type": "1", "name": "columns.item.3", "value": "SNR24"},
                            {"type": "1", "name": "columns.timeshift.3", "value": ""},
                            {
                                "type": "0",
                                "name": "columns.aggregate_function.3",
                                "value": "0"
                            },
                            {
                                "type": "0",
                                "name": "columns.decimal_places.3",
                                "value": "2"
                            },
                            {"type": "0", "name": "columns.display.3", "value": "1"},
                            {"type": "0", "name": "columns.history.3", "value": "1"},
                            {"type": "1", "name": "columns.base_color.3", "value": ""},
                            {"type": "0", "name": "order", "value": "3"},
                            {
                                "type": "1",
                                "name": "columns.name.4",
                                "value": "Длительность подключения"
                            },
                            {"type": "0", "name": "columns.data.4", "value": "1"},
                            {
                                "type": "1",
                                "name": "columns.item.4",
                                "value": "ConnectedTime24"
                            },
                            {"type": "1", "name": "columns.timeshift.4", "value": ""},
                            {
                                "type": "0",
                                "name": "columns.aggregate_function.4",
                                "value": "0"
                            },
                            {
                                "type": "0",
                                "name": "columns.decimal_places.4",
                                "value": "0"
                            },
                            {"type": "0", "name": "columns.display.4", "value": "1"},
                            {"type": "0", "name": "columns.history.4", "value": "1"},
                            {"type": "1", "name": "columns.base_color.4", "value": ""}
                        ]
                    },
                    {
                        "type": "svggraph",
                        "name": "Колличество подключенных клиентов",
                        "x": "7",
                        "y": "0",
                        "width": "10",
                        "height": "4",
                        "view_mode": "0",
                        "fields": [
                            {
                                "type": "1",
                                "name": "ds.hosts.0.0",
                                "value": "Zabbix server"
                            },
                            {
                                "type": "1",
                                "name": "ds.items.0.0",
                                "value": "Summ wifi clients"
                            },
                            {"type": "1", "name": "ds.color.0", "value": "80FF00"},
                            {"type": "0", "name": "righty", "value": "0"},
                            {"type": "0", "name": "legend_statistic", "value": "1"}
                        ]
                    },
                    {
                        "type": "tophosts",
                        "name": "Информация о подключенных клиентак 5Ghz",
                        "x": "12",
                        "y": "7",
                        "width": "12",
                        "height": "5",
                        "view_mode": "0",
                        "fields": [
                            {"type": "0", "name": "rf_rate", "value": "10"},
                            {"type": "2", "name": "groupids", "value": group_5},
                            {"type": "1", "name": "columns.name.0", "value": "IP AP"},
                            {"type": "0", "name": "columns.data.0", "value": "3"},
                            {
                                "type": "0",
                                "name": "columns.aggregate_function.0",
                                "value": "0"
                            },
                            {
                                "type": "0",
                                "name": "columns.decimal_places.0",
                                "value": "2"
                            },
                            {"type": "1", "name": "columns.base_color.0", "value": ""},
                            {
                                "type": "1",
                                "name": "columns.text.0",
                                "value": "{HOST.CONN}"
                            },
                            {
                                "type": "1",
                                "name": "columns.name.1",
                                "value": "Mac WiFI Client"
                            },
                            {"type": "0", "name": "columns.data.1", "value": "2"},
                            {
                                "type": "0",
                                "name": "columns.aggregate_function.1",
                                "value": "0"
                            },
                            {
                                "type": "0",
                                "name": "columns.decimal_places.1",
                                "value": "2"
                            },
                            {"type": "1", "name": "columns.base_color.1", "value": ""},
                            {
                                "type": "1",
                                "name": "columns.name.2",
                                "value": "Уровень сигнала"
                            },
                            {"type": "0", "name": "columns.data.2", "value": "1"},
                            {"type": "1", "name": "columns.item.2", "value": "RSSI5"},
                            {"type": "1", "name": "columns.timeshift.2", "value": ""},
                            {
                                "type": "0",
                                "name": "columns.aggregate_function.2",
                                "value": "0"
                            },
                            {
                                "type": "0",
                                "name": "columns.decimal_places.2",
                                "value": "0"
                            },
                            {"type": "0", "name": "columns.display.2", "value": "1"},
                            {"type": "0", "name": "columns.history.2", "value": "1"},
                            {"type": "1", "name": "columns.base_color.2", "value": ""},
                            {
                                "type": "1",
                                "name": "columns.name.3",
                                "value": "Сигнал/ШУМ"
                            },
                            {"type": "0", "name": "columns.data.3", "value": "1"},
                            {"type": "1", "name": "columns.item.3", "value": "SNR5"},
                            {"type": "1", "name": "columns.timeshift.3", "value": ""},
                            {
                                "type": "0",
                                "name": "columns.aggregate_function.3",
                                "value": "0"
                            },
                            {
                                "type": "0",
                                "name": "columns.decimal_places.3",
                                "value": "0"
                            },
                            {"type": "0", "name": "columns.display.3", "value": "1"},
                            {"type": "0", "name": "columns.history.3", "value": "1"},
                            {"type": "1", "name": "columns.base_color.3", "value": ""},
                            {"type": "0", "name": "column", "value": "2"},
                            {
                                "type": "1",
                                "name": "columnsthresholds.color.2.0",
                                "value": "FF0000"
                            },
                            {
                                "type": "1",
                                "name": "columnsthresholds.threshold.2.0",
                                "value": "-95"
                            },
                            {
                                "type": "1",
                                "name": "columnsthresholds.color.2.1",
                                "value": "FF8000"
                            },
                            {
                                "type": "1",
                                "name": "columnsthresholds.threshold.2.1",
                                "value": "-80"
                            },
                            {
                                "type": "1",
                                "name": "columnsthresholds.color.2.2",
                                "value": "FFFF00"
                            },
                            {
                                "type": "1",
                                "name": "columnsthresholds.threshold.2.2",
                                "value": "-75"
                            },
                            {
                                "type": "1",
                                "name": "columnsthresholds.color.2.3",
                                "value": "9CCC65"
                            },
                            {
                                "type": "1",
                                "name": "columnsthresholds.threshold.2.3",
                                "value": "-60"
                            },
                            {
                                "type": "1",
                                "name": "columnsthresholds.color.2.4",
                                "value": "4CAF50"
                            },
                            {
                                "type": "1",
                                "name": "columnsthresholds.threshold.2.4",
                                "value": "-10"
                            },
                            {"type": "0", "name": "order", "value": "3"},
                            {
                                "type": "1",
                                "name": "columns.name.4",
                                "value": "Длительность подключения"
                            },
                            {"type": "0", "name": "columns.data.4", "value": "1"},
                            {
                                "type": "1",
                                "name": "columns.item.4",
                                "value": "ConnectedTime5"
                            },
                            {"type": "1", "name": "columns.timeshift.4", "value": ""},
                            {
                                "type": "0",
                                "name": "columns.aggregate_function.4",
                                "value": "0"
                            },
                            {
                                "type": "0",
                                "name": "columns.decimal_places.4",
                                "value": "0"
                            },
                            {"type": "0", "name": "columns.display.4", "value": "1"},
                            {"type": "0", "name": "columns.history.4", "value": "1"},
                            {"type": "1", "name": "columns.base_color.4", "value": ""}
                        ]
                    }
                ]
            }
        ]
