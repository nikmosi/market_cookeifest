from litestar import Litestar


def create_app() -> Litestar:
    return Litestar()


app = create_app()
