import logging

from shop_app.logging.context import request_id_ctx


class RequestIdFilter(logging.Filter):
    """Добавляет request_id в LogRecord (можно использовать в форматтере)."""

    def filter(self, record: logging.LogRecord) -> bool:
        record.request_id = request_id_ctx.get()
        return True
