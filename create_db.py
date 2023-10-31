import psycopg2
from psycopg2 import sql

# Replace these with your database configuration
dbname = "solita"
user = "trevor"
password = "mypassword"

# Establish a connection to the PostgreSQL server
conn = psycopg2.connect(
    dbname=dbname,
    user=user,
    password=password
)

# Create a cursor object to interact with the database
cursor = conn.cursor()

# Create a new PostgreSQL database
# try:
#    cursor.execute(sql.SQL("CREATE DATABASE {}").format(sql.Identifier(dbname)))
#    print("Database created successfully.")
# except psycopg2.Error as e:
#    print("Error creating the database:", e)
# Execute a command: create datacamp_courses table
cursor.execute(sql.SQL("""CREATE TABLE solita.datacamp_courses(
            course_id SERIAL PRIMARY KEY,
            course_name VARCHAR (50) UNIQUE NOT NULL,
            course_instructor VARCHAR (100) NOT NULL,
            topic VARCHAR (20) NOT NULL);
            """))
#
cursor.execute(sql.SQL("SELECT * FROM solita.datacamp_courses;"))
# Close the cursor and connection
cursor.close()
conn.close()
