import time
from datetime import datetime
import json

class CacheMetrics:
    def __init__(self):
        self.cache_hits = 0
        self.cache_misses = 0
        self.total_time_saved = 0  # in seconds
        self.requests_served = 0
        self.start_time = datetime.now()
        
    def record_hit(self, time_saved):
        self.cache_hits += 1
        self.total_time_saved += time_saved
        self.requests_served += 1
        
    def record_miss(self):
        self.cache_misses += 1
        self.requests_served += 1
        
    def get_metrics(self):
        uptime = (datetime.now() - self.start_time).total_seconds()
        hit_ratio = (self.cache_hits / self.requests_served * 100) if self.requests_served > 0 else 0
        avg_time_saved = (self.total_time_saved / self.cache_hits) if self.cache_hits > 0 else 0
        
        return {
            "cache_hits": self.cache_hits,
            "cache_misses": self.cache_misses,
            "hit_ratio": round(hit_ratio, 2),
            "total_time_saved": round(self.total_time_saved, 2),
            "avg_time_saved": round(avg_time_saved, 2),
            "requests_served": self.requests_served,
            "uptime_seconds": round(uptime, 2)
        }
        
    def save_metrics(self):
        with open('cache_stats.json', 'w') as f:
            json.dump(self.get_metrics(), f, indent=2)

# Global metrics instance
metrics = CacheMetrics()
