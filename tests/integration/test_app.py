from fastapi.testclient import TestClient


def test_post_request_with_special_characters(base_app):
    @base_app.action()
    def my_action(msg):
        return msg

    base_app.add_api_routes()

    test_input = base_app.get_action("my_action", func_kwargs={"msg": "+& "}).dict()["url"]
    expected = "/receiver?func_name=my_action&msg=%2B%26%20"
    assert test_input == expected

    client = TestClient(base_app.app)
    response = client.post("/receiver?func_name=my_action&msg=%2B%26%20")
    assert response.status_code == 200

    test_input = response.content.decode("utf-8")
    expected = "+& "
    assert test_input == expected
