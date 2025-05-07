import json
import time
from datetime import datetime, timedelta
from cache_metrics import metrics

class URLCacheManager:
    def __init__(self, cache_file='url_cache.json', cache_duration_hours=24):
        self.cache_file = cache_file
        self.cache_duration = timedelta(hours=cache_duration_hours)
        self.cache = self.load_cache()

    def load_cache(self):
        """Load cache from file or create new if not exists"""
        try:
            with open(self.cache_file, 'r') as f:
                cache_data = json.load(f)
                # Convert string timestamps back to datetime objects
                return {k: {'features': v['features'], 
                              'timestamp': datetime.fromisoformat(v['timestamp'])}
                       for k, v in cache_data.items()}
        except (json.JSONDecodeError, KeyError, FileNotFoundError):
            return {}

    def save_cache(self):
        """Save cache to file"""
        cache_data = {k: {'features': v['features'],
                         'timestamp': v['timestamp'].isoformat()}
                     for k, v in self.cache.items()}
        with open(self.cache_file, 'w') as f:
            json.dump(cache_data, f, indent=2)

    def get_cached_result(self, url):
        """Get cached result for URL if exists and not expired"""
        if url in self.cache:
            cache_entry = self.cache[url]
            if datetime.now() - cache_entry['timestamp'] <= self.cache_duration:
                # Estimate time saved (average time to process a URL)
                time_saved = 2.5  # seconds (typical processing time)
                metrics.record_hit(time_saved)
                return cache_entry['features']
            else:
                # Remove expired entry
                del self.cache[url]
                self.save_cache()
        metrics.record_miss()
        return None

    def cache_result(self, url, features):
        """Cache result for URL"""
        self.cache[url] = {
            'features': features,
            'timestamp': datetime.now()
        }
        self.save_cache()
        # Also save metrics
        metrics.save_metrics()

    def clear_expired(self):
        """Clear expired entries from cache"""
        current_time = datetime.now()
        expired = [url for url, data in self.cache.items()
                  if current_time - data['timestamp'] > self.cache_duration]
        for url in expired:
            del self.cache[url]
        if expired:
            self.save_cache()
