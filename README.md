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

3. Now it is possible to run the project inside the Docker container:
    ```shell
    docker compose up
    ```
   When containers are up server starts at [http://0.0.0.0:8080](http://0.0.0.0:8080). You can open it in your browser.

4. The server can be configured to have the Synertau templates using Postman:

   Please read README.md in the `postman` folder.
