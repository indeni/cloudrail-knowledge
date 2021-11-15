from enum import Enum


class GcpResourceType(Enum):
    NONE = 'none'
    GOOGLE_SQL_DATABASE_INSTANCE = 'google_sql_database_instance'
    GOOGLE_COMPUTE_INSTANCE = 'google_compute_instance'
    GOOGLE_COMPUTE_HEALTH_CHECK = 'google_compute_health_check'
    GOOGLE_COMPUTE_NETWORK = 'google_compute_network'
    GOOGLE_PROJECT = 'google_project'
