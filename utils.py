import math
from django.utils import timezone

def haversine_distance(lat1, lon1, lat2, lon2):
    """
    Calculate the great circle distance in kilometers between two points 
    on the earth (specified in decimal degrees)
    """
    if lat1 is None or lon1 is None or lat2 is None or lon2 is None:
        return float('inf')

    # Convert decimal degrees to radians 
    lat1, lon1, lat2, lon2 = map(math.radians, [lat1, lon1, lat2, lon2])

    # Haversine formula 
    dlon = lon2 - lon1 
    dlat = lat2 - lat1 
    a = math.sin(dlat/2)**2 + math.cos(lat1) * math.cos(lat2) * math.sin(dlon/2)**2
    c = 2 * math.asin(math.sqrt(a)) 
    r = 6371 # Radius of earth in kilometers. Use 3956 for miles.
    return c * r

def process_expired_donations(donations):
    """
    Utility to check and mark a queryset of donations as expired.
    Usually you would run this in a Celery task, but we can call it on view-load for simplicity.
    """
    now = timezone.now()
    expired_count = 0
    for donation in donations:
        if donation.status == 'PENDING' and now > donation.expiry_time:
            donation.status = 'EXPIRED'
            donation.save(update_fields=['status'])
            expired_count += 1
    return expired_count
