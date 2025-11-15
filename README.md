# Caregiving Platform Database

PostgreSQL database setup using Docker and Docker Compose.

## Prerequisites

- Docker
- Docker Compose

## Quick Start

1. **Build and start the database:**

   ```bash
   docker-compose up -d
   ```

2. **Check if the database is running:**

   ```bash
   docker-compose ps
   ```

3. **Connect to the database:**
   ```bash
   docker exec -it caregiving_db psql -U postgres -d caregiving_db
   ```

## Database Configuration

- **Database Name:** `caregiving_db`
- **Username:** `postgres`
- **Password:** `postgres`
- **Port:** `5432`
- **Host:** `localhost` (from host machine)

## Useful Commands

### Start the database

```bash
docker-compose up -d
```

### Stop the database

```bash
docker-compose down
```

### Stop and remove volumes (clears all data)

```bash
docker-compose down -v
```

### View logs

```bash
docker-compose logs -f postgres
```

### Access PostgreSQL CLI

```bash
docker exec -it caregiving_db psql -U postgres -d caregiving_db
```

### Run SQL file

```bash
docker exec -i caregiving_db psql -U postgres -d caregiving_db < your_file.sql
```

## Connection String

```
postgresql://postgres:postgres@localhost:5432/caregiving_db
```

## Schema Tables

- `user` - User accounts
- `caregiver` - Caregiver profiles
- `member` - Member profiles
- `address` - Member addresses
- `job` - Job postings
- `job_application` - Job applications
- `appointment` - Appointments between caregivers and members
