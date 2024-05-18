from ._anvil_designer import MSIMainFormTemplate
from anvil import *
import anvil.server
import anvil.tables as tables
import anvil.tables.query as q
from anvil.tables import app_tables
import plotly.graph_objects as go




class MSIMainForm(MSIMainFormTemplate):
  def __init__(self, **properties):
    # Set Form properties and Data Bindings.
    self.init_components(**properties)

    # Any code you write here will run before the form opens.

  def button_details_click(self, **event_args):
    """This method is called when the button is clicked"""
    masses = anvil.server.call('extract_df_masses')    
    self.drop_down_xic.items = masses
    
    

  def drop_down_xic_change(self, **event_args):
    """This method is called when an item is selected"""
    
    mass_id = self.drop_down_xic.selected_value
    print(str(mass_id))
    #extract_df_xic_fig
    fig = anvil.server.call('create_fig')#, mass_id)    
    self.plot_xic.data = fig
      
