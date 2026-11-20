from fastapi import APIRouter

from .business import router as business_router
from .business_hours import router as business_hours_router
from .gym_policies import router as gym_policies_router
from .memberships import router as memberships_router
from .products import router as products_router
from .trainers import router as trainers_router

admin_router = APIRouter(prefix="/admin")
admin_router.include_router(business_router)
admin_router.include_router(business_hours_router)
admin_router.include_router(gym_policies_router)
admin_router.include_router(memberships_router)
admin_router.include_router(products_router)
admin_router.include_router(trainers_router)
