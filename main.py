import requests
import json
import sqlite3
import os
from dotenv import load_dotenv

from data.queries import (
    CREATE_INVOICES_TABLE,
    INSERT_INVOICES_DATA,
    CREATE_ACTIVATED_SERVICES_TABLE,
    INSERT_ACTIVATED_SERVICES_DATA,
    CREATE_ROAMING_PACKAGES_TABLE,
    INSERT_ROAMING_PACKAGES_DATA
)

load_dotenv()

# 1. Extract

def extract_data(url: str, file_path: str):
    """Reads JSON file and writes data in data/landing_zone"""
    print(" Extracting raw Data...")
    try:
        response = requests.get(url)
        response.raise_for_status()
        data = response.json()

        os.makedirs(os.path.dirname(file_path), exist_ok=True)
        with open(file_path, 'w', encoding='utf-8') as f:
            json.dump(data, f, indent=4)
        print(f"✅ Staging Data is loaded at: {file_path}")
        return data['invoices']
    except requests.exceptions.RequestException as e:
        print(f"❌ Error while fetching data from raw source. Details: {e}")
        return None


# 2. Transform Data
def transform_data(invoices_data: list):
    """Transforms raw JSON data into data types to match SQL Schemas"""
    print("Transforming Data...")
    invoices_table = []
    services_table = []
    roaming_packages_table = []

    # Normalizing Invoices data
    for invoice in invoices_data:
        invoices_table.append({
            'invoice_id': invoice['invoice_id'],
            'customer_id': invoice['customer_id'],
            'billing_start_date': invoice['billing_period']['start_date'],
            'billing_end_date': invoice['billing_period']['end_date'],
            'data_mobile_internet_mb': invoice['usage']['data']['mobile_internet_mb'],
            'data_roaming_mb': invoice['usage']['data']['roaming_mb'],
            'data_bonus_mb': invoice['usage']['data']['bonus_mb'],
            'minutes_on_net': invoice['usage']['minutes']['on_net'],
            'minutes_off_net': invoice['usage']['minutes']['off_net'],
            'minutes_international': invoice['usage']['minutes']['international'],
            'minutes_roaming': invoice['usage']['minutes']['roaming'],
            'sms_on_net': invoice['usage']['sms']['on_net'],
            'sms_off_net': invoice['usage']['sms']['off_net'],
            'sms_international': invoice['usage']['sms']['international'],
            'charges_subscription_fee': invoice['charges']['subscription_fee'],
            'charges_additional_services': invoice['charges']['additional_services'],
            'charges_usage_charges': invoice['charges']['usage_charges'],
            'charges_vat': invoice['charges']['vat'],
            'charges_total_amount': invoice['charges']['total_amount'],
            'payment_status': invoice['payment_status']
        })

        # Extracting and loading data for active services
        for service in invoice['activated_services']:
            services_table.append({
                'invoice_id': invoice['invoice_id'],
                'service_name': service['service_name'],
                'is_active': service['active']
            })

        # Extracting and loading data fro roaming packages
        for package in invoice['roaming_packages']:
            roaming_packages_table.append({
                'invoice_id': invoice['invoice_id'],
                'package_name': package['package_name'],
                'is_active': package['active']
            })

    print("✅ Data is transformed successfully.")
    return invoices_table, services_table, roaming_packages_table


# 3. Loading Data
def load_data(invoices_data: list, services_data: list, roaming_packages_data: list, db_path: str):
    """Loads transformed data in SQLite DB"""
    print("Loading data in Database...")
    conn = sqlite3.connect(db_path)
    cursor = conn.cursor()

    # Create SQL tables (only on first run)
    cursor.execute(CREATE_INVOICES_TABLE)
    cursor.execute(CREATE_ACTIVATED_SERVICES_TABLE)
    cursor.execute(CREATE_ROAMING_PACKAGES_TABLE)

    # Insert Data
    cursor.executemany(
        INSERT_INVOICES_DATA,
        [tuple(d.values()) for d in invoices_data])

    cursor.executemany(
        INSERT_ACTIVATED_SERVICES_DATA,
        [(d['invoice_id'], d['service_name'], d['is_active']) for d in services_data])

    cursor.executemany(
        INSERT_ROAMING_PACKAGES_DATA,
        [(d['invoice_id'], d['package_name'], d['is_active']) for d in roaming_packages_data])

    conn.commit()
    conn.close()
    print("✅ Data is successfully uploaded in SQLite DB.")


def main():
    """Runs Main ETL logic."""
    json_url = os.getenv("RAW_SOURCE_URL")
    data_dir = os.getenv("WORKING_DIR")
    local_file_path = os.path.join(data_dir, "landing_zone/raw_telecom_data.json")
    sqlite_db_path = os.path.join(data_dir, "telecom_data.db")

    invoices = extract_data(json_url, local_file_path)
    if not invoices:
        return

    invoices_transformed, services_transformed, roaming_packages_transformed = transform_data(invoices)

    load_data(invoices_transformed, services_transformed, roaming_packages_transformed, sqlite_db_path)


if __name__ == "__main__":
    main()