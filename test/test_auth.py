# content of test_class.py
class TestAdd:
    def test_one(self):
        x = "this"
        assert "h" in x

    def test_two(self):
        x = "hello"
        assert hasattr(x, "check")

class TestCreate:
    def test_one(self):
        x = "than"
        assert "h" in x

    def test_two(self):
        x = "potato"
        assert hasattr(x, "check")

    # content of test_tmpdir.py
def test_needsfiles(tmpdir):
    print(tmpdir)
    assert 0
