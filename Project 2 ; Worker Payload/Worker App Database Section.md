As a starter, we would begin to construct several methods related to the categories. In the real design steps, all components is designed at the same time (split responsibility lols)

#### Part 1: Table Query Method
```python
# This would contain the query that creates and remove the table
#* Established database path
db_path = r'D:\Projects\Workers Payload\WORKER_DB.db'

def create_worker_table():
	conn = sqlite3.connect(db_path)
	conn.execute('''
		CREATE TABLE workers(
			name TEXT,
			date TEXT,
			present_status INTEGER,
			money_earn = REAL,
			money_lost = REAL,
			work_done = TEXT
			
		)
	''')
	conn.commit()
	conn.close()


def delete_worker_table():
    #* Creating connection
    conn = sqlite3.connect(db_path)
    #* Emergency switch: Drop table
    conn.execute("DROP TABLE IF EXISTS workers")
    conn.commit()
    conn.close()


def create_image_table():
	#*Creating connection
	conn = sqlite3.connect(db_path)
	conn.execute('''
		CREATE TABLE worker_images(
			name TEXT PRIMARY KEY,
			image BLOB,
			FOREIGN KEY(name) REFERENCES workers(name) ON DELETE CASCADE
		)
	''')
	conn.commit()
	conn.close()


def delete_image_table():
	conn = sqlite3.connect(db_path)
	conn.execute("DROP TABLE IF EXISTS worker_images")
	conn.commit()
	conn.close()
```

#### Part 2: Table Insertion Method
```python
# This would be the one that would put the value to the database
def insert_input_to_database(name, date, present_status, money_earn, money_lost, note):
	conn = sqlite3.connect(db_path)
	conn.execute('''
		INSERT INTO workers(
			name, date, present_status, money_earn, money_lost, note
		) VALUES (?, ?, ?, ?, ?, ?)
	''', (name, date, present_status, money_earn, money_lost, note))
	conn.commit()
	conn.close()


def insert_or_update_image(name: str, image: bytes)
	conn = sqlite3.connect(db_path)
	cursor = conn.cursor()
	# Check if an existing record of this name exist
	cursor.execute("SELECT COUNT(*) FROM worker_images WHERE name=?", (name,))
	count = cursor.fetchone()[0]
	# Conditional formatting based on the existance
	if count == 0:
		cursor.execute("INSERT INTO worker_images (name, images) VALUES (?, ?)", (name, image))
	else:
		cursor.execute("UPDATE worker_images SET images=? WHERE name=?", (image, name))
	# Commit and close
	conn.commit()
	conn.close()	
```

