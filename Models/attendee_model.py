# libs:
from datetime import datetime

# scripts:
from Config.config import get_connection

# building the class for attendees :
class Attendee:
    @staticmethod
    # function for add an attendee:
    def add_attendee(username, phone, amount, num_persons, email, qr_code_path):
        print("username: {}".format(username))
        print("phone: {}".format(phone))
        print("amount: {}".format(amount))
        print("num_persons: {}".format(num_persons))
        print("email: {}".format(email))
        print("qr_code_path: {}".format(qr_code_path))

        connect = get_connection()
        cursor = connect.cursor()

        # checking if the current records for attendee is already exist in data base:
        cursor.execute('SELECT * FROM attendees WHERE phone = ?', (phone,))
        existing_attendee = cursor.fetchone()

        # add current time of execute:
        current_time = datetime.now().strftime("%Y-%m-%d %H:%M:%S")

        if not existing_attendee:
            cursor.execute(''' 
                INSERT INTO attendees (username, phone, amount, num_persons, email, qr_code_path, user_created_date, user_updated_date)
                VALUES (?, ?, ?, ?, ?, ?, ?, ?)        
            ''', (username, phone, amount, num_persons, email, qr_code_path, current_time, current_time))

        # initializing:
        connect.commit()
        connect.close()

    @staticmethod
    # updating attendee_db:
    def updating_attendee(username, phone, amount, num_persons, email, qr_code_path, attendee_id):
        print("username: {}".format(username))
        print("phone: {}".format(phone))
        print("amount: {}".format(amount))
        print("num_persons: {}".format(num_persons))
        print("email: {}".format(email))
        print("qr_code_path: {}".format(qr_code_path))
        print("attendee_id: {}".format(attendee_id))

        connect = get_connection()
        cursor = connect.cursor()

        # Check if attendee already exists
        cursor.execute('SELECT * FROM attendees WHERE id = ?', (attendee_id,))
        existing_attendee = cursor.fetchone()

        # recodr current time:
        current_time = datetime.now().strftime("%Y-%m-%d %H:%M:%S")

        if existing_attendee:
            # Update the existing attendee
            cursor.execute('''
                UPDATE attendees
                SET username = ?, phone = ?, amount = ?, num_persons = ?, email = ?, qr_code_path = ?, user_updated_date = ?
                WHERE id = ?
            ''', (username, phone, amount, num_persons, email, qr_code_path, current_time, attendee_id))

        connect.commit()
        connect.close()

    @staticmethod
    # deleting an existing record:
    def delete_attendee(phone):
        """Deletes an attendee from the database by phone number."""
        conn = get_connection()
        cursor = conn.cursor()
        cursor.execute('DELETE FROM attendees WHERE phone = ?', (phone,))
        conn.commit()
        conn.close()

    @staticmethod
    #get an attendee reocord by their phone details:
    def get_by_phonr(phone):
        """Retrieves an attendee's details by phone number."""
        conn = get_connection()
        cursor = conn.cursor()
        cursor.execute('SELECT * FROM attendees WHERE phone = ?', (phone,))
        attendee = cursor.fetchone()
        conn.close()
        return attendee
    
    @staticmethod
    # geeting all the current attendees:
    def get_all_attendees():
        conn = get_connection()
        cursor = conn.cursor()
        cursor.execute(''' SELECT id, username, phone, amount, num_persons, email, qr_code_path, attended, user_created_date, user_updated_date FROM attendees''')
        attendees = cursor.fetchall()
        conn.close()
        return attendees
    
    @staticmethod
    # marking a random attendee:
    def mark_attendance(phone):
        conn = get_connection()
        cursor = conn.cursor()
        
        current_time = datetime.dtrftime("%Y-%m-%d %H:%M:%S")
        cursor.execute('UPDATE attendees SET attended = 1, user_updated_date = ? WHERE phone = ?', (current_time, phone))
        conn.commit()
        conn.close()

