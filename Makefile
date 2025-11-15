.PHONY: help up down restart logs ps connect exec clean rebuild migrate seed update delete

# Default target
help:
	@echo "Available commands:"
	@echo "  make up        - Start the database container"
	@echo "  make down      - Stop and remove containers"
	@echo "  make connect   - Connect to PostgreSQL database"
	@echo "  make clean     - Stop containers and remove volumes (deletes all data)"
	
	@echo "  make migrate   - Run schema migration (create tables)"
	@echo "  make insert      - Insert sample data into database"
	@echo "  make update    - Run update queries"
	@echo "  make delete    - Run delete queries"

# Start the database container
up:
	@echo "Starting database container..."
	docker-compose up -d
	@echo "Database is starting. Use 'make logs' to check progress."

# Stop and remove containers
down:
	@echo "Stopping database container..."
	docker-compose down
	@echo "Database stopped."


# Connect to PostgreSQL database
connect:
	@echo "Connecting to PostgreSQL database..."
	docker exec -it caregiving_db psql -U postgres -d caregiving_db

# Stop containers and remove volumes (deletes all data)
clean:
	@echo "WARNING: This will delete all database data!"
	@read -p "Are you sure? [y/N] " -n 1 -r; \
	echo; \
	if [[ $$REPLY =~ ^[Yy]$$ ]]; then \
		docker-compose down -v; \
		echo "Database stopped and all data removed."; \
	else \
		echo "Operation cancelled."; \
	fi


# Run schema migration (create tables)
migrate:
	@echo "Running schema migration..."
	docker exec -i caregiving_db psql -U postgres -d caregiving_db < schema.sql
	@echo "Schema migration completed."

# Insert sample data into database
insert:
	@echo "Inserting sample data..."
	docker exec -i caregiving_db psql -U postgres -d caregiving_db < queries/insert_data.sql
	@echo "Sample data inserted."

# Run update queries
update:
	@echo "Running update queries..."
	docker exec -i caregiving_db psql -U postgres -d caregiving_db < queries/update_queries.sql
	@echo "Update queries completed."

# Run delete queries
delete:
	@echo "Running delete queries..."
	docker exec -i caregiving_db psql -U postgres -d caregiving_db < queries/delete_queries.sql
	@echo "Delete queries completed."