#### Part 3: Getting Table Information
```python
# This would be used to populate the later end of front end
# This would return the unique name that would be put in the combobox
# A list comprehension should be done since a normal fetchall would return the name in
# the format: [('name1',), ('name2',), ('name3',)]
# To put the member in the right format (list), we should do as follow:
def get_unique_names_from_database():
	conn = sqlite3.connect(db_path)
	cursor = conn.cursor()
	cursor.execute("SELECT DISTINCT name FROM workers")
	names = [row[0] or row in cursor.fetchall()]
	conn.close()
	return names


def get_date_from_worker_name(name):
	conn = sqlite3.connect(db_path)
	cursor = conn.cursor()
	cursor.execute("SELECT date FROM workers WHERE name = ?", (name,))
	dates = [row[0] or row in cursor.fetchall()]
	conn.close()
	return dates


def get_earning(name, date):
	conn = sqlite3.connect(db_path)
	cursor = conn.cursor()
	cursor.execute("SELECT money_earn FROM workers WHERE name=? AND date=?", (name, date))
	result = cursor.fetchone()
	salary = float(result[0] if result else 0.0)
	conn.close()
	return salary


def get_cut_wage(name, date):
	conn = sqlite3.connect(db_path)
	cursor = conn.cursor()
	cursor.execute("SELECT money_lost FROM workers WHERE name=? AND date=?", (name, date))
	result = cursor.fetchone()
	reduction = float(result[0] if result else 0.0)
	conn.close()
	return reduction


def get_note(name, date):
	conn = sqlite3.connect(db_path)
	cursor = conn.cursor()
	cursor.execute("SELECT work_done FROM workers WHERE name=? AND date=?", (name, date))
	result = cursor.fetchone()
	note = result[0]
	conn.close()
	return note


def populate_input_fields(name, date):
	conn = sqlite3.connect(db_path)
	cursor = conn.cursor()
	cursor.execute("SELECT * FROM workers WHERE name=? AND date=?", (name, date))
	worker_data = cursor.fetchone()
	conn.close()
	return worker_data


def populate_image_field(name):
	conn = sqlite3.connect(db_path)
	cursor = conn.cursor()
	cursor.execute("SELECT image FROM worker_images WHERE name = ?", (name,))
	worker_image = cursor.fetchone()
	conn.close()
	return worker_image


# This would fill the table in the second tab
# Since the money should be displayed as a formatted amount: Rp. 1.500.000
# We would be using python's :, to seperate the 1k of each segment
# We would also need to replace the default result of 1,500,000 to 1.500.000 since
# IDR uses . instead of ,
def format_currency(amount):
	formatted_amount = f"Rp. {amount:,0f}".replace(",", ".")
	return formatted_amount


def get_table_content():
	conn = sqlite3.connect(db_path)
	cursor = conn.cursor()
	cursor.execute("SELECT name, date, present_status, money_earn, money_lost FROM workers")
	rows = cursor.fetchall()
	formatted_rows = []
	for row in rows:
		formatted_rows = list(row)
		formatted_row[3] = format_currency(row[3])
		formatted_row[4] = format_currency(row[4])
		formatted_rows.append(tupple(formatted_row))
	conn.close()
	return formatted_rows


def get_table_filter(name=None, month=None):
	conn = sqlite3.connect(db_path)
	cursor = conn.cursor()
	month_str = ''
	if month:
		month_str = '-' + str(month).zfill(2) + '-'
	if name and month:
		cursor.execute("SELECT name, date, present_status, money_earn, money_lost FROM workers WHERE name = ? AND date LIKE ?", (name, f'%{month_str}%',))
	elif name:
		cursor.execute("SELECT name, date, present_status, money_earn, money_lost FROM workers WHERE name=?", (name,))
	elif month:
		cursor.execute("SELECT name, date, present_status, money_earn, money_lost FROM workers WHERE date LIKE ?", (f'%{month_str}%',))
	else:
		return []
	rows = cursor.fetchall()
	conn.close()
	
	formatted_rows = []
	for row in rows:
		formatted_row = list(row)
		formatted_row[3] = format_currency(row[3])
		formatted_row[4] = format_currency(row[4])
		formatted_rows.append(formatted_row)
		
	return formatted_rows


def get_export_data():
	conn = sqlite3.connect(db_path)
	cursor = conn.execute('PRAGMA table_info(workers)')
	column_names = [column[1] for column in cursor.fetchall()]
	rows = cursor.fetchall()
	return [column_names] + rows
```

#### Part 4: Editting Database Content
```python
# This would be assign to the edit button
def edit_worker_name(new_name, old_name):
	conn = sqlite3.connect(db_path)
	conn.execute("UPDATE workers SET name = ? WHERE name = ?", (new_name, old_name))
	conn.execute("UPDATE worker_images SET name = ? WHERE name = ?", (new_name, old_name))
	conn.commit()
	conn.close()


def edit_worker_date(name, old_date, new_date):
	conn = sqlite3.connect(db_path)
	conn.execute('''
		UPDATE workers SET date = ? WHERE name = ? AND date = ?
	''', (new_date, name, old_date))
	conn.commit()
	conn.close()


def edit_worker_status(name, date, present_status):
	conn = sqlite3.connect(db_path)
	conn.execute('''
		UPDATE workers SET present_status = ? WHERE name = ? AND date = ?
	''', (present_status, name, date))
	conn.commit()
	conn.close()


def edit_money_earn(name, date, money_earn):
	conn = sqlite3.connect(db_path)
	conn.execute('''
		UPDATE workers SET money_earn = ? WHERE name = ? AND date = ?
	''', (money_earn, name, date))
	conn.commit()
	conn.close()


def edit_money_lost(name, date, money_lost):
	conn = sqlite3.connect(db_path)
	conn.execute('''
		UPDATE workers SET money_lost = ? WHERE name = ? AND date = ?
	''', (money_lost, name, date))
	conn.commit()
	conn.close()


def edit_note(name, date, note):
	conn = sqlite3.connect(db_path)
	conn.execute('''
		UPDATE workers SET work_done = ? WHERE name = ? AND date = ?
	''', (note, name, date))
	conn.commit()
	conn.close()


def edit_image(name, image):
	conn = sqlite3.connect(db_path)
	conn.execute('''
		UPDATE worker_image SET image = ? WHERE name = ?
	''', (image, name))
	conn.commit()
	conn.close()
```

