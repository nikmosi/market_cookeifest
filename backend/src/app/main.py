from litestar import Litestar, Request, get

from app.routes import route_handlers


@get("/")
async def index() -> str:
    return "Hello, world!"


@get("/ip")
async def get_ip(request: Request) -> str:
    client_ip = request.scope.get("client", ["Unknown"])
    return f"Your IP address is: {client_ip}"


def create_app() -> Litestar:
    return Litestar(
        route_handlers=route_handlers + [index, get_ip],
    )


app = create_app()
