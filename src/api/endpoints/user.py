from typing import Annotated
from fastapi import APIRouter, status, Depends
from fastapi.responses import JSONResponse
from src.common.docs import NotFoundError, ForbiddenError, UnAuthorizedError, BadRequest
from src.common.dto import (
    CustomerFilter,
    CustomerCreate,
    CustomerID,
    CreateOrderWithCustomerData,
)
from src.services.user import UserService


user_router = APIRouter(prefix="/user", tags=["user"])


@user_router.get(
    "/customers",
    status_code=status.HTTP_200_OK,
    responses={
        status.HTTP_400_BAD_REQUEST: {"model": BadRequest},
        status.HTTP_404_NOT_FOUND: {"model": NotFoundError},
        status.HTTP_401_UNAUTHORIZED: {"model": UnAuthorizedError},
        status.HTTP_403_FORBIDDEN: {"model": ForbiddenError},
    }
)
async def get_customers(
    filters_query: Annotated[CustomerFilter,  Depends(CustomerFilter)],
    user_service: Annotated[UserService, Depends(UserService)]
) -> JSONResponse:
    result = await user_service.get_customers_from_retailcrm(filters=filters_query)
    return JSONResponse(result.json(), result.status_code)


@user_router.post(
    "/create",
    status_code=status.HTTP_201_CREATED,
    responses={
        status.HTTP_400_BAD_REQUEST: {"model": BadRequest},
        status.HTTP_404_NOT_FOUND: {"model": NotFoundError},
        status.HTTP_401_UNAUTHORIZED: {"model": UnAuthorizedError},
        status.HTTP_403_FORBIDDEN: {"model": ForbiddenError},
    }
)
async def create_new_customer(
    query: Annotated[CustomerCreate, Depends(CustomerCreate)],
    user_service: Annotated[UserService, Depends()],
) -> JSONResponse:
    customer = await user_service.create_customer(query)
    return JSONResponse(customer.json(), status_code=customer.status_code)


@user_router.get(
    "/get_orders",
    status_code=status.HTTP_200_OK,
    responses={
        status.HTTP_400_BAD_REQUEST: {"model": BadRequest},
        status.HTTP_404_NOT_FOUND: {"model": NotFoundError},
        status.HTTP_401_UNAUTHORIZED: {"model": UnAuthorizedError},
        status.HTTP_403_FORBIDDEN: {"model": ForbiddenError},
    }
)
async def get_orders_by_customer_id(
    query: Annotated[CustomerID, Depends(CustomerID)],
    service: Annotated[UserService, Depends(UserService)],
) -> JSONResponse:
    result = await service.get_order_by_customer_id(query.customer_id)
    return JSONResponse(result.json(), status_code=result.status_code)


@user_router.post(
    "/create_order",
    status_code=status.HTTP_200_OK,
    responses={
        status.HTTP_400_BAD_REQUEST: {"model": BadRequest},
        status.HTTP_404_NOT_FOUND: {"model": NotFoundError},
        status.HTTP_401_UNAUTHORIZED: {"model": UnAuthorizedError},
        status.HTTP_403_FORBIDDEN: {"model": ForbiddenError},
    }
)
async def create_order_with_customer_data(
    query: Annotated[CreateOrderWithCustomerData, Depends(CreateOrderWithCustomerData)],
    service: Annotated[UserService, Depends(UserService)],
) -> JSONResponse:
    result = await service.create_order_with_customer_data(query)
    return JSONResponse(result.json(), result.status_code)