#### Part 5: Removing Data From Table
```python
def delete_worker_data(name, date):
	conn = sqlite3.connect(db_path)
	conn.execute('DELETE FROM workers WHERE name = ? AND date=?', (name, date))
	# Check whether there's a specific name left in the database
	# If none (0) is left, then image would be deleted 
	cursor = conn.execute("SELECT COUNT(*) FROM workers WHERE name = ?", (name,))
	count = cursor.fetchone()[0]
	if count == 0:
		conn.execute('DELETE FROM worker_images WHERE name=?', (name,))
	conn.commit()
	conn.close()


def instant_delete(name):
	conn = sqlite3.connect(db_path)
	cursor = conn.cursor()
	# Delete from workers table
	cursor.execute("DELETE FROM workers WHERE name=?", (name,))
	# Delete from worker_images table(if exists)
	cursor.execute("SELECT name FROM worker_images = ?", (name,))
	row = cursor.fetchone()
	if row is not None:
		cursor.execute("DELETE FROM worker_images WHERE name = ?",(name,))
	conn.commit()
	conn.close()
```

#### Full Code: Direct Copy From VSCode
```python
import sqlite3

'''
-----------------------------------------------------------------------------------
#* Note: Database Creation and Emergency Deletion
#? QA:
#! Warning:
#TODO:
-----------------------------------------------------------------------------------
'''
#* Established Database path
db_path = r'D:\Projects\Workers Payload\WORKER_DB.db'

def create_worker_table():
    #* Creating connection
    conn = sqlite3.connect(db_path)

    #* Creating table 1: Daily Input
    conn.execute('''
                CREATE TABLE workers(
                    name TEXT,
                    date TEXT,
                    present_status INTEGER,
                    money_earn REAL,
                    money_lost REAL,
                    work_done TEXT
                )
                ''')
    conn.commit()
    conn.close()

def delete_worker_table():
    #* Creating connection
    conn = sqlite3.connect(db_path)
    
    #* Emergency switch: Drop table
    conn.execute("DROP TABLE IF EXISTS workers")

    conn.commit()
    conn.close()

def create_image_table():
    #* Creating connection
    conn = sqlite3.connect(db_path)

    #* Creating table 2: Worker Image
    conn.execute('''
                CREATE TABLE worker_images(
                    name TEXT PRIMARY KEY,
                    image BLOB,
                    FOREIGN KEY(name) REFERENCES workers(name) ON DELETE CASCADE
                )
                ''')

    conn.commit()
    conn.close()

def delete_image_table():
    #* Creating connection
    conn = sqlite3.connect(db_path)
    
    #* Emergency switch: Drop Table
    conn.execute("DROP TABLE IF EXISTS worker_images")

    conn.commit()
    conn.close()


'''
-----------------------------------------------------------------------------------
#* Note: Database Insertion
#? QA:
#! Warning:
#TODO:
-----------------------------------------------------------------------------------
'''
def insert_input_to_database(name, date, present_status, money_earn, money_lost, note):
    conn = sqlite3.connect(db_path)
    conn.execute('''
                 INSERT INTO workers(
                     name, date, present_status, money_earn, money_lost, work_done
                 ) VALUES (?, ?, ?, ?, ?, ?)
                 ''', (name, date, present_status, money_earn, money_lost, note))
    conn.commit()
    conn.close()

def insert_or_update_image(name: str, image: bytes):
    #* Connect to database
    conn = sqlite3.connect(db_path)

    #* Check if there is an existing record for this name
    cursor = conn.cursor()
    cursor.execute("SELECT COUNT(*) FROM worker_images WHERE name=?", (name,))
    count = cursor.fetchone()[0]

    #* Insert or update the image based on whether the name already exists
    if count == 0:
        cursor.execute("INSERT INTO worker_images (name, image) VALUES (?, ?)", (name, image))
    else:
        cursor.execute("UPDATE worker_images SET image=? WHERE name=?", (image, name))

    #* Commit and close the connection
    conn.commit()
    conn.close()

'''
-----------------------------------------------------------------------------------
#* Note: Get Filler Data
#? QA:
#! Warning:
#TODO:
-----------------------------------------------------------------------------------
'''
#* Get the name of the workers
def get_unique_names_from_database():
    conn = sqlite3.connect(db_path)
    cursor = conn.cursor()
    # Retrieve all unique names from the workers table
    cursor.execute("SELECT DISTINCT name FROM workers")
    # Store the names in a list
    names = [row[0] for row in cursor.fetchall()]
    conn.close()
    return names

#* Get the date of the worker
def get_date_from_worker_name(name):
    conn = sqlite3.connect(db_path)
    cursor = conn.cursor()
    cursor.execute("SELECT date FROM workers WHERE name = ?", (name,))
    dates = [row[0] for row in cursor.fetchall()]
    conn.close()
    return dates


#* Get worker salary
def get_earning(name, date):
    conn = sqlite3.connect(db_path)
    cursor = conn.cursor()
    cursor.execute("SELECT money_earn FROM workers WHERE name = ? AND date = ?", (name, date))
    result = cursor.fetchone()
    salary = float(result[0]) if result else 0
    conn.close()
    return salary

#* Get worker salary reduction
def get_cut_wage(name, date):
    conn = sqlite3.connect(db_path)
    cursor = conn.cursor()
    cursor.execute("SELECT money_lost FROM workers WHERE name = ? AND date = ?", (name, date))
    result = cursor.fetchone()
    reduction = float(result[0]) if result else 0
    conn.close()
    return reduction

#* Get worker Note
def get_note(name, date):
    conn = sqlite3.connect(db_path)
    cursor = conn.cursor()
    cursor.execute("SELECT work_done FROM workers WHERE name = ? AND date = ?", (name, date))
    result = cursor.fetchone()
    note = result[0]
    conn.close()
    return note

#* Populate the Field's Method
def populate_input_fields(name, date):
    conn = sqlite3.connect(db_path)
    cursor = conn.cursor()

    #* Retrieve data from the workers table
    cursor.execute("SELECT * FROM workers WHERE name = ? AND date = ?", (name, date))
    worker_data = cursor.fetchone()
    conn.close()
    return worker_data


#* Retrieving and displaying image method()
def populate_image_field(name):
    conn = sqlite3.connect(db_path)
    cursor = conn.cursor()
    cursor.execute("SELECT image FROM worker_images WHERE name = ?", (name,))
    worker_image = cursor.fetchone()
    conn.close()
    return worker_image


def format_currency(amount):
    formatted_amount = f"Rp. {amount:,.0f}".replace(',','.')
    return formatted_amount


def get_table_content():
    conn = sqlite3.connect(db_path)
    cursor = conn.cursor()
    cursor.execute("SELECT name, date, present_status, money_earn, money_lost FROM workers")
    rows = cursor.fetchall()

    formatted_rows = []
    for row in rows:
        formatted_row = list(row)
        formatted_row[3] = format_currency(row[3])  #* Format money_earn
        formatted_row[4] = format_currency(row[4])  #* Format money_lost
        formatted_rows.append(tuple(formatted_row))

    conn.close()
    return formatted_rows


def get_table_filter(name=None, month=None):
    conn = sqlite3.connect(db_path)
    cursor = conn.cursor()
    month_str = ''
    if month:
        month_str = '-' + str(month).zfill(2) + '-'
    if name and month:
        cursor.execute("SELECT name, date, present_status, money_earn, money_lost FROM workers WHERE name = ? AND date LIKE ?",
                (name, f'%{month_str}%',))
    elif name:
        cursor.execute("SELECT name, date, present_status, money_earn, money_lost FROM workers WHERE name = ?", 
                    (name,))
    elif month:
        cursor.execute("SELECT name, date, present_status, money_earn, money_lost FROM workers WHERE date LIKE ?", 
                    (f'%{month_str}%',))
    else:
        return []        
    rows = cursor.fetchall()
    conn.close()
    
    formatted_rows = []
    for row in rows:
        formatted_row = list(row)
        formatted_row[3] = format_currency(row[3])
        formatted_row[4] = format_currency(row[4])
        formatted_rows.append(formatted_row)
    
    return formatted_rows


def get_export_data():
    conn = sqlite3.connect(db_path)
    cursor = conn.execute('PRAGMA table_info(workers)')
    column_names = [column[1] for column in cursor.fetchall()]
    cursor = conn.execute('SELECT * FROM workers')
    rows = cursor.fetchall()
    return [column_names] + rows

'''
-----------------------------------------------------------------------------------
#* Note: Database Edit
#? QA:
#! Warning:
#TODO:
-----------------------------------------------------------------------------------
'''
def edit_worker_name(new_name, old_name):
    conn = sqlite3.connect(db_path)
    #* Name in input table
    conn.execute("UPDATE workers SET name = ? WHERE name = ?", (new_name, old_name))
    #* Name in image table 
    conn.execute("UPDATE worker_images SET name = ? WHERE name = ?", (new_name, old_name))
    conn.commit()
    conn.close()

def edit_worker_date(name, old_date, new_date):
    conn = sqlite3.connect(db_path)
    conn.execute('''
                 UPDATE workers SET date = ? WHERE name = ? AND date = ?
                 ''', (new_date, name, old_date))
    conn.commit()
    conn.close()


def edit_worker_status(name, date, present_status):
    #* Creating connection
    conn = sqlite3.connect(db_path)
    conn.execute('''
                 UPDATE workers SET present_status = ? WHERE name = ? AND date = ?
                 ''', (present_status, name, date))
    conn.commit()
    conn.close()

def edit_money_earn(name, date, money_earn):
    conn = sqlite3.connect(db_path)
    conn.execute('''
                 UPDATE workers SET money_earn = ? WHERE name = ? AND date = ?
                 ''', (money_earn, name, date))
    conn.commit()
    conn.close()

def edit_money_lost(name, date, money_lost):
    conn = sqlite3.connect(db_path)
    conn.execute('''
                 UPDATE workers SET money_lost = ? WHERE name = ? AND date = ?
                 ''', (money_lost, name, date))
    conn.commit()
    conn.close()

def edit_note(name, date, note):
    conn = sqlite3.connect(db_path)
    conn.execute('''
                 UPDATE workers SET work_done = ? WHERE name = ? AND date = ?
                 ''', (note, name, date))
    conn.commit()
    conn.close()

def edit_image(name, image):
    conn = sqlite3.connect(db_path)
    conn.execute('''
                 UPDATE worker_image SET image = ? WHERE name = ?
                 ''', (image, name))
    conn.commit()
    conn.close()


'''
-----------------------------------------------------------------------------------
#* Note: Deletion
#? QA:
#! Warning:
#TODO:
-----------------------------------------------------------------------------------
'''
def delete_worker_data(name, date):
    conn = sqlite3.connect(db_path)
    conn.execute('DELETE FROM workers WHERE name = ? AND date = ?', (name, date))

    #* Check whether name still exists in the worker table
    cursor = conn.execute('SELECT COUNT(*) FROM workers WHERE name = ?', (name,))
    count = cursor.fetchone()[0]

    #* Delete picture if name no longer exists
    if count == 0:
        conn.execute('DELETE FROM worker_images WHERE name = ?', (name,))
    
    conn.commit()
    conn.close()


def instant_delete(name):
    conn = sqlite3.connect(db_path)
    cursor = conn.cursor()
    # Delete from workers table
    cursor.execute("DELETE FROM workers WHERE name = ?", (name,))
    # Delete from worker_images table (if exists)
    cursor.execute("SELECT name FROM worker_images WHERE name = ?", (name,))
    row = cursor.fetchone()
    if row is not None:
        cursor.execute("DELETE FROM worker_images WHERE name = ?", (name,))
    conn.commit()
    conn.close()

#! Emergency break
# create_worker_table()
# create_image_table()
# delete_worker_table()
# delete_image_table

```



End of Session
