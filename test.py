import pdb
from Result import Result
import urllib3

urllib3.disable_warnings(urllib3.exceptions.InsecureRequestWarning)

test = Result(config_dir=r'./search.json')
test.Data.to_csv(r'./test.csv')
pdb.set_trace()