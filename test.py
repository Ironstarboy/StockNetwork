import pandas as pd

import sqlCmd
from tqdm import tqdm

a=b=0

sqlCmd.insert('''
insert into q64
value 
(1,2,1.1)
''')