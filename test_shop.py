from shop import order_total


def test_no_coupon():
    assert order_total([1000, 2000]) == 3000


def test_save10():
    assert order_total([10000]) * 0.9 == order_total([10000], "SAVE10")


def test_flat_never_negative():
    assert order_total([1000], "FLAT3000") == 0


def test_http_server():
    # 작은 통합 테스트: 서버를 실제로 띄워 /healthz와 / 응답을 확인
    import json
    import threading
    import urllib.request
    from http.server import HTTPServer

    from shop import Handler
    srv = HTTPServer(("127.0.0.1", 0), Handler)
    threading.Thread(target=srv.serve_forever, daemon=True).start()
    base = f"http://127.0.0.1:{srv.server_port}"
    assert json.load(urllib.request.urlopen(base + "/healthz"))["status"] == "ok"
    assert json.load(urllib.request.urlopen(base + "/"))["total"] == 18000
    srv.shutdown()
