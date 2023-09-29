# Synertau Zabbix Server Configurator


## Installation

Clone the repository to your computer:
```bash
git clone https://github.com/kingnothinq/synertau_zabbix.git
```

### Requirements:

Install the appropriate software:

1. [Docker Desktop](https://www.docker.com).
2. [Git](https://github.com/git-guides/install-git).
3. [PyCharm](https://www.jetbrains.com/ru-ru/pycharm/download) (optional).

## Usage

1. Configure Zabbix Server following the official documentation:
   [Zabbix from containers](https://www.zabbix.com/documentation/current/en/manual/installation/containers).

   You can modify this part according to your standards.
   
   The example provided in this project: Zabbix Nginx Frontend + PostgreSQL Backend.

   To set it up, fulfill the variables and parameters in the next configuration files in the `env_vars` folder:
   - `.env_db_pgsql` – PostgreSQL Server configuration
   - `.POSTGRES_USER` – PostgreSQL User
   - `.POSTGRES_PASSWORD` – PostgreSQL Password
   - `.env_srv` – Zabbix Server configuration
   - `.env_web` – Zabbix Frontend Server configuration

2. Build the container using Docker Compose:
    ```shell
    docker compose build
    ```
   This command should be run from the root directory where `Dockerfile` is located.
   You also need to build the docker container again in case if you have updated `requirements.txt`.

3. Now it is possible to run the project inside the Docker container:
    ```shell
    docker compose up
    ```
   When containers are up server starts at [http://0.0.0.0:80](http://0.0.0.0:80). You can open it in your browser.

4. The server can be configured to have the Synertau templates in two ways:
   - Using a script
   
   To configure the Synertau application copy `.env_app.sample` into `.env_app` file in the env_vars folder:
    ```shell
    cp .env_app.sample .env_app
    ```
   
   This file contains environment variables that will share their values across the application.
   The sample file (`.env_app.sample`) contains a set of variables with default values. 
   So it can be configured depending on the environment.
   
   Set received access tokens as environment variable values (in `.env_app` file):
   - `ZABBIX_SERVER` – Zabbix Server URL or IP
   - `ZABBIX_PORT` – Zabbix Server Port
   - `ZABBIX_API_KEY` – Given Zabbix API Token (Users -> API Tokens -> Create API token)
   - `IPERF_SERVER` – Your Iperf Server (used in Scripts)

   - Using Postman collection
   Please read README.md in the `postman` folder.

## Documentation

The project integrated with the [Sphinx](https://www.sphinx-doc.org/en/master/) documentation engine. 
It allows the creation of documentation from source code. 
So the source code should contain docstrings in [reStructuredText](https://docutils.sourceforge.io/rst.html) format.

To create HTML documentation run this command from the source directory where `Makefile` is located:
```shell
make docs-html
```

After generation documentation can be opened from a file `docs/build/html/index.html`.

## Contributing
Pull requests are welcome. For major changes, please open an issue first to discuss what you would like to change.

Please make sure to update tests as appropriate.

## License
[MIT](https://choosealicense.com/licenses/mit/)
