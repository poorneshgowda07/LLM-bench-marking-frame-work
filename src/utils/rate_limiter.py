"""Token bucket rate limiter for provider API calls."""
import time
import threading
from typing import Dict


class RateLimiter:
    """Thread-safe token bucket rate limiter.

    Ensures we don't exceed provider rate limits by controlling
    the number of requests per minute.
    """

    def __init__(self, requests_per_minute: int):
        self.requests_per_minute = requests_per_minute
        self.min_interval = 60.0 / requests_per_minute
        self._lock = threading.Lock()
        self._last_request_time = 0.0

    def acquire(self):
        """Block until a request slot is available."""
        with self._lock:
            elapsed = time.monotonic() - self._last_request_time
            if elapsed < self.min_interval:
                time.sleep(self.min_interval - elapsed)
            self._last_request_time = time.monotonic()

    def __enter__(self):
        self.acquire()
        return self

    def __exit__(self, *args):
        pass


# Global registry of rate limiters per provider
_limiters: Dict[str, RateLimiter] = {}
_lock = threading.Lock()


def get_rate_limiter(provider: str, requests_per_minute: int) -> RateLimiter:
    """Get or create a rate limiter for a provider."""
    with _lock:
        if provider not in _limiters:
            _limiters[provider] = RateLimiter(requests_per_minute)
        return _limiters[provider]
