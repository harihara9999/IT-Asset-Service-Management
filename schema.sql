
CREATE TABLE IF NOT EXISTS employees (
    employee_id TEXT PRIMARY KEY,
    name TEXT NOT NULL,
    department TEXT NOT NULL,
    email TEXT UNIQUE NOT NULL,
    phone TEXT
);

CREATE TABLE IF NOT EXISTS assets (
    asset_id TEXT PRIMARY KEY,
    type TEXT NOT NULL,
    brand TEXT NOT NULL,
    model TEXT NOT NULL,
    serial_no TEXT UNIQUE NOT NULL,
    status TEXT DEFAULT 'AVAILABLE',
    purchase_date TEXT NOT NULL,
    CHECK (
        status IN (
            'AVAILABLE',
            'ASSIGNED',
            'UNDER_REPAIR',
            'RETIRED'
        )
    )
);

CREATE TABLE IF NOT EXISTS asset_assignments (
    assignment_id INTEGER PRIMARY KEY AUTOINCREMENT,
    asset_id TEXT NOT NULL,
    employee_id TEXT NOT NULL,
    assigned_date TEXT NOT NULL,
    return_date TEXT,
    FOREIGN KEY (asset_id)
        REFERENCES assets(asset_id),
    FOREIGN KEY (employee_id)
        REFERENCES employees(employee_id)
);

CREATE TABLE IF NOT EXISTS service_tickets (
    ticket_id TEXT PRIMARY KEY,
    asset_id TEXT NOT NULL,
    employee_id TEXT NOT NULL,
    technician_id TEXT,
    title TEXT NOT NULL,
    description TEXT NOT NULL,
    priority TEXT DEFAULT 'MEDIUM',
    status TEXT DEFAULT 'OPEN',
    diagnosis_notes TEXT,
    resolved_at TEXT,
    CHECK (
        priority IN (
            'LOW',
            'MEDIUM',
            'HIGH',
            'CRITICAL'
        )
    ),
    CHECK (
        status IN (
            'OPEN',
            'IN_PROGRESS',
            'RESOLVED',
            'CLOSED'
        )
    ),
    FOREIGN KEY (asset_id)
        REFERENCES assets(asset_id),
    FOREIGN KEY (employee_id)
        REFERENCES employees(employee_id),
    FOREIGN KEY (technician_id)
        REFERENCES employees(employee_id)
);
