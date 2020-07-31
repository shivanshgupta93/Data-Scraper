import pandas as pd
from jobs.cron import get_product_data, get_categories_data, get_features_data

def extract_excel():

    
    excel_writer = pd.ExcelWriter('./extractfile/' + 'Scrapped_Data.xlsx', engine='xlsxwriter') ## Creating a excel file where data would be dumped

    table_columns, data = get_product_data()

    data_df = pd.DataFrame(data, columns = table_columns)

    data_df.to_excel(excel_writer, sheet_name = 'Product', encoding='utf-8', index=None) ## Dumping products table data

    table_columns, data = get_categories_data()

    data_df = pd.DataFrame(data, columns = table_columns)

    data_df.to_excel(excel_writer, sheet_name = 'Category', encoding='utf-8', index=None) ## Dumping category table data

    table_columns, data = get_features_data()

    data_df = pd.DataFrame(data, columns = table_columns)

    data_df.to_excel(excel_writer, sheet_name = 'Feature', encoding='utf-8', index=None) ## Dumping feature table data

    excel_writer.save()