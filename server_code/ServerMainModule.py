import anvil.files
from anvil.files import data_files
import anvil.tables as tables
import anvil.tables.query as q
from anvil.tables import app_tables
import anvil.server
import plotly.express as px


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
import numpy as np
import plotly.express as px

class DFWrapper:

  def __init__(self, file_obj):
      self.df = self.convert_to_df(file_obj)
    

  def convert_to_df(self, file_obj)-> pd.DataFrame:        
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

  def to_np_from_df(self, col_name:str):
      df = self.df
      xs = df["x"]
      ys = df["y"]
      cs = df[col_name].to_numpy()
  
      x_dim = np.unique(xs).size
      y_dim = np.unique(ys).size
      new_cs = cs.copy()
      new_cs.resize(y_dim, x_dim)
      return new_cs
      
@anvil.server.callable
def extract_df_masses():
  file_obj = "mussel_xic.txt"
  header_file = open(data_files[file_obj], "r")
  header_lines = []
  for i in range(4):
    aline = header_file.readline().strip().rstrip()
    header_lines.append(aline)

  add_cols = header_lines[3].split('\t')
  print("len cols = " + str(len(add_cols)))
  return add_cols



@anvil.server.callable
def extract_df_xic_fig(mass_to_extract):
  file_obj = "mussel_xic.txt"
  df_wrap = DFWrapper(file_obj)  
  np_img = df_wrap.to_np_from_df(mass_to_extract)
  print("np_img shape = " + str(np_img.shape))
  fig = px.imshow(np_img)
  return fig

@anvil.server.callable
def create_fig():
    data = px.data.iris()
    fig = px.scatter(data, x="sepal_width", y="sepal_length", color="species", trendline="ols")
    return fig
  



  