#!/bin/bash

# ---------- Configuration ----------
__FILE__=$0

# 1. Define path to .env (One directory up from script)
ENV_FILE="$(dirname "$0")/../.env"

# 2. Check if .env exists and Load it
if [ -f "$ENV_FILE" ]; then
    # 'set -a' automatically exports variables defined in the sourced file
    set -a
    source "$ENV_FILE"
    set +a
else
    echo -e "\033[0;31m❌ Error: .env file not found at $ENV_FILE\033[0m"
    exit 1
fi

# ---------- Variable Mapping ----------
# Map .env variables to the specific variable names this script uses

# 1. Handle DB_NAME (Convert single string from .env to Array for the script loop)
# Use Internal Field Separator (IFS) to handle comma-separated lists if you ever have them, 
# or just wrap the single value in parens.
IFS=',' read -r -a DB_NAMES <<< "$DB_NAME"

# 2. Map Password and Defaults
DB_HOST="${DB_HOST:-localhost}"
DB_USER="${DB_USER}"
DB_PASS="${DB_PASSWORD}"       # Mapping .env DB_PASSWORD to script DB_PASS
DB_PORT="${DB_PORT:-3306}"     # Default to 3306 if not set

# 3. Define Backup Directory (Since it wasn't in your .env snippet)
BACKUP_DIR="backups" 

# ---------- Colors ----------
Green='\033[0;32m'
Yellow='\033[1;33m'
Red='\033[0;31m'
Cyan='\033[0;36m'
Color_Off='\033[0m'

# ---------- Settings ----------
script_dir=$(dirname "$(realpath "$0")")
FULL_DIR_PATH="$script_dir/$BACKUP_DIR"

# ---------- Create Backup Directory ----------
bkp_directory() {
    echo -e "${Cyan}Checking backup directory...${Color_Off}"
    if [ ! -d "$FULL_DIR_PATH" ]; then
        mkdir -p "$FULL_DIR_PATH"
        echo -e "${Green}✔ Directory '$FULL_DIR_PATH' created.${Color_Off}"
    else
        echo -e "${Yellow}⚠ Directory '$FULL_DIR_PATH' already exists.${Color_Off}"
    fi
}

# ---------- Create Backup ----------
create_backup() {
    DATE=$(date -u +"%Y%m%d_%H%M%S")
    echo -e "\n${Cyan}Starting database backup using UTC time...${Color_Off}"

    for DB_CURRENT in "${DB_NAMES[@]}"; do
        BACKUP_FILE="$FULL_DIR_PATH/${DB_CURRENT}_$DATE.sql"
        echo -e "${Cyan}⏳ Backing up '${DB_CURRENT}' on Host: ${DB_HOST}...${Color_Off}"
        
        # Added -P for Port based on your .env
        mysqldump -h "${DB_HOST}" -P "${DB_PORT}" -u "${DB_USER}" -p"${DB_PASS}" --routines --events --triggers "${DB_CURRENT}" > "$BACKUP_FILE"

        if [ $? -eq 0 ]; then
            echo -e "${Green}✔ Backup successful: ${BACKUP_FILE}${Color_Off}\n"
        else
            echo -e "${Red}❌ Error: Backup of ${DB_CURRENT} failed.${Color_Off}\n"
        fi
    done
}

# ---------- Run Script ----------
echo -e "${Cyan}========== MySQL Backup Script ==========${Color_Off}"
bkp_directory
create_backup
echo -e "${Cyan}========== Backup Process Completed ==========${Color_Off}\n"