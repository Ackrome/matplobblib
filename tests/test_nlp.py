from matplobblib.nlp import call_model, description


class FakeResponse:
    ok = True
    status_code = 200
    text = ""

    def json(self):
        return {
            "output": [
                {
                    "content": [
                        {"type": "output_text", "text": "test answer"}
                    ]
                }
            ]
        }


def test_call_model_uses_proxyapi_responses_endpoint(monkeypatch):
    calls = []

    def fake_post(url, headers, json, timeout):
        calls.append(
            {
                "url": url,
                "headers": headers,
                "json": json,
                "timeout": timeout,
            }
        )
        return FakeResponse()

    monkeypatch.setattr("matplobblib.nlp.nlp.requests.post", fake_post)

    result = call_model("hello", api_key="test-key", model="gpt-test", timeout=5)

    assert result == "test answer"
    assert calls[0]["url"] == "https://api.proxyapi.ru/openai/v1/responses"
    assert calls[0]["headers"]["Authorization"] == "Bearer test-key"
    assert calls[0]["json"]["model"] == "gpt-test"
    assert calls[0]["json"]["input"] == "hello"
    assert calls[0]["timeout"] == 5


def test_description_lists_call_model():
    text = description(to_print=False)

    assert "Вызовы языковых моделей" in text
    assert "call_model" in text
    assert "ProxyAPI" in text


def test_description_can_show_only_topics():
    text = description(show_only_keys=True, to_print=False)

    assert "Вызовы языковых моделей" in text
    assert "call_model" not in text
