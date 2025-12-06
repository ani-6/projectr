#!/bin/bash

# ---------- Configuration ----------
# 1. Define path to .env (One directory up from script)
SCRIPT_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"
ENV_FILE="$SCRIPT_DIR/../.env"

# 2. Check if .env exists and Load it
if [ -f "$ENV_FILE" ]; then
    set -a
    source "$ENV_FILE"
    set +a
else
    echo -e "\033[0;31m❌ Error: .env file not found at $ENV_FILE\033[0m"
    exit 1
fi

# ---------- Variable Mapping ----------
# Map .env variables to script variables

# 1. Handle DB_NAME
# If DB_NAME is a comma-separated list in .env (e.g., "db1,db2"), we take the FIRST one as the default target.
IFS=',' read -r -a DB_LIST <<< "$DB_NAME"
TARGET_DB="${DB_LIST[0]}"

# 2. Map Password, Host, Port
DB_HOST="${DB_HOST:-localhost}"
DB_USER="${DB_USER}"
DB_PASS="${DB_PASSWORD}"       # Mapping .env DB_PASSWORD to script DB_PASS
DB_PORT="${DB_PORT:-3306}"     # Default to 3306

# 3. Define Backup Directory (Fallback if not in .env)
BACKUP_DIR="backups"
BACKUP_PATH="${SCRIPT_DIR}/${BACKUP_DIR}"

# ---------- Function: Restore Backup ----------
restore_backup() {
    echo "🔍 Looking for latest backup in: $BACKUP_PATH"

    # Find the latest SQL file
    LATEST_BACKUP=$(ls -t "$BACKUP_PATH"/*.sql 2>/dev/null | head -n 1)

    if [[ -z "$LATEST_BACKUP" ]]; then
        echo "⚠️  No backup files found in $BACKUP_PATH"
        exit 1
    fi

    echo "📦 Latest backup found: $LATEST_BACKUP"

    # Check if we have a target database from .env
    if [[ -z "$TARGET_DB" ]]; then
        echo "❌ Error: DB_NAME not found in .env file."
        exit 1
    fi

    echo "🎯 Target database: $TARGET_DB"

    # 1. Drop and Recreate Database
    echo "🧨 Dropping and recreating database: $TARGET_DB..."
    
    # Added -P for Port
    mysql -h "$DB_HOST" -P "$DB_PORT" -u "$DB_USER" -p"$DB_PASS" -e "DROP DATABASE IF EXISTS \`$TARGET_DB\`; CREATE DATABASE \`$TARGET_DB\`;"
    
    if [[ $? -ne 0 ]]; then
        echo "❌ Failed to drop/recreate the database $TARGET_DB"
        exit 1
    fi

    # 2. Restore SQL File
    echo "🔄 Restoring backup from $LATEST_BACKUP..."

    # Added -P for Port
    mysql -h "$DB_HOST" -P "$DB_PORT" -u "$DB_USER" -p"$DB_PASS" "$TARGET_DB" < "$LATEST_BACKUP"
    
    if [[ $? -eq 0 ]]; then
        echo "✅ Database $TARGET_DB restored successfully."
    else
        echo "❌ Failed to restore the database $TARGET_DB."
        exit 1
    fi
}

# Run the function
restore_backup