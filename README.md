### Auto-creation Ampere A1 in the Oracle Cloud

Inspired by chacuavip10 and the [article](https://www.hintdesk.com/2022/01/15/how-to-create-a-free-oracle-vps-with-python-script-out-of-capacity/).

## Quick start

1. Read the article above
2. Register an API key*
3. Start to create an instance in the control panel*
4. Catch the request*
5. Put your key to `config`
6. Fill two files with your request data:
   1. config/config
   2. .env.example
7. Run `docker-compose up`

`* you can get more information from the article`

## ENVs
- `OCPUS=4` - CPU's cores number (from request)
- `MEMORY_IN_GBS=24` - RAM's quantity (from request)
- `WAIT_INTERVAL=30` - Time interval between attempts (from request)
- `INSTANCE_DISPLAY_NAME=instance-xxx` - Instance's name (from request)
- `COMPARTMENT_ID=ocid1.xxx` - Compartment ID (from request)
- `DOMAIN=FIiW:xxx` - Your domain (from request)
- `IMAGE_ID=ocid1.xxx` - OS image (from request)
- `SUBNET_ID=ocid1.xxx` - Your network ID (from request)
---
- `SSH_KEY=ssh-rsa xxx` - Public ssh key
- `PATH_TO_CONFIG_FILE=/config/config` - Path to OCI config
---
- `BOT_ID=xxx` - Telegram bot ID (unnecessary)
- `CHAT_ID=xxx` - Telegram chat ID (unnecessary)
