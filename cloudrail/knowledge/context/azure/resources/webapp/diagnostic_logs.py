from dataclasses import dataclass


@dataclass
class DiagnosticLogs:
    """
            Attributes:
                detailed_error_logging_enabled: Indicate if the detailed error logging enable.
                http_logging_enabled: Indicate if the http logging enable.
                request_tracing_enabled: Indicate if the request tracing logging enable.
    """
    detailed_error_logging_enabled: bool
    http_logging_enabled: bool
    request_tracing_enabled: bool
