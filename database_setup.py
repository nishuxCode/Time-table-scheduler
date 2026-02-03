import mysql.connector

def create_database():
    try:
        # Connect to MySQL server
        # Ensure these credentials match your local MySQL setup
        con = mysql.connector.connect(
            host="localhost",
            user="root",
            password="Nishu@124" 
        )
        cursor = con.cursor()
        
        # Create database
        cursor.execute("CREATE DATABASE IF NOT EXISTS test")
        cursor.execute("USE test")
        
        # Create users table
        cursor.execute("""
        CREATE TABLE IF NOT EXISTS users (
            id int(4) NOT NULL AUTO_INCREMENT,
            username varchar(50) NOT NULL,
            password varchar(50) NOT NULL,
            country varchar(50) NOT NULL,
            email varchar(50) NOT NULL,
            PRIMARY KEY (id)
        ) ENGINE=InnoDB DEFAULT CHARSET=latin1;
        """)
        
        # Insert default user if not exists
        cursor.execute("SELECT * FROM users WHERE username = 'pranav'")
        if not cursor.fetchone():
            cursor.execute("""
            INSERT INTO users (username, password, country, email) VALUES
            ('pranav', 'khurana', 'india', 'pranavkhurana96@gmail.com');
            """)
            con.commit()
            print("Database 'test' and table 'users' created successfully with default user.")
        else:
            print("Database and user already exist.")
            
        cursor.close()
        con.close()
    except Exception as e:
        print(f"Error: {e}")

if __name__ == "__main__":
    create_database()