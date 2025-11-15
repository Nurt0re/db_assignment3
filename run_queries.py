import os
import psycopg2
from psycopg2 import sql
from dotenv import load_dotenv

# Load environment variables from .env file
load_dotenv()

# Database connection parameters
DB_CONFIG = {
    'host': os.getenv('DB_HOST', 'localhost'),
    'port': os.getenv('DB_PORT', '5432'),
    'database': os.getenv('DB_NAME', 'caregiving_db'),
    'user': os.getenv('DB_USER', 'postgres'),
    'password': os.getenv('DB_PASSWORD', 'postgres')
}

# SQL files to execute
SQL_FILES = {
    '1': {'name': 'Schema Migration', 'file': 'schema.sql'},
    '2': {'name': 'Insert Data', 'file': 'queries/insert_data.sql'},
	'3': {'name': 'Update Queries', 'file': 'queries/update_queries.sql'},
    '4': {'name': 'Delete Queries', 'file': 'queries/delete_queries.sql'},
    '5': {'name': 'Simple Queries', 'file': 'queries/simple_queries.sql'},
    '6': {'name': 'Complex Queries', 'file': 'queries/complex_queries.sql'},
    '7': {'name': 'Derived Attribute Query', 'file': 'queries/derived_attribute_query.sql'},
    '8': {'name': 'Create View', 'file': 'queries/create_view.sql'},
    '9': {'name': 'View Operation', 'file': 'queries/view_operation.sql'},

}

def connect_db():
    """Establish database connection"""
    try:
        conn = psycopg2.connect(**DB_CONFIG)
        return conn
    except psycopg2.Error as e:
        print(f"Error connecting to database: {e}")
        return None

def execute_sql_file(cursor, filepath):
    """Execute SQL commands from a file and display results"""
    try:
        with open(filepath, 'r') as f:
            sql_content = f.read()
            
        # Split into individual statements (handling semicolons)
        statements = [stmt.strip() for stmt in sql_content.split(';') if stmt.strip()]
        
        results = []
        for statement in statements:
            # Skip comments
            if statement.startswith('--') or not statement:
                continue
                
            try:
                cursor.execute(statement)
                
                # Try to fetch results if it's a SELECT query
                if statement.strip().upper().startswith('SELECT') or \
                   statement.strip().upper().startswith('WITH'):
                    rows = cursor.fetchall()
                    colnames = [desc[0] for desc in cursor.description] if cursor.description else []
                    results.append({
                        'query': statement[:100] + '...' if len(statement) > 100 else statement,
                        'columns': colnames,
                        'rows': rows,
                        'count': len(rows)
                    })
            except psycopg2.Error as e:
                print(f"Error in statement: {e}")
                continue
        
        return results
    except FileNotFoundError:
        print(f"Error: File '{filepath}' not found")
        return None
    except Exception as e:
        print(f"Error reading file: {e}")
        return None

def display_menu():
    """Display menu of available SQL files"""
    print("\n" + "="*50)
    print("DATABASE QUERY EXECUTOR")
    print("="*50)
    print("\nAvailable SQL files:")
    for key, value in SQL_FILES.items():
        print(f"  {key}. {value['name']} ({value['file']})")
    print("  0. Exit")
    print("  a. Run all queries in order")
    print("="*50)

def run_query(choice, conn):
    """Run selected query"""
    if choice == '0':
        return False
    
    if choice == 'a':
        print("\nRunning all queries in order...")
        for key in sorted(SQL_FILES.keys()):
            run_single_query(key, conn)
        return True
    
    if choice in SQL_FILES:
        run_single_query(choice, conn)
        return True
    else:
        print("Invalid choice. Please try again.")
        return True

def format_table(columns, rows):
    """Format query results as a table"""
    if not rows:
        return "No results found."
    
    # Calculate column widths
    col_widths = []
    for i, col in enumerate(columns):
        max_width = len(str(col))
        for row in rows:
            if i < len(row):
                max_width = max(max_width, len(str(row[i])))
        col_widths.append(min(max_width, 50))  # Cap at 50 chars
    
    # Create header
    header = " | ".join(str(col).ljust(col_widths[i]) for i, col in enumerate(columns))
    separator = "-+-".join("-" * width for width in col_widths)
    
    # Create rows
    table_rows = []
    for row in rows:
        formatted_row = " | ".join(
            str(row[i] if i < len(row) else "").ljust(col_widths[i])[:col_widths[i]] 
            for i in range(len(columns))
        )
        table_rows.append(formatted_row)
    
    return f"\n{header}\n{separator}\n" + "\n".join(table_rows)

def run_single_query(choice, conn):
    """Execute a single query file"""
    query_info = SQL_FILES[choice]
    print(f"\n{'='*50}")
    print(f"Executing: {query_info['name']}")
    print(f"File: {query_info['file']}")
    print('='*50)
    
    cursor = conn.cursor()
    try:
        results = execute_sql_file(cursor, query_info['file'])
        
        if results is not None:
            conn.commit()
            print(f"✓ Successfully executed {query_info['name']}")
            
            # Display results for each SELECT query
            for i, result in enumerate(results, 1):
                if result['rows']:
                    print(f"\n--- Query {i} Results ({result['count']} rows) ---")
                    print(format_table(result['columns'], result['rows']))
                else:
                    print(f"\n--- Query {i}: No results ---")
            
            # Show affected rows for non-SELECT queries
            if not results:
                print(f"Rows affected: {cursor.rowcount}")
        else:
            conn.rollback()
            print(f"✗ Failed to execute {query_info['name']}")
    except Exception as e:
        conn.rollback()
        print(f"✗ Error: {e}")
    finally:
        cursor.close()

def main():
    """Main function"""
    print("Connecting to database...")
    conn = connect_db()
    
    if not conn:
        print("Failed to connect to database. Check your .env configuration.")
        return
    
    print(f"✓ Connected to {DB_CONFIG['database']} at {DB_CONFIG['host']}:{DB_CONFIG['port']}")
    
    try:
        while True:
            display_menu()
            choice = input("\nEnter your choice: ").strip().lower()
            
            if not run_query(choice, conn):
                break
    
    except KeyboardInterrupt:
        print("\n\nExiting...")
    finally:
        conn.close()
        print("Database connection closed.")

if __name__ == "__main__":
    main()
