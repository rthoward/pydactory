from typing import Any

from faker import Faker


class FakeGen:
    """
    A wrapper around Faker to integrate it with Pydactory.
    """

    def __init__(self):
        self.fake = Faker()

    def __getattr__(self, name: str) -> Any:
        """
        Search for a Faker method matching `name` and wrap it in a
        function (thunk) to delay its evaluation until generation time.
        """
        try:
            fake_func = getattr(self.fake, name)

            def fake_func_wrapper(*args, **kwargs):
                return lambda _field: fake_func(*args, **kwargs)

            return fake_func_wrapper
        except AttributeError:
            raise AttributeError(f"Not a valid fake: {name}")

    def __call__(self, provider: str) -> Any:
        return getattr(self.fake, provider)
