# Synertau Zabbix Dashboard

This Postman collection is used to create Synertau Zabbix Dashboard.

## Installation

Install the appropriate software:

1. [Postman](https://www.postman.com/).

## Usage

1. Import Postman collection and Postman Evnironment Variables:
   - zabbix.postman_collection.json
   - ZabbixVars.postman_environment.json
   
   https://learning.postman.com/docs/getting-started/importing-and-exporting/importing-and-exporting-overview/

2. Get Zabbix API Token:
   
   Users -> API Tokens -> Create API token

3. Set your variables:

   Postman -> Environment -> `ZabbixVars`

   Modify ONLY the next fields:
   - URL: IP Address or URL of your server
   - PORT: Port where your server is started
   - API_TOKEN: Given Zabbix API Token
   - IPERF: IP address of your Iperf Server

   https://blog.postman.com/using-variables-inside-postman-and-collection-runner/

4. Run Postman Collection

   Postman -> Collections -> `zabbix` -> Right Click and hit "Run collection" -> Run zabbix

   You can run subfolders separately if you don't need Dashboard or Scripts.
   
   Please don't modify the order of requests.

   https://learning.postman.com/docs/collections/running-collections/intro-to-collection-runs/

## License
[MIT](https://choosealicense.com/licenses/mit/)
