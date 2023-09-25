from zabbix_api.api_create import ZabbixCreateCalls
from zabbix_api.api_delete import ZabbixDeleteCalls
from zabbix_api.api_export import ZabbixExportCalls
from zabbix_api.api_get import ZabbixGetCalls
from zabbix_api.api_import import ZabbixImportCalls
from zabbix_api.api_update import ZabbixUpdateCalls


class ZabbixCalls(
    ZabbixCreateCalls,
    ZabbixGetCalls,
    ZabbixImportCalls,
    ZabbixExportCalls,
    ZabbixUpdateCalls,
    ZabbixDeleteCalls,
):
    """
    Zabbix API Calls.
    """
