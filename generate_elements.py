import random
import string
import pandas as pd
from tqdm import tqdm

from faker import Faker
from faker_e164.providers import E164Provider

# instantiate faker
fake = Faker()
fake.add_provider(E164Provider)


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
    df_school.head()
    df_school.to_csv('output\schools.csv')