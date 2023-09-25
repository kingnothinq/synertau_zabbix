import logging
from pathlib import Path
from typing import Optional

from dotenv import load_dotenv

from calls import ZabbixCalls
from clients import ZabbixClient

# Build path inside the project
ROOT_DIR: Path = Path(__file__).parent
# Environment
dotenv_path = ROOT_DIR / "src" / ".env"
if dotenv_path.exists():
    load_dotenv(dotenv_path)
# Logger
logger = logging.getLogger(__name__)


class ZabbixConfiguration:

    def __init__(self):
        self.client = ZabbixClient()
        self.api = ZabbixCalls()
        self.host_groups = {"CPE_Wive-NG": None,
                            "WIFI CLIENTS 5": None,
                            "WIFI CLIENTS 24": None
                            }
        self.template_groups = {"CPE Wive-NG": None,
                                }
        self.templates = {"CreateWIFIHOST5metrics": None,
                          "CreateWIFIHOST24metrics": None,
                          "WirelessStationInfo": None,
                          "WICAT-MIB - wicat": None,
                          "WiCatManagement": None,
                          "WIFI_Clients_status": None,
                          }
        self.rules = {"Discovery Wi-Fi Clients - host5": None,
                      "Discovery Wi-Fi Clients - host24": None
                      }

    def create_host_groups(self):
        """
        Call API to import Synertau Host Groups.

        :return:
        """

        for group in self.host_groups.keys():
            request = self.api.create_host_group(group)
            response = self.client.call_api(data=request)
            if response and not ("error" in response):
                self.host_groups[group] = response.get("result").get("groupids")[0]
                logger.debug("Success")
            else:
                logger.debug("Fail")

    def create_template_groups(self):
        """
        Call API to import Synertau Template Groups.

        :return:
        """

        for group in self.template_groups.keys():
            request = self.api.create_template_group(group)
            response = self.client.call_api(data=request)
            if response and not ("error" in response):
                self.template_groups[group] = response.get("result").get("groupids")[0]
                logger.debug("Success")
            else:
                logger.debug("Fail")

    def import_templates(self):
        """
        Call API to import Synertau Templates.

        :return:
        """

        yaml_path = ROOT_DIR / "src" / "zabbix_templates" / "synertau_template.yaml"
        request = self.api.import_config_yaml(yaml_path)
        response = self.client.call_api(data=request)
        if response and not ("error" in response):
            logger.debug("Success")
        else:
            logger.debug("Fail")

    def create_lld_rules(self):
        """
        Call API to create Synertau Low Level Discovery Rules.

        :return:
        """

        request = self.api.get_items(["WalkWiFiMac5", "WalkWiFiMac24"])
        response = self.client.call_api(data=request)
        if response and not ("error" in response):
            hostid = response.get("result")[0].get("hostid")
            itemid5 = response.get("result")[0].get("itemid")
            itemid24 = response.get("result")[1].get("itemid")
            request = self.api.create_lld_rules(hostid, itemid5, itemid24)
            for rule in request:
                response = self.client.call_api(data=rule)
                if response and not ("error" in response):
                    self.rules[rule.get("params").get("name")] = response.get("result").get("itemids")[0]
                    logger.debug("Success")
        else:
            logger.debug("Fail")

    def create_host_prototypes(self):
        """
        Call API to create Synertau Host Prototypes.

        :return:
        """

        prototype5 = {"host": "wc5_{#MAC5}",
                      "name": "{#MAC5}",
                      "ruleid": self.rules.get("Discovery Wi-Fi Clients - host5"),
                      "groupid": self.host_groups.get("WIFI CLIENTS 5"),
                      "templateid": self.templates.get("CreateWIFIHOST5metrics"),
                      }
        prototype24 = {"host": "wc24_{#MAC24}",
                       "name": "{#MAC24}",
                       "ruleid": self.rules.get("Discovery Wi-Fi Clients - host24"),
                       "groupid": self.host_groups.get("WIFI CLIENTS 24"),
                       "templateid": self.templates.get("CreateWIFIHOST24metrics"),
                       }
        for prototype in [prototype5, prototype24]:
            request = self.api.create_host_prototype(prototype)
            response = self.client.call_api(data=request)
            if response and not ("error" in response):
                logger.debug("Success")
            else:
                logger.debug("Fail")

    def create_scripts(self):
        """
        Call API to create Synertau Scripts.

        :return:
        """

        group = self.get_host_group("CPE_Wive-NG")

        request = self.api.create_scripts(group)
        for script in request:
            response = self.client.call_api(data=script)
            if response and not ("error" in response):
                logger.debug("Success")
            else:
                logger.debug("Fail")

    def create_dashboard(self):
        """
        Call API to create Synertau Dashboard.

        :return:
        """

        wive_group = self.get_host_group("CPE_Wive-NG")
        group_5 = self.get_host_group("WIFI CLIENTS 5")
        group_24 = self.get_host_group("WIFI CLIENTS 24")
        request = self.api.get_item("Summ wifi clients")
        response = self.client.call_api(data=request)
        if response and not ("error" in response):
            sum_clients = response.get("result")[0].get("itemid")
            request = self.api.create_dashboard(wive_group, group_5, group_24, sum_clients)
            response = self.client.call_api(data=request)
            if response and not ("error" in response):
                logger.debug("Success")
        else:
            logger.debug("Fail")

    def get_host_group(self, name: str) -> Optional[str]:
        """
        Call API to get Host Group.

        :param str name:
        :return:
        """

        request = self.api.get_host_group(name)
        response = self.client.call_api(data=request)

        if response and not ("error" in response):
            logger.debug("Success")
            return response.get("result")[0].get("groupid")

        logger.debug("Fail")
        return None

    def get_host(self, name: str) -> Optional[str]:
        """
        Call API to get Host.

        :param str name:
        :return:
        """

        request = self.api.get_host(name)
        response = self.client.call_api(data=request)

        if response and not ("error" in response):
            logger.debug("Success")
            return response.get("result")[0].get("groupid")

        logger.debug("Fail")
        return None

    def get_templates(self) -> Optional[str]:
        """
        Call API to get Templates.

        :return:
        """

        request = self.api.get_templates(list(self.templates.keys()))
        response = self.client.call_api(data=request)
        if response and not ("error" in response):
            for template in response.get("result"):
                self.templates[template.get("host")] = template.get("templateid")
            logger.debug("Success")

        logger.debug("Fail")
        return None


if __name__ == "__main__":
    app = ZabbixConfiguration()
    logger.info("Run configuration...")
    # Configure groups
    app.create_host_groups()
    # Configure template groups
    app.create_template_groups()
    # Import templates from yaml
    app.import_templates()
    # Get Templates
    app.get_templates()
    # Create Low Level Discovery Rules
    app.create_lld_rules()
    # Create Host Prototypes
    app.create_host_prototypes()
    # Configure scripts
    app.create_scripts()
    # Create Dashboard
    app.create_dashboard()
    logger.info("Server configured!")
