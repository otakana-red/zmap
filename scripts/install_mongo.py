import sys
import os
import os.path

import sh
from sh import git, cd, make, rm, sudo

def write_output(line):
	sys.stdout.write(line)

directory = os.path.dirname(os.path.realpath(__file__))

mongo_c_driver = os.path.join(directory, "mongo-c-driver")

rm("-r", "-f", mongo_c_driver)
autogen_location = os.path.join(mongo_c_driver, "autogen.sh")

git.clone("https://github.com/mongodb/mongo-c-driver.git",
	mongo_c_driver,
	branch="1.1.5",
	depth="1",
	_out=write_output,
)

cd(mongo_c_driver)
autogen = sh.Command(autogen_location)
autogen(prefix="/usr", libdir="/usr/lib64", _out=write_output)
make(_out=write_output)

if os.environ.get("ZMAP_TRAVIS_BUILD", None):
	print("Installing...")
	with sudo:
		make.install(_out=write_output)

print("Done.")
