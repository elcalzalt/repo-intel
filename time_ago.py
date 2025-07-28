from datetime import datetime
import pytz

def time_ago(date_str):
    try:
        # Parse the ISO format date string
        if date_str.endswith('Z'):
            # Handle UTC timezone indicator 'Z'
            date_str = date_str[:-1]
            date_time = datetime.strptime(date_str, "%Y-%m-%dT%H:%M:%S")
            date_time = date_time.replace(tzinfo=pytz.UTC)
        else:
            date_time = datetime.strptime(date_str, "%Y-%m-%dT%H:%M:%S")
        
        # Get current time in UTC
        now = datetime.now(pytz.UTC)
        
        # Calculate the time difference
        time_diff = now - date_time
        seconds = time_diff.total_seconds()
        
        # Convert to appropriate units
        if seconds < 60:
            return f"{int(seconds)} seconds ago"
        elif seconds < 3600:
            minutes = int(seconds / 60)
            return f"{minutes} minute{'s' if minutes != 1 else ''} ago"
        elif seconds < 86400:  # seconds in a day
            hours = int(seconds / 3600)
            return f"{hours} hour{'s' if hours != 1 else ''} ago"
        elif seconds < 604800:  # seconds in a week
            days = int(seconds / 86400)
            return f"{days} day{'s' if days != 1 else ''} ago"
        elif seconds < 2629746:  # seconds in a month (approximate)
            weeks = int(seconds / 604800)
            return f"{weeks} week{'s' if weeks != 1 else ''} ago"
        elif seconds < 31556952:  # seconds in a year
            months = int(seconds / 2629746)
            return f"{months} month{'s' if months != 1 else ''} ago"
        else:
            years = int(seconds / 31556952)
            return f"{years} year{'s' if years != 1 else ''} ago"
    except ValueError:
        return date_str