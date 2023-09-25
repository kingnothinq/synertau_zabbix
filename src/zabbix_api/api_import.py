from pathlib import Path

from zabbix_api.api_base import ZabbixBase


class ZabbixImportCalls(ZabbixBase):
    """
    Zabbix API Import calls.
    """

    def import_config_yaml(self, path: Path) -> dict:
        """
        Get Items.
        https://www.zabbix.com/documentation/current/en/manual/api/reference/item/get

        :param Path path:
        :return:
        """

        method = "configuration.import"
        params = {
            "params": {
                "format": "yaml",
                "rules": {
                    "template_groups": {"createMissing": True, "updateExisting": True},
                    "templates": {"createMissing": True, "updateExisting": True},
                    "items": {"createMissing": True, "updateExisting": True},
                    "triggers": {"createMissing": True, "updateExisting": True},
                    "valueMaps": {"createMissing": True, "updateExisting": True},
                },
                "source": self._yaml_to_str(path),
            }
        }
        return self.base_json | {"method": method} | params

    @staticmethod
    def _yaml_to_str(path: Path) -> str:
        with open(file=path, mode="r", encoding="utf-8") as conf_yaml:
            config = conf_yaml.readlines()

        return "".join(config)
