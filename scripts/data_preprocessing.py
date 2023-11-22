import json

# Load the original large JSON file
input_file_path = 'data/raw/NY_2023-2024_bills.json'
with open(input_file_path, 'r') as file:
    bills_data = json.load(file)

# Process the data to include only Assembly bills and relevant fields
filtered_bills = []
sponsors_data = []

for bill in bills_data:
    if bill['chamber'] == 'lower':
        # Extracting bill information
        bill_info = {
            'bill_id': bill['id'],
            'bill_name': bill['identifier'],
            'title': bill['title'],
            'abstract': bill['abstracts'][0]['abstract'] if bill['abstracts'] else None  # Using None for no abstract
        }
        filtered_bills.append(bill_info)

        # Extracting sponsor information
        if 'sponsors' in bill:
            for sponsor in bill['sponsors']:
                sponsors_data.append({
                    'bill_id': bill['id'],
                    'sponsor_name': sponsor['name']
                })

# Write the filtered bill data to a new smaller JSON file in the 'filtered' directory
output_bill_file_path = 'data/filtered/NY_Assembly_bills.json'
with open(output_bill_file_path, 'w') as file:
    json.dump(filtered_bills, file, indent=4)

# Write the sponsor data to a separate JSON file in the 'filtered' directory
output_sponsor_file_path = 'data/filtered/NY_Assembly_bill_sponsors.json'
with open(output_sponsor_file_path, 'w') as file:
    json.dump(sponsors_data, file, indent=4)

