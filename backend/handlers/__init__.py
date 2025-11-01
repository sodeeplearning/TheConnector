from aiogram import Router

from . import post, watch


router = Router()

router.include_routers(post.router, watch.router)
