import pandas as pd
from ip_cleaner import ip_cleaner
from ssh_data_collector import ssh_data_collector
from datetime import datetime




start_time = datetime.now()

vits_df = pd.read_excel("test.xlsx")

#print(df)

ips = vits_df["IP address"].tolist()
#ips = ["192.168.6.210", "192.168.6.216/32", "192.168.6.213/32", "192.168.6.217/32"]

ips = ip_cleaner(ips)

device_info = ssh_data_collector(ips, "admin", "admin")


end_time = datetime.now()
print("\n***********************************")    
print("Total Time: ", end_time - start_time)
print("***********************************\n")    

device_info_df = pd.DataFrame(device_info)
device_info_df = device_info_df.rename(columns={"ip_address": "IP address"})
#print(device_info_df)

merged_df = pd.merge(vits_df, device_info_df, on='IP address', how='left')



# Create a mask for rows without a serial number
mask = merged_df['serial_number'].isna()

# Group by 'serial_number' and 'Vulnerability' and aggregate columns
grouped_df = merged_df[~mask].groupby(['serial_number', 'Vulnerability']).agg(
    lambda x: x.iloc[0] if len(x.unique()) == 1 else x.tolist()
).reset_index()

# Calculate the number of duplicates for each group
grouped_df['duplicate_counter'] = merged_df[~mask].groupby(['serial_number', 'Vulnerability']).size().values

# Filter out rows without a serial number and concatenate them with grouped DataFrame
jumbled_df = pd.concat([merged_df[mask], grouped_df])



# Define the columns you want to keep at the beginning
first_columns = ['Vulnerability', 'duplicate_counter', 'Number', 'IP address', 'serial_number', 'os_version', 'model', 'hostname', 'fqdn']

# Move the remaining columns to the end
remaining_columns = [col for col in jumbled_df.columns if col not in first_columns]

# Reorder the columns
new_column_order = first_columns + remaining_columns
result_df = jumbled_df[new_column_order].sort_values(by='Vulnerability')

result_df.to_excel("output.xlsx", index=False)
