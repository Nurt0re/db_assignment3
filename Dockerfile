# Dockerfile for PostgreSQL with custom schema
FROM postgres:16-alpine

# Set environment variables
ENV POSTGRES_DB=caregiving_db
ENV POSTGRES_USER=postgres
ENV POSTGRES_PASSWORD=postgres

# Copy the schema file to the initialization directory
# PostgreSQL will automatically execute .sql files in this directory
COPY schema.sql /docker-entrypoint-initdb.d/

# Expose PostgreSQL port
EXPOSE 5432
