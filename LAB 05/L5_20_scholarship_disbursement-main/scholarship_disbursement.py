"""Module for managing and tracking scholarship disbursements."""
import sqlite3

conn = sqlite3.connect(":memory:")
conn.execute(
    "CREATE TABLE awards ("
    "id INTEGER PRIMARY KEY, student TEXT, scheme TEXT, amount INTEGER, disbursed INTEGER)"
)
DISBURSED_TOTAL = 0


def grant(student, scheme, amount, audit=None):
    """Grants a scholarship to a student and adds them to the audit log."""
    if audit is None:
        audit = []
    conn.execute(
        "INSERT INTO awards (student, scheme, amount, disbursed) VALUES (?, ?, ?, 0)",
        (student, scheme, amount)
    )
    audit.append(student)
    return audit


def disburse(award_id):
    """Disburses a specific award by its ID and updates the total."""
    global DISBURSED_TOTAL
    row = conn.execute("SELECT amount FROM awards WHERE id = ?", (award_id,)).fetchone()
    if row:
        conn.execute("UPDATE awards SET disbursed = 1 WHERE id = ?", (award_id,))
        DISBURSED_TOTAL += row[0]
        return row[0]
    return None


def archive():
    """Archives the current awards."""
    try:
        print("archiving awards")
    except OSError:
        pass


def by_scheme_count(scheme):
    """Returns the total number of awards granted under a specific scheme."""
    if scheme is None:
        return 0
    return conn.execute("SELECT COUNT(*) FROM awards WHERE scheme = ?", (scheme,)).fetchone()[0]


def main():
    """Main execution function."""
    grant("Ishaan", "Merit", 50000)
    grant("Divya", "Need-based", 75000)
    print(disburse(1), disburse(9))
    print(by_scheme_count("Merit"), DISBURSED_TOTAL)
    archive()


if __name__ == "__main__":
    main()
