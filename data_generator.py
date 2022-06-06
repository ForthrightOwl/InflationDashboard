import bls

"""Input paramaters"""
BLS_API_KEY=''
start_year = "1920"

"""Lists of series codes to be pulled for each dataset"""
not_seasonally_adjusted_series = ["CUUR0000SA0", "CUUR0000SA0L1E", "CUUR0000SAF1", "CUUR0000SA0E", "CUUR0000SACL1E", 	"CUUR0000SASLE", 	"CUUR0000SAF11", "CUUR0000SEFV", "CUUR0000SACE", "CUUR0000SEHF",
                              "CUUR0000SETA01", "CUUR0000SETA02", "CUUR0000SAA", "CUUR0000SAM1", "CUUR0000SAF116", "CUUR0000SEGA", "CUUR0000SAH1", "CUUR0000SAS4", "CUUR0000SAM2", "CUUR0000SAF111",
                              "CUUR0000SAF112", "CUUR0000SEFJ", "CUUR0000SAF113", "CUUR0000SAF114", "CUUR0000SAF115", "CUUR0000SEFV01", "CUUR0000SEHE01", "CUUR0000SETB01", "CUUR0000SEHF01", "CUUR0000SEFV02",
                              "CUUR0000SEHF02"
                                  ]
seasonally_adjusted_series = ["CUSR0000SA0", "CUSR0000SA0L1E", "CUSR0000SAF1", "CUSR0000SA0E", "CUSR0000SACL1E", 	"CUSR0000SASLE", 	"CUSR0000SAF11", "CUSR0000SEFV", "CUSR0000SACE", "CUSR0000SEHF",
                              "CUSR0000SETA01", "CUSR0000SETA02", "CUSR0000SAA", "CUSR0000SAM1", "CUSR0000SAF116", "CUSR0000SEGA", "CUSR0000SAH1", "CUSR0000SAS4", "CUSR0000SAM2", "CUSR0000SAF111",
                              "CUSR0000SAF112", "CUSR0000SEFJ", "CUSR0000SAF113", "CUSR0000SAF114", "CUSR0000SAF115", "CUSR0000SEFV01", "CUSR0000SEHE01", "CUSR0000SETB01", "CUSR0000SEHF01",
                              "CUSR0000SEHF02"
                              ]

"""Api calls for datasets"""
df_NSA = bls.get_series(not_seasonally_adjusted_series, startyear=start_year, key=BLS_API_KEY)
df_SA = bls.get_series(seasonally_adjusted_series, startyear=start_year, key=BLS_API_KEY)

"""Renaming the datasets from codes into text names"""
NSA_data = df_NSA.rename(columns={"CUUR0000SA0": "CPI",
                                  "CUUR0000SA0L1E": "Core CPI",
                                  "CUUR0000SAF1": "Food",
                                  "CUUR0000SA0E": "Energy",
                                  "CUUR0000SACL1E": "Commodities (less food and energy)",
                                  "CUUR0000SASLE": "Services (less energy)",
                                  "CUUR0000SAF11": "Food at home",
                                  "CUUR0000SEFV": "Food away from home",
                                  "CUUR0000SACE": "Energy commodities",
                                  "CUUR0000SEHF": "Energy services",
                                  "CUUR0000SETA01": "New vehicles",
                                  "CUUR0000SETA02": "Used cars and trucks",
                                  "CUUR0000SAA": "Apparel",
                                  "CUUR0000SAM1": "Medical care commodities",
                                  "CUUR0000SAF116": "Alcoholic Beverages",
                                  "CUUR0000SEGA": "Tobacco and smoking products",
                                  "CUUR0000SAH1": "Shelter",
                                  "CUUR0000SAS4": "Transportation services",
                                  "CUUR0000SAM2": "Medical care services",
                                  "CUUR0000SAF111": "Cereals and bakery products",
                                  "CUUR0000SAF112": "Meats, poultry, fish, and eggs",
                                  "CUUR0000SEFJ": "Dairy and related products",
                                  "CUUR0000SAF113": "Fruits and vegetables",
                                  "CUUR0000SAF114": "Nonalcoholic beverages",
                                  "CUUR0000SAF115": "Other food at home",
                                  "CUUR0000SEFV01": "Full service meals",
                                  "CUUR0000SEHE01": "Fuel oil",
                                  "CUUR0000SETB01": "Gasoline",
                                  "CUUR0000SEHF01": "Electricity",
                                  "CUUR0000SEFV02":"Limited Service Meals",
                                  "CUUR0000SEHF02": "Utility gas service",
                                  "CUUR0000SAF116":"Alcoholic beverages"})

SA_data = df_SA.rename(columns={"CUSR0000SA0": "CPI",
                                "CUSR0000SA0L1E": "Core CPI",
                                "CUSR0000SAF1": "Food",
                                "CUSR0000SA0E": "Energy",
                                "CUSR0000SACL1E": "Commodities (less food and energy)",
                                "CUSR0000SASLE": "Services (less energy)",
                                "CUSR0000SAF11": "Food at home",
                                "CUSR0000SEFV": "Food away from home",
                                "CUSR0000SACE": "Energy commodities",
                                "CUSR0000SEHF": "Energy services",
                                "CUSR0000SETA01": "New vehicles",
                                "CUSR0000SETA02": "Used cars and trucks",
                                "CUSR0000SAA": "Apparel",
                                "CUSR0000SAM1": "Medical Care Commodities",
                                "CUSR0000SAF116": "Alcoholic Beverages",
                                "CUSR0000SEGA": "Tobacco and smoking products",
                                "CUSR0000SAH1": "Shelter",
                                "CUSR0000SAS4": "Transportation services",
                                "CUSR0000SAM2": "Medical care services",
                                "CUSR0000SAF111": "Cereals and bakery products",
                                "CUSR0000SAF112": "Meats, poultry, fish, and eggs",
                                "CUSR0000SEFJ": "Dairy and related products",
                                "CUSR0000SAF113": "Fruits and vegetables",
                                "CUSR0000SAF114": "Nonalcoholic beverages",
                                "CUSR0000SAF115": "Other food at home",
                                "CUSR0000SEFV01": "Full service meals",
                                "CUSR0000SEHE01": "Fuel oil",
                                "CUSR0000SETB01": "Gasoline",
                                "CUSR0000SEHF01": "Electricity",
                                "CUSR0000SEHF02": "Utility gas service",
                                "CUSR0000SAF116":"Alcoholic beverages"})

"""Convert indexes into timestamp format for plotting"""
NSA_data.index = NSA_data.index.to_timestamp()
SA_data.index = SA_data.index.to_timestamp()

"""Separate data into annual and monthly"""
YoY_NSA_data = NSA_data.pct_change(periods=12)
YoY_SA_data = SA_data.pct_change(periods=12)
MoM_NSA_data = NSA_data.pct_change()
MoM_SA_data = SA_data.pct_change()

"""Write data to csv to be used by the main code"""
YoY_NSA_data.to_csv("venv/Data/YoY_NSA_data.csv")
YoY_SA_data.to_csv("venv/Data/YoY_SA_data.csv")
MoM_NSA_data.to_csv("venv/Data/MoM_NSA_data.csv")
MoM_SA_data.to_csv("venv/Data/MoM_SA_data.csv")
