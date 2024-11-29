from litestar.types import ControllerRouterHandler

from app.domain.products import ProductsController

route_handlers: list[ControllerRouterHandler] = [ProductsController]
