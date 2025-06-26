from datetime import datetime

def parse_detected_at(detected_at_str):
        """Parses a detected_at date string in multiple possible formats."""
        formats = [
            "%Y-%m-%dT%H:%M:%S.%fZ",        # OpenSearch/ISO format
            "%b %d, %Y @ %H:%M:%S.%f",      # Excel format
        ]
        
        for fmt in formats:
            try:
                return datetime.strptime(detected_at_str, fmt)
            except (ValueError, TypeError):
                continue
        raise ValueError(f"Unsupported date format: {detected_at_str}")