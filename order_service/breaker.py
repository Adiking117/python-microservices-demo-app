import pybreaker

rabbitmq_breaker = pybreaker.CircuitBreaker(
    fail_max=3,
    reset_timeout=30
)