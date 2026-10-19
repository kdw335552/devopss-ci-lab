"""DevOps 과목 예제 앱 — 주문 금액 계산 + 아주 작은 HTTP 서버(표준 라이브러리만)"""
import json
import os
from http.server import BaseHTTPRequestHandler, HTTPServer

VERSION = os.environ.get("APP_VERSION", "dev")


def order_total(prices, coupon=None):
    """상품 가격 목록과 쿠폰으로 결제 금액을 계산한다. 쿠폰: SAVE10(10%), FLAT3000(3000원)"""
    subtotal = sum(prices)
    if coupon == "SAVE10":
        subtotal = subtotal * 0.9
    elif coupon == "FLAT3000":
        subtotal = subtotal - 3000
    return max(int(subtotal), 0)


class Handler(BaseHTTPRequestHandler):
    def do_GET(self):
        if self.path == "/healthz":
            body = {"status": "ok", "version": VERSION}
        else:
            body = {"total": order_total([12000, 8000], "SAVE10"), "version": VERSION}
        data = json.dumps(body).encode()
        self.send_response(200)
        self.send_header("Content-Type", "application/json")
        self.end_headers()
        self.wfile.write(data)

    def log_message(self, *args):
        pass


if __name__ == "__main__":
    HTTPServer(("0.0.0.0", 8000), Handler).serve_forever()
# 할인 규칙 메모
