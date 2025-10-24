DB_NAME=postgres
DB_USER=postgres
DB_HOST=localhost
DB_PORT=5432
DB_PASSWORD=mypassword

SCHEMA=schema/schema.sql


.PHONY: db-init
db-init:
	@echo "Creating database $(DB_NAME)..."
	PGPASSWORD=$(DB_PASSWORD) psql -U $(DB_USER) -h $(DB_HOST) -p $(DB_PORT) -d postgres -c "CREATE DATABASE $(DB_NAME);"
	#$(call psql_exec, "CREATE DATABASE $(DB_NAME);")
	@echo "Database $(DB_NAME) created."

## Create tables from schema.sql
.PHONY: db-create-schema
db-create-schema:
	@echo "Applying schema..."
	PGPASSWORD=$(DB_PASSWORD) psql -U $(DB_USER) -h $(DB_HOST) -p $(DB_PORT) -d $(DB_NAME) -f $(SCHEMA)

## Drop database
.PHONY: db-drop
db-drop:
	@echo "Dropping database..."
	PGPASSWORD=$(DB_PASSWORD) psql -U $(DB_USER) -h $(DB_HOST) -p $(DB_PORT) -d postgres -c "DROP DATABASE IF EXISTS $(DB_NAME);"


.PHONE: db-build-db
db-build-db:
	@echo "Initializing database $(DB_NAME)"
	$(MAKE) db-init

	@echo "$(DB_NAME) initialized successfully"
	$(MAKE) db-create-schema
	@echo "Schema created successfully"
