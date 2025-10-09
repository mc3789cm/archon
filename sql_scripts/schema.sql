CREATE TABLE IF NOT EXISTS "Statistics" (
    "Server Name" TEXT,
    "Server ID" INTEGER NOT NULL UNIQUE,
    "Join Date" TEXT,
    PRIMARY KEY("Server ID")
);

CREATE TABLE IF NOT EXISTS "General Configuration" (
    "Server ID" INTEGER NOT NULL UNIQUE,
    "Admin Role ID" INTEGER,
    PRIMARY KEY("Server ID")
);
