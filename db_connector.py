import psycopg2
import configparser

config = configparser.ConfigParser()
config.read("config.ini")  # читаем конфиг
print(config["database"]["db"])
con = psycopg2.connect(
    database=config["database"]["db"],
    user=config["database"]["user"],
    password=config["database"]["passwd"],
    host=config["database"]["host"],
    port=int(config["database"]["port"])
)

def create_table_counters(name):
  cur = con.cursor()
  cur.execute(f'''CREATE TABLE {name}  
       (id serial primary key,
       SERIAl INT NOT NULL,
       ADDRESS INT NOT NULL,
       MODEL CHAR(50),
       MANUFACTURED CHAR(50),
       DESCRIPTION CHAR(50));''')
  commit()


def create_table_data(name='data'):
  cur = con.cursor()
  cur.execute(f'''CREATE TABLE {name}  
       (Currentdatetime timestamp not null default CURRENT_TIMESTAMP PRIMARY KEY,
       ADDRESS INT NOT NULL,
       DESCRIPTION CHAR(50),
       VOLTAGE_A REAL,
       VOLTAGE_B REAL,
       VOLTAGE_C REAL,
       CURRENT_A REAL,
       CURRENT_B REAL,
       CURRENT_C REAL,
       ACTIVE_POWER_FULL REAL,
       ACTIVE_POWER_A REAL,
       ACTIVE_POWER_B REAL,
       ACTIVE_POWER_C REAL,
       REACTIVE_POWER_A REAL,
       REACTIVE_POWER_B REAL,
       REACTIVE_POWER_C REAL,
       FULL_POWER REAL,
       FULL_POWER_A REAL,
       FULL_POWER_B REAL,
       FULL_POWER_C REAL,
       ACTIVE_ENERGY REAL,
       ACTIVE_ENERGY_T1 REAL,
       ACTIVE_ENERGY_T2 REAL,
       ACTIVE_ENERGY_T3 REAL,
       ACTIVE_ENERGY_T4 REAL,
       ACTIVE_ENERGY_A REAL,
       ACTIVE_ENERGY_B REAL,
       ACTIVE_ENERGY_C REAL);''')
  commit()


def insert_data_counter(name="counter"):
  cur = con.cursor()
  cur.execute(
    f"INSERT INTO {name} (SERIAL,ADDRESS,DESCRIPTION) VALUES (41851891, 91, 'test')"
  )
  commit()

def insert_data_data(name="data",):
  cur = con.cursor()
  cur.execute(
    f"INSERT INTO {name} (ADDRESS,DESCRIPTION,VOLTAGE_A,VOLTAGE_B,VOLTAGE_C,CURRENT_A,CURRENT_B,CURRENT_C,ACTIVE_POWER_FULL,"
    f"ACTIVE_POWER_A,ACTIVE_POWER_B,ACTIVE_POWER_C,REACTIVE_POWER_A,REACTIVE_POWER_B,REACTIVE_POWER_C,FULL_POWER,FULL_POWER_A,"
    f"FULL_POWER_B,FULL_POWER_C,ACTIVE_ENERGY,ACTIVE_ENERGY_T1,ACTIVE_ENERGY_T2,ACTIVE_ENERGY_T3,ACTIVE_ENERGY_T4,ACTIVE_ENERGY_A,"
    f"ACTIVE_ENERGY_B,ACTIVE_ENERGY_C) VALUES (91, 'test', 0.00, 0.00, 0.00, 0.00, 0.00, 0.00, 0.00, 0.00, 0.00, 0.00, 0.00, 0.00, 0.00, 0.00, 0.00, 0.00, 0.00, 0.00, 0.00, 0.00, 0.00, 0.00, 0.00, 0.00, 0.00)"
  )
  commit()
  print('ok')

def read_data(name):
  cur = con.cursor()
  cur.execute(f"SELECT * from {name}")
  rows = cur.fetchall()
  print(rows)
  close()


def update_data(name):
  cur = con.cursor()
  cur.execute(f"UPDATE {name} set MODEL = 'MERCURY-234 ARTM-03 PBR.G', MANUFACTURED = '03.02.2020' where id = 1;")
  commit()
  print("ok")


def close():
  con.close()


def commit():
  con.commit()
  con.close()

# create_table_counters('test')
read_data('data')
# update_data('test')
# create_table_data()
# insert_data_data()
