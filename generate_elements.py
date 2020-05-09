import random
import string
import pandas as pd
import random
import datetime
from dateutil.relativedelta import relativedelta
from tqdm import tqdm

from faker import Faker
from faker_e164.providers import E164Provider

# instantiate faker
fake = Faker()
fake.add_provider(E164Provider)

DATE_END = datetime.datetime.now() + relativedelta(years=-25)
DATE_START = DATE_END + relativedelta(years=-34)

STU_DATE_END = datetime.datetime.now() + relativedelta(years=-6)
STU_DATE_START = STU_DATE_END + relativedelta(years=-12)

PC_DATE_END = datetime.datetime.now() + relativedelta(months=-2)
PC_DATE_START = PC_DATE_END + relativedelta(years=-3)
last_valid_date = datetime.datetime.now() + relativedelta(years=-30)
last_valid_student_date = datetime.datetime.now() + relativedelta(years=-6)
last_valid_purchase_date = datetime.datetime.now() + relativedelta(months=-3)

hs_cut_off = datetime.datetime.today() + relativedelta(years=-14)
ms_cut_off = datetime.datetime.today() + relativedelta(years=-11)

def create_school(schooltype):
    name = fake.name() + " " + schooltype
    address = fake.building_number() + " " + fake.street_name() + " " + fake.street_suffix()
    phone = fake.safe_e164(region_code="US")
    fax = fake.safe_e164(region_code="US")
    while phone == fax:
        fax = fake.safe_e164(region_code="US")
    return name, address, phone, fax


def generate_schools(num, school_type, city, state='MD'):
    df_school = pd.DataFrame(columns={"schoolid", "name", "address", "city", "state", "phone", "fax", "principal"})

    for i in tqdm(range(0, num)):
        name, address, phone, fax = create_school(school_type)
        values_to_add = {"schoolid": i + 1, "name": name, "address": address, "city": city, "state": state,
                         "phone": phone, "fax": fax, "principal": ""}
        row_to_add = pd.Series(values_to_add, name=str(i + 1))
        df_school = df_school.append(row_to_add)

    # save the dataset
    df_school = df_school[["schoolid", "name", "address", "city", "state", "phone", "fax", "principal"]]
    df_school.to_csv('output_schools.csv')


def create_device(dev_type="desktop"):
    global last_valid_purchase_date
    asset_tag = fake.hexify(text='^^^^^^')
    if dev_type == "ipad":
        # ipad stuff
        make = "Apple"
        model = random.choice(["iPad Mini", "iPad"])
    elif dev_type == "desktop":
        # desktop pc stuff
        make = "Dell"
        model = random.choice(["Inspiron","Optiplex"])
    else:
        # laptop
        make = "Dell"
        model = random.choice(["Latitude 3500","Latitude 3310","Latitude 3400"])

    try:
        purchase_date = fake.date_between_dates(PC_DATE_START, PC_DATE_END)
    except:
        purchase_date = last_valid_purchase_date

    last_valid_purchase_date = purchase_date
    serial_number = fake.uuid4()
    mac_addr = fake.hexify(text='^^:^^:^^:^^:^^:^^')
    status = "unassigned"
    usage = "noone"
    return asset_tag, make, model, purchase_date, serial_number, mac_addr, status, usage


def generate_devices(num=20, dev_type="desktop"):
    df_devices = pd.DataFrame(
        columns={"asset_tag", "make", "model", "dev_type", "purchase_date", "serial_number", "mac_addr", "status",
                 "usage"})
    for i in tqdm(range(0, num)):
        asset_tag, make, model, purchase_date, serial_number, mac_addr, status, usage = create_device(dev_type)
        values_to_add = {"asset_tag": asset_tag, "make": make, "model": model, "dev_type": "tablet",
                         "purchase_date": purchase_date, "serial_number": serial_number, "mac_addr": mac_addr,
                         "status": status, "usage": usage}
        row_to_add = pd.Series(values_to_add, name=str(i))
        df_devices = df_devices.append(row_to_add)

    # save the dataset
    df_devices = df_devices[["asset_tag", "make", "model", "dev_type", "purchase_date", "serial_number", "mac_addr",
                             "status", "usage"]]
    df_devices.to_csv('output_devices.csv', mode='a')

def create_student():
    global last_valid_student_date

    fname = fake.first_name()
    lname = fake.last_name()
    address = fake.building_number() + " " + fake.street_name() + " " + fake.street_suffix()
    hphone = fake.safe_e164(region_code="US")
    try:
        dob = fake.date_between_dates
        dob = fake.date_between_dates(STU_DATE_START, STU_DATE_END)
    except:
        dob = last_valid_student_date

    last_valid_date = dob
    ssn = fake.ssn()

    if dob > hs_cut_off.date():
        school = random.randrange(0, 16)
    elif dob > ms_cut_off.date():
        school = random.randrange(16, 48)
    else:
        school = random.randrange(48, 116)

    grade = relativedelta(datetime.date.today(), dob).years - 5

    assignedschool = school
    return fname, lname, address, hphone, dob, ssn, grade, assignedschool


def create_students(num=20, seed=0):
    for i in tqdm(range(seed+0, seed+num)):
        fname, lname, address, hphone, dob, ssn, grade, assignedschool = create_student()
        device = find_avail_device('tablet', df_devices)
        a_tag = df_devices.iloc[device]['asset_tag']
        values_to_add = {
            "stuid": i,
            "fname": fname,
            "lname": lname,
            "address": address,
            "city": city,
            "state": state,
            "hphone": hphone,
            "dob": dob,
            "ssn": ssn,
            "grade": grade,
            "degreeschool": edschool,
            "schoolassignment": assignedschool,
            "deviceassignment": a_tag
        }
        df_devices.status[df_devices['asset_tag'] == a_tag] = 'assigned'
        df_devices.usage[df_devices['asset_tag'] == a_tag] = i
        row_to_add = pd.Series(values_to_add, name=i)
        df_student = df_student.append(row_to_add)

    df_devices = df_devices[
        ["asset_tag", "make", "model", "dev_type", "purchase_date", "serial_number", "mac_addr", "status", "usage"]]
    df_student = df_student[
        ["stuid", "fname", "lname", "address", "city", "state", "hphone", "dob", "ssn", "grade", "schoolassignment",
         "deviceassignment"]]
