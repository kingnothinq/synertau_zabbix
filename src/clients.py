import json
import os
from http import HTTPStatus

from typing import Optional, Any
from urllib.parse import ParseResult

import httpx


class ZabbixClient:
    """
    HTTPx client for Zabbix.
    """

    def __init__(self) -> None:
        self._API: str = "api_jsonrpc.php"
        self._URL: Optional[str] = os.getenv("ZABBIX_SERVER")
        self._PORT: Optional[str] = os.getenv("ZABBIX_PORT")
        self._token: Optional[str] = os.getenv("ZABBIX_API_KEY")

    @property
    def headers_no_auth(self) -> dict:
        """
        HTTP Header w/o authorization.

        :return:
        """

        return {
            "Content-Type": "application/json-rpc",
        }

    @property
    def headers(self) -> dict:
        """
        HTTP Header w/ authorization.

        :return:
        """

        return {
            "Content-Type": "application/json-rpc",
            "Authorization": f"Bearer {self._token}",
        }

    def _build_url(self) -> str:
        """
        Create URL for Zabbix API.

        :return: URL
        """

        return ParseResult(
            scheme="http",
            netloc=f"{self._URL}{self._PORT}",
            path=self._API,
            params="",
            query="",
            fragment="",
        ).geturl()

    @staticmethod
    def _request(**kwargs: Any) -> Optional[dict]:
        """
        HTTP Post to Zabbix.
        kwargs params:
        url - Zabbix API URL
        headers - Content-Type and Authorization
        content - Zabbix API call

        :params kwargs:
        :return:
        """

        with httpx.Client(verify=False) as client:
            response = client.post(
                url=kwargs.get("url"),
                headers=kwargs.get("header"),
                content=kwargs.get("content"),
            )
            if response.status_code == HTTPStatus.OK:
                return response.json()

            return None

    def call_api(self, data: dict) -> Optional[dict]:
        return self._request(
            url=self._build_url(), header=self.headers, content=json.dumps(data)
        )
