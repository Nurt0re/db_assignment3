.PHONY: help up down restart logs ps connect exec clean rebuild migrate seed update delete simple complex derived view runserver test-db install truncate

# Load environment variables from .env file
include .env
export

# Default target
help:
	@echo "Available commands:"
	@echo ""
	@echo "Database commands:"
	@echo "  make up        - Start the database container"
	@echo "  make down      - Stop and remove containers"
	@echo "  make connect   - Connect to PostgreSQL database"
	@echo "  make clean     - Stop containers and remove volumes (deletes all data)"
	@echo "  make migrate   - Run schema migration (create tables)"
	@echo "  make insert    - Insert sample data into database"
	@echo "  make truncate  - Remove all data from tables (keeps structure)"
	@echo "  make update    - Run update queries"
	@echo "  make delete    - Run delete queries"
	@echo ""
	@echo "Query commands:"
	@echo "  make simple    - Run simple queries"
	@echo "  make complex   - Run complex queries"
	@echo "  make derived   - Run derived attribute query"
	@echo "  make view      - Create and query view operation"
	@echo "  make execute_view   - Execute view query"
	@echo ""
	@echo "Django Web Application commands:"
	@echo "  make install   - Install Python dependencies"
	@echo "  make runserver - Run Django development server"
	@echo "  make test-db   - Test database connection with SQLAlchemy"


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
	PGPASSWORD=$(DB_PASSWORD) psql -h $(DB_HOST).oregon-postgres.render.com -U $(DB_USER) -d $(DB_NAME)

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
	PGPASSWORD=$(DB_PASSWORD) psql -h $(DB_HOST).oregon-postgres.render.com -U $(DB_USER) -d $(DB_NAME) < schema.sql
	@echo "Schema migration completed."

# Insert sample data into database
insert:
	@echo "Inserting sample data..."
	PGPASSWORD=$(DB_PASSWORD) psql -h $(DB_HOST).oregon-postgres.render.com -U $(DB_USER) -d $(DB_NAME) < queries/insert_data.sql
	@echo "Sample data inserted."

# Truncate all tables (remove all data but keep structure)
truncate:
	@echo "Truncating all tables..."
	PGPASSWORD=$(DB_PASSWORD) psql -h $(DB_HOST).oregon-postgres.render.com -U $(DB_USER) -d $(DB_NAME) < queries/truncate_tables.sql
	@echo "All tables truncated."

# Run update queries
update:
	@echo "Running update queries..."
	PGPASSWORD=$(DB_PASSWORD) psql -h $(DB_HOST).oregon-postgres.render.com -U $(DB_USER) -d $(DB_NAME) < queries/update_queries.sql
	@echo "Update queries completed."

# Run delete queries
delete:
	@echo "Running delete queries..."
	PGPASSWORD=$(DB_PASSWORD) psql -h $(DB_HOST).oregon-postgres.render.com -U $(DB_USER) -d $(DB_NAME) < queries/delete_queries.sql
	@echo "Delete queries completed."

# Run simple queries 
simple:
	@echo "Running simple queries..."
	PGPASSWORD=$(DB_PASSWORD) psql -h $(DB_HOST).oregon-postgres.render.com -U $(DB_USER) -d $(DB_NAME) < queries/simple_queries.sql
	@echo "Simple queries completed."

# Run complex queries 
complex:
	@echo "Running complex queries..."
	PGPASSWORD=$(DB_PASSWORD) psql -h $(DB_HOST).oregon-postgres.render.com -U $(DB_USER) -d $(DB_NAME) < queries/complex_queries.sql
	@echo "Complex queries completed."

# Run derived attribute query 
derived:
	@echo "Running derived attribute query..."
	PGPASSWORD=$(DB_PASSWORD) psql -h $(DB_HOST).oregon-postgres.render.com -U $(DB_USER) -d $(DB_NAME) < queries/derived_attribute_query.sql
	@echo "Derived attribute query completed."

# Create and query view operation
view:
	@echo "Creating and querying view..."
	PGPASSWORD=$(DB_PASSWORD) psql -h $(DB_HOST).oregon-postgres.render.com -U $(DB_USER) -d $(DB_NAME) < queries/create_view.sql
	@echo "View operation completed."

execute_view:
	@echo "Executing view query..."
	PGPASSWORD=$(DB_PASSWORD) psql -h $(DB_HOST).oregon-postgres.render.com -U $(DB_USER) -d $(DB_NAME) < queries/view_operation.sql
	@echo "View query executed."

# Install Python dependencies
install:
	@echo "Installing Python dependencies..."
	pip3 install -r requirements.txt
	@echo "Dependencies installed successfully."

# Run Django development server
runserver:
	@echo "Starting Django development server..."
	@echo "Access the application at http://127.0.0.1:8000/"
	python3 manage.py runserver

# Test database connection
test-db:
	@echo "Testing database connection..."
	python3 -c "from database import test_connection; test_connection()"