import anvil.files
from anvil.files import data_files
import anvil.tables as tables
import anvil.tables.query as q
from anvil.tables import app_tables
import anvil.server

# This is a server module. It runs on the Anvil server,
# rather than in the user's browser.
#
# To allow anvil.server.call() to call functions here, we mark
# them with @anvil.server.callable.
# Here is an example - you can replace it with your own:
#
# @anvil.server.callable
# def say_hello(name):
#   print("Hello, " + name + "!")
#   return 42
#
import pandas as pd


def convert_to_df(file_obj)-> pd.DataFrame:        
        header_file = open(data_files[file_obj], "r")
        header_lines = []
        for i in range(4):
          aline = header_file.readline().strip().rstrip()
          header_lines.append(aline)

        add_cols = header_lines[3].split('\t')
        print("len cols = " + str(len(add_cols)))
        df = pd.read_csv(data_files[file_obj], sep='\t', skiprows=(0, 1, 2, 3, 4), index_col=False)
        header_cols=["s","x", "y"]        
        for col in add_cols:
            header_cols.append(str(col))
        header_cols.append("x1")
        header_cols.append("x2")  
        df.columns=header_cols
        return df

def to_np_from_df(df:pd.DataFrame, col_name:str):
    xs = df["x"]
    ys = df["y"]
    cs = df[col_name].to_numpy()

    x_dim = np.unique(xs).size
    y_dim = np.unique(ys).size
    new_cs = cs.copy()
    new_cs.resize(y_dim, x_dim)

@anvil.server.callable
def explore():
  msi_df = convert_to_df('mussel_xic.txt')
  print(str(msi_df.iloc[[3]]))
  #print(msi_df.head())
  