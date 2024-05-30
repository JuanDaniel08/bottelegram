import pandas as pd
from datetime import datetime
var= None


excel_file_path = "./Models/Database/Inventario.xlsx"
inventario_df = pd.read_excel(excel_file_path, sheet_name="Hoja1")


def demandas(message):
    if (message.text).lower()=="medias":
            var=0
    elif (message.text).lower()=="zapatos":
        var=1
    elif (message.text).lower()=="boxer":
        var=2
    elif (message.text).lower()=="camiseta":
        var=3
    elif (message.text).lower()=="chompas":
        var=4


    inventario_df.loc[var, 'Demanda']=inventario_df.loc[var, 'Demanda']+1        
    inventario_df.to_excel("./Models/Database/Inventario.xlsx",index=False,sheet_name = "Hoja1")


