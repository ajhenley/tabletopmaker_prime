from generate_elements import generate_schools
from faker import Faker

import argparse

#=====================================================================
# Handle Arguments for the script
#=====================================================================

parser = argparse.ArgumentParser(description='')
parser.add_argument('--config_path', type=str, default="config/default/",
                    help="stuff")
parser.add_argument("--schools", type=int, default=1,
                    help="number of schools")
parser.add_argument("--students", type=int, default=10,
                    help="number of students")
parser.add_argument("--teachers", type=int, default=1,
                    help="number of teachers")
parser.add_argument("--staff", type=int, default=2,
                    help="number of staff")

#=====================================================================
# Set up all the configs
#=====================================================================
args = parser.parse_args()
print("schools", args.schools)
print("students", args.students)
print("teachers", args.teachers)
print("staff", args.staff)

city = "Helenville"

generate_schools(args.schools, "High School", city)
