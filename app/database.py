from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker, declarative_base
import os

# Use DATABASE_URL environment variable when provided. This makes it easy to
# switch between IPv4/IPv6 or remote hosts without changing code.
# Examples:
#  - IPv4 localhost (default): postgresql://admin:admin@localhost/logistiscout
#  - IPv6 loopback literal:  postgresql://admin:admin@[::1]/logistiscout
#  - Remote IPv6 address:    postgresql://user:pass@[2001:db8::1]:5432/dbname
SQLALCHEMY_DATABASE_URL = os.getenv(
	"DATABASE_URL", "postgresql://admin:admin@localhost/logistiscout"
)

# SQLAlchemy / psycopg accept IPv6 literals in the host portion if wrapped in
# square brackets. No additional engine flags are required here.
engine = create_engine(SQLALCHEMY_DATABASE_URL)
SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)
Base = declarative_base()