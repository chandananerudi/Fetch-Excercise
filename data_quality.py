import json
import csv
from datetime import datetime
import pandas as pd


# Load JSON data from file
data = []

def convert_timestamp_to_date(timestamp):
    return datetime.fromtimestamp(timestamp / 1000).strftime('%Y-%m-%d %H:%M:%S')


with open('receipts.json', 'r') as file:
    for line in file:
        receipts_record = json.loads(line)
        receipts_record['_id'] = receipts_record['_id']['$oid']
        receipts_record['createDate'] = convert_timestamp_to_date(receipts_record['createDate']['$date'])
        receipts_record['dateScanned'] = convert_timestamp_to_date(receipts_record['dateScanned']['$date'])
        if 'finishedDate' in record:
            receipts_record['finishedDate'] = convert_timestamp_to_date(receipts_record['finishedDate']['$date'])
        receipts_record['modifyDate'] = convert_timestamp_to_date(receipts_record['modifyDate']['$date'])
        if 'pointsAwardedDate' in record:
            receipts_record['pointsAwardedDate'] = convert_timestamp_to_date(receipts_record['pointsAwardedDate']['$date'])
        if 'purchaseDate' in record:
            receipts_record['purchaseDate'] = convert_timestamp_to_date(receipts_record['purchaseDate']['$date'])
        
        # Check if rewardsReceiptItemList exists and has items
        if 'rewardsReceiptItemList' in receipts_record and receipts_record['rewardsReceiptItemList']:
            item = receipts_record['rewardsReceiptItemList'][0]  # Assuming only the first item is considered
            receipts_record['barcode'] = item.get('barcode')
            receipts_record['description'] = item.get('description')
            receipts_record['finalPrice'] = item.get('finalPrice')
            receipts_record['itemPrice'] = item.get('itemPrice')
            receipts_record['needsFetchReview'] = item.get('needsFetchReview')
            receipts_record['partnerItemId'] = item.get('partnerItemId')
            receipts_record['preventTargetGapPoints'] = item.get('preventTargetGapPoints')
            receipts_record['quantityPurchased'] = item.get('quantityPurchased')
            receipts_record['userFlaggedBarcode'] = item.get('userFlaggedBarcode')
            receipts_record['userFlaggedNewItem'] = item.get('userFlaggedNewItem')
            receipts_record['userFlaggedPrice'] = item.get('userFlaggedPrice')
            receipts_record['userFlaggedQuantity'] = item.get('userFlaggedQuantity')
        
        data.append(receipts_record)  # Append each record to the data list

# Specify the CSV file name
csv_file = 'receipts.csv'

# Specify the CSV column names, including 'cpg_id' and 'cpg_ref'
csv_columns = ['_id', 'bonusPointsEarned', 'bonusPointsEarnedReason', 'createDate', 'dateScanned', 
               'finishedDate', 'modifyDate', 'pointsAwardedDate', 'pointsEarned', 'purchaseDate',
               'purchasedItemCount', 'barcode', 'description', 'finalPrice', 'itemPrice', 'needsFetchReview',
               'partnerItemId', 'preventTargetGapPoints', 'quantityPurchased', 'userFlaggedBarcode', 
               'userFlaggedNewItem', 'userFlaggedPrice', 'userFlaggedQuantity', 'rewardsReceiptStatus', 'totalSpent', 
               'userId']
# Write the processed data to CSV file
try:
    with open(csv_file, 'w', newline='') as csvfile:
        writer = csv.DictWriter(csvfile, fieldnames=csv_columns)
        writer.writeheader()
        
        for record in data:
            csv_data = {
                '_id': receipts_record['_id'],
                'bonusPointsEarned': receipts_record.get('bonusPointsEarned'),
                'bonusPointsEarnedReason': receipts_record.get('bonusPointsEarnedReason'),
                'createDate': receipts_record.get('createDate'),  # Use .get() to handle missing key
                'dateScanned': receipts_record.get('dateScanned'),
                'finishedDate': receipts_record.get('finishedDate'),
                'modifyDate': receipts_record.get('modifyDate'),
                'pointsAwardedDate': receipts_record.get('pointsAwardedDate'),
                'pointsEarned': receipts_record.get('pointsEarned'),
                'purchaseDate': receipts_record.get('purchaseDate'),
                'purchasedItemCount': receipts_record.get('purchasedItemCount'),  # Use .get() to handle missing key
                'barcode': receipts_record.get('barcode'),
                'description': receipts_record.get('description'),
                'finalPrice': receipts_record.get('finalPrice'),
                'itemPrice': receipts_record.get('itemPrice'),
                'needsFetchReview': receipts_record.get('needsFetchReview'),
                'partnerItemId': receipts_record.get('partnerItemId'),
                'preventTargetGapPoints': receipts_record.get('preventTargetGapPoints'),
                'quantityPurchased': receipts_record.get('quantityPurchased'),  # Use .get() to handle missing key
                'userFlaggedBarcode': receipts_record.get('userFlaggedBarcode'),
                'userFlaggedNewItem': receipts_record.get('userFlaggedNewItem'),
                'userFlaggedPrice': receipts_record.get('userFlaggedPrice'),
                'userFlaggedQuantity': receipts_record.get('userFlaggedQuantity'),
                'rewardsReceiptStatus': receipts_record.get('rewardsReceiptStatus'),
                'totalSpent': receipts_record.get('totalSpent'),
                'userId': receipts_record.get('userId'),
            }
            writer.writerow(csv_data)
    
    print(f'Data written to {csv_file}')
except IOError as e:
    print(f'I/O error occurred while writing to {csv_file}: {e}')

#convert three files similar to above


receipts = pd.read_csv('receipts.csv')
users = pd.read_csv('users.csv')

missing_values_receipts = receipts.isnull().sum()
print("Missing values in Receipts data:\n", missing_values_receipts)

missing_values_users = users.isnull().sum()
print("Missing values in Users data:\n", missing_values_users)

duplicate_users = users[users.duplicated('_id', keep=False)]
print("Duplicate user IDs:\n", duplicate_users)

duplicate_receipts = receipts[receipts.duplicated('_id', keep=False)]
print("Duplicate receipt IDs:\n", duplicate_receipts)

def is_valid_date(date):
    try:
        pd.to_datetime(date, format='%Y-%m-%d')
        return True
    except ValueError:
        return False

invalid_dates = receipts[~receipts['purchaseDate'].apply(is_valid_date)]
print("Invalid dates in Receipts data:\n", invalid_dates)

valid_states = set(['AL', 'AK', 'AZ', 'AR', 'CA', 'CO', 'CT', 'DE', 'FL', 'GA', 'HI', 'ID', 'IL', 'IN', 'IA', 'KS', 'KY', 'LA', 'ME', 'MD', 'MA', 'MI', 'MN', 'MS', 'MO', 'MT', 'NE', 'NV', 'NH', 'NJ', 'NM', 'NY', 'NC', 'ND', 'OH', 'OK', 'OR', 'PA', 'RI', 'SC', 'SD', 'TN', 'TX', 'UT', 'VT', 'VA', 'WA', 'WV', 'WI', 'WY'])
invalid_states = users[~users['state'].isin(valid_states)]
print("Invalid states in Users data:\n", invalid_states)
