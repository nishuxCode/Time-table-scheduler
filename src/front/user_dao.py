import mysql.connector

class UserDao:
    
    @staticmethod
    def get_connection():
        con = None
        try:
            # Update these credentials to match your MySQL setup
            con = mysql.connector.connect(
                host="localhost",
                user="root",
                password="Nishu@124",
                database="test"
            )
        except Exception as e:
            print(f"Connection Error: {e}")
        return con

    @staticmethod
    def validate(username, password):
        status = False
        con = None
        cursor = None
        try:
            con = UserDao.get_connection()
            if con and con.is_connected():
                cursor = con.cursor()
                query = "SELECT id FROM users WHERE username = %s AND password = %s"
                cursor.execute(query, (username, password))
                if cursor.fetchone():
                    status = True
                
                # ✅ FIX 1: Ensure all results are consumed
                # Iterate over any remaining results to clear the buffer
                for _ in cursor:
                    pass 
                    
        except Exception as e:
            print(f"Validation Error: {e}")
        finally:
            if cursor: cursor.close()
            if con and con.is_connected(): con.close()
        return status

    @staticmethod
    def register(username, password, email, country):
        status = False
        con = None
        cursor = None
        try:
            con = UserDao.get_connection()
            if con and con.is_connected():
                cursor = con.cursor()
                query = "INSERT INTO users (username, password, country, email) VALUES (%s, %s, %s, %s)"
                cursor.execute(query, (username, password, country, email))
                con.commit()
                if cursor.rowcount > 0:
                    status = True
                    
                # ✅ FIX 2: Ensure all results are consumed even after INSERT
                for _ in cursor:
                    pass

        except Exception as e:
            print(f"Registration Error: {e}")
        finally:
            if cursor: cursor.close()
            if con and con.is_connected(): con.close()
        return status
