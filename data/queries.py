# 1.1 Creating invoices table
CREATE_INVOICES_TABLE = """
CREATE TABLE IF NOT EXISTS invoices (
    invoice_id TEXT PRIMARY KEY,
    customer_id TEXT,
    billing_start_date TEXT,
    billing_end_date TEXT,
    data_mobile_internet_mb INTEGER,
    data_roaming_mb INTEGER,
    data_bonus_mb INTEGER,
    minutes_on_net INTEGER,
    minutes_off_net INTEGER,
    minutes_international INTEGER,
    minutes_roaming INTEGER,
    sms_on_net INTEGER,
    sms_off_net INTEGER,
    sms_international INTEGER,
    charges_subscription_fee REAL,
    charges_additional_services REAL,
    charges_usage_charges REAL,
    charges_vat REAL,
    charges_total_amount REAL,
    payment_status TEXT
)
"""

# 1.2 Insert records into invoices table
INSERT_INVOICES_DATA = """
INSERT OR REPLACE INTO invoices VALUES (?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?)
"""

# 2.1 Create activated_services table
CREATE_ACTIVATED_SERVICES_TABLE = """
CREATE TABLE IF NOT EXISTS activated_services (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    invoice_id TEXT,
    service_name TEXT,
    is_active BOOLEAN,
    FOREIGN KEY (invoice_id) REFERENCES invoices (invoice_id)
)
"""

# 2.2 Insert records in activated_services table
INSERT_ACTIVATED_SERVICES_DATA = """
INSERT INTO activated_services (invoice_id, service_name, is_active) VALUES (?,?,?)
"""

# З.1 Create roaming_packages
CREATE_ROAMING_PACKAGES_TABLE = """
CREATE TABLE IF NOT EXISTS roaming_packages (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    invoice_id TEXT,
    package_name TEXT,
    is_active BOOLEAN,
    FOREIGN KEY (invoice_id) REFERENCES invoices (invoice_id)
)
"""

# 3.2 Insert records in roaming_packages table
INSERT_ROAMING_PACKAGES_DATA = """
INSERT INTO roaming_packages (invoice_id, package_name, is_active) VALUES (?,?,?)
"""