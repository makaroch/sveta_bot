from aiogram import Router
from src.handlers.user_private import user_private_router
# from src.handlers.admin_hendlers import admin_private_router
# from src.handlers.admin_group import admin_group_router

handlers_router = Router()

handlers_router.include_routers(
    user_private_router,
    # admin_private_router,
    # admin_group_router,
)
