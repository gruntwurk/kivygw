from kivygw import snake_case


def test_snake_case():
    assert snake_case("SomeThing") == "some_thing"
    assert snake_case("someThing") == "some_thing"
    assert snake_case("some_thing") == "some_thing"
    assert snake_case("something") == "something"
    assert snake_case("") == ""

