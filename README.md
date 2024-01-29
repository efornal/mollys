# mollys
Administration request for internal user accounts to the organization. The user accounts are relationated with ldap account


### Docker
* Volume Creation
```bash
docker volume create mollys_app
docker volume create mollys_pgdata
```
* Application settings
```bash
cp .env.tpl .env.dev
```
configuration details in /mollys/settings.py
* Environment creation with docker-compose 
```bash
docker-compose up
```
