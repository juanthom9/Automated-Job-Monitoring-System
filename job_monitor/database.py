from datetime import datetime
from typing import Any

import psycopg
from psycopg.rows import dict_row

from config import DATABASE_URL


class Database:
    def __init__(self) -> None:
        self.database_url = DATABASE_URL

    def connect(self) -> psycopg.Connection:
        # Return a PostgreSQL connection
        return psycopg.connect(
            self.database_url,
            row_factory=dict_row,
        )

    def create_tables(self) -> None:
        # Create all tables needed by the monitor
        with self.connect() as connection:
            with connection.cursor() as cursor:
                cursor.execute(
                    """
                    CREATE TABLE IF NOT EXISTS companies (
                        id SERIAL PRIMARY KEY,
                        name TEXT NOT NULL UNIQUE,
                        careers_url TEXT NOT NULL,
                        connector TEXT NOT NULL DEFAULT 'auto',
                        platform_hint TEXT,
                        enabled BOOLEAN NOT NULL DEFAULT TRUE,
                        last_checked_at TIMESTAMPTZ,
                        created_at TIMESTAMPTZ NOT NULL DEFAULT NOW(),
                        updated_at TIMESTAMPTZ NOT NULL DEFAULT NOW()
                    );
                    """
                )

                cursor.execute(
                    """
                    CREATE TABLE IF NOT EXISTS jobs (
                        id SERIAL PRIMARY KEY,
                        company_id INTEGER NOT NULL
                            REFERENCES companies(id)
                            ON DELETE CASCADE,
                        external_id TEXT NOT NULL,
                        title TEXT NOT NULL,
                        location TEXT,
                        job_url TEXT NOT NULL,
                        description TEXT,
                        posted_at TIMESTAMPTZ,
                        discovered_at TIMESTAMPTZ NOT NULL DEFAULT NOW(),
                        is_relevant BOOLEAN NOT NULL DEFAULT TRUE,
                        UNIQUE(company_id, external_id)
                    );
                    """
                )

                cursor.execute(
                    """
                    CREATE TABLE IF NOT EXISTS monitor_history (
                        id SERIAL PRIMARY KEY,
                        company_id INTEGER NOT NULL
                            REFERENCES companies(id)
                            ON DELETE CASCADE,
                        checked_at TIMESTAMPTZ NOT NULL DEFAULT NOW(),
                        status TEXT NOT NULL,
                        jobs_found INTEGER NOT NULL DEFAULT 0,
                        relevant_jobs_found INTEGER NOT NULL DEFAULT 0,
                        error_message TEXT
                    );
                    """
                )

                cursor.execute(
                    """
                    CREATE TABLE IF NOT EXISTS email_log (
                        id SERIAL PRIMARY KEY,
                        job_id INTEGER NOT NULL
                            REFERENCES jobs(id)
                            ON DELETE CASCADE,
                        recipient TEXT NOT NULL,
                        sent_at TIMESTAMPTZ NOT NULL DEFAULT NOW(),
                        status TEXT NOT NULL,
                        error_message TEXT
                    );
                    """
                )

                cursor.execute(
                    """
                    CREATE INDEX IF NOT EXISTS idx_jobs_company_id
                    ON jobs(company_id);
                    """
                )

                cursor.execute(
                    """
                    CREATE INDEX IF NOT EXISTS idx_monitor_history_company_id
                    ON monitor_history(company_id);
                    """
                )

            connection.commit()

    def add_company(
        self,
        name: str,
        careers_url: str,
        connector: str = "auto",
        platform_hint: str | None = None,
        enabled: bool = True,
    ) -> dict[str, Any]:
        # Insert a company or update it if it already exists
        with self.connect() as connection:
            with connection.cursor() as cursor:
                cursor.execute(
                    """
                    INSERT INTO companies (
                        name,
                        careers_url,
                        connector,
                        platform_hint,
                        enabled
                    )
                    VALUES (%s, %s, %s, %s, %s)
                    ON CONFLICT (name)
                    DO UPDATE SET
                        careers_url = EXCLUDED.careers_url,
                        connector = EXCLUDED.connector,
                        platform_hint = EXCLUDED.platform_hint,
                        enabled = EXCLUDED.enabled,
                        updated_at = NOW()
                    RETURNING *;
                    """,
                    (
                        name,
                        careers_url,
                        connector,
                        platform_hint,
                        enabled,
                    ),
                )

                company = cursor.fetchone()

            connection.commit()

        if company is None:
            raise RuntimeError("Company could not be saved")

        return company

    def get_enabled_companies(self) -> list[dict[str, Any]]:
        # Get every company currently being monitored
        with self.connect() as connection:
            with connection.cursor() as cursor:
                cursor.execute(
                    """
                    SELECT *
                    FROM companies
                    WHERE enabled = TRUE
                    ORDER BY name;
                    """
                )

                return list(cursor.fetchall())

    def get_company_by_name(
        self,
        name: str,
    ) -> dict[str, Any] | None:
        # Find one company by its name
        with self.connect() as connection:
            with connection.cursor() as cursor:
                cursor.execute(
                    """
                    SELECT *
                    FROM companies
                    WHERE LOWER(name) = LOWER(%s);
                    """,
                    (name,),
                )

                return cursor.fetchone()

    def job_exists(
        self,
        company_id: int,
        external_id: str,
    ) -> bool:
        # Check whether a job was previously saved
        with self.connect() as connection:
            with connection.cursor() as cursor:
                cursor.execute(
                    """
                    SELECT 1
                    FROM jobs
                    WHERE company_id = %s
                      AND external_id = %s;
                    """,
                    (company_id, external_id),
                )

                return cursor.fetchone() is not None

    def save_job(
        self,
        company_id: int,
        external_id: str,
        title: str,
        job_url: str,
        location: str | None = None,
        description: str | None = None,
        posted_at: datetime | None = None,
        is_relevant: bool = True,
    ) -> dict[str, Any] | None:
        # Save a job unless it already exists
        with self.connect() as connection:
            with connection.cursor() as cursor:
                cursor.execute(
                    """
                    INSERT INTO jobs (
                        company_id,
                        external_id,
                        title,
                        location,
                        job_url,
                        description,
                        posted_at,
                        is_relevant
                    )
                    VALUES (%s, %s, %s, %s, %s, %s, %s, %s)
                    ON CONFLICT (company_id, external_id)
                    DO NOTHING
                    RETURNING *;
                    """,
                    (
                        company_id,
                        external_id,
                        title,
                        location,
                        job_url,
                        description,
                        posted_at,
                        is_relevant,
                    ),
                )

                job = cursor.fetchone()

            connection.commit()

        return job

    def log_monitor_result(
        self,
        company_id: int,
        status: str,
        jobs_found: int = 0,
        relevant_jobs_found: int = 0,
        error_message: str | None = None,
    ) -> None:
        # Record the result of a company check
        with self.connect() as connection:
            with connection.cursor() as cursor:
                cursor.execute(
                    """
                    INSERT INTO monitor_history (
                        company_id,
                        status,
                        jobs_found,
                        relevant_jobs_found,
                        error_message
                    )
                    VALUES (%s, %s, %s, %s, %s);
                    """,
                    (
                        company_id,
                        status,
                        jobs_found,
                        relevant_jobs_found,
                        error_message,
                    ),
                )

                cursor.execute(
                    """
                    UPDATE companies
                    SET last_checked_at = NOW(),
                        updated_at = NOW()
                    WHERE id = %s;
                    """,
                    (company_id,),
                )

            connection.commit()

    def log_email(
        self,
        job_id: int,
        recipient: str,
        status: str,
        error_message: str | None = None,
    ) -> None:
        # Record whether an email was sent successfully
        with self.connect() as connection:
            with connection.cursor() as cursor:
                cursor.execute(
                    """
                    INSERT INTO email_log (
                        job_id,
                        recipient,
                        status,
                        error_message
                    )
                    VALUES (%s, %s, %s, %s);
                    """,
                    (
                        job_id,
                        recipient,
                        status,
                        error_message,
                    ),
                )

            connection.commit()

    def has_successful_check(self, company_id: int) -> bool:
    # Check whether this company completed a previous scan
        with self.connect() as connection:
            with connection.cursor() as cursor:
                cursor.execute(
                    """
                    SELECT 1
                    FROM monitor_history
                    WHERE company_id = %s
                    AND status = 'success'
                    LIMIT 1;
                    """,
                    (company_id,),
                )

                result = cursor.fetchone()

        return result is not None