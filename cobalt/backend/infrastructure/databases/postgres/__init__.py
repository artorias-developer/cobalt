#  Copyright (C) 2026 ArtoriasCode
#  Author: ArtoriasCode
#  Repository: https://github.com/ArtoriasCode/cobalt
#  SPDX-License-Identifier: AGPL-3.0-or-later

from domain.exceptions import NotFoundError
from domain.enums import PermissionsEnum
from application.dtos import (
    RoleDto,
    RolesGetPageDto,
    RoleCreateDto,
    RoleUpdateDto,
    UsersGetPageDto,
    UserCreateDto,
    UserUpdateDto
)
from application.contracts.services import (
    AbstractUsersService,
    AbstractRolesService
)
from application.contracts.loggers import AbstractLogger


async def _has_admin_user(
    users_service: AbstractUsersService,
    required_permissions: set
) -> bool:
    """
    Checks if any user with the required permissions exists.

    Parameters:
    - users_service: AbstractUsersService object.
    - required_permissions: Set of required permissions.

    Returns:
    - bool: True if such a user exists, False otherwise.
    """
    current_page = 1
    total_pages = 1

    while current_page <= total_pages:
        users_page_dto = UsersGetPageDto(
            page=current_page,
            limit=100
        )

        try:
            users_page = await users_service.get_page(
                dto=users_page_dto
            )
        except NotFoundError:
            break

        for user in users_page.users:
            user_permissions = set(user.role.permissions)

            if required_permissions.issubset(user_permissions):
                return True

        total_pages = users_page.pages
        current_page += 1

    return False

async def _get_or_create_admin_role(
    roles_service: AbstractRolesService,
    role_name: str,
    required_permissions: set,
    logger: AbstractLogger
) -> RoleDto:
    """
    Finds or creates a role with the given name and ensures it has all permissions.

    Parameters:
    - roles_service: AbstractRolesService object.
    - role_name: Name of the role to find or create.
    - required_permissions: Set of required permissions.
    - logger: AbstractLogger logger.

    Returns:
    - RoleDto: RoleDto object.
    """
    admin_role = None
    current_page = 1
    total_pages = 1

    while current_page <= total_pages:
        roles_page_dto = RolesGetPageDto(
            page=current_page,
            limit=100
        )

        try:
            roles_page = await roles_service.get_page(
                dto=roles_page_dto
            )
        except NotFoundError:
            break

        for role in roles_page.roles:
            if role.name != role_name:
                continue

            admin_role = role
            break

        if admin_role:
            break

        total_pages = roles_page.pages
        current_page += 1

    if not admin_role:
        role_dto = RoleCreateDto(
            name=role_name,
            permissions=list(PermissionsEnum)
        )

        admin_role = await roles_service.create_one(
            dto=role_dto
        )

        logger.info("Administrator role created with all permissions.")
    else:
        role_permissions = set(admin_role.permissions)

        if not required_permissions.issubset(role_permissions):
            role_dto = RoleUpdateDto(
                permissions=list(PermissionsEnum)
            )

            admin_role = await roles_service.update_one(
                role_id=admin_role.id,
                dto=role_dto
            )

            logger.info("Administrator role updated with all permissions.")

    return admin_role

async def _ensure_admin_user(
    users_service: AbstractUsersService,
    login: str,
    password: str,
    role_id,
    logger: AbstractLogger
) -> None:
    """
    Creates or updates the admin user with the given login and password.

    Parameters:
    - users_service: AbstractUsersService object.
    - login: Login of the admin user.
    - password: Password of the admin user.
    - role_id: ID of the admin role.
    - logger: AbstractLogger logger.

    Returns:
    - None.
    """
    try:
        existing_user = await users_service.get_one_by_login(
            login=login
        )
    except NotFoundError:
        existing_user = None

    if existing_user:
        user_dto = UserUpdateDto(
            login=login,
            password=password,
            role_id=role_id
        )

        updated_user = await users_service.update_one(
            user_id=existing_user.id,
            dto=user_dto
        )

        logger.info(f'Admin user "{updated_user.login}" updated with password "{password}".')
    else:
        user_dto = UserCreateDto(
            login=login,
            password=password,
            role_id=role_id
        )

        created_user = await users_service.create_one(
            dto=user_dto
        )

        logger.info(f'Admin user "{created_user.login}" created with password "{password}".')

async def check_default_user(
    roles_service: AbstractRolesService,
    users_service: AbstractUsersService,
    logger: AbstractLogger
) -> None:
    """
    Creates a default admin user if necessary.

    Parameters:
    - roles_service: AbstractRolesService object.
    - users_service: AbstractUsersService object.
    - logger: AbstractLogger logger.

    Returns:
    - None.
    """
    role_name = "Administrator"
    login = "admin"
    password = "admin"

    required_permissions = {
        PermissionsEnum.ROLES_VIEW,
        PermissionsEnum.ROLES_CREATE,
        PermissionsEnum.ROLES_UPDATE,
        PermissionsEnum.ROLES_DELETE,
        PermissionsEnum.USERS_VIEW,
        PermissionsEnum.USERS_CREATE,
        PermissionsEnum.USERS_UPDATE,
        PermissionsEnum.USERS_DELETE
    }

    if await _has_admin_user(users_service, required_permissions):
        return

    admin_role = await _get_or_create_admin_role(
        roles_service=roles_service,
        role_name=role_name,
        required_permissions=required_permissions,
        logger=logger
    )

    await _ensure_admin_user(
        users_service=users_service,
        login=login,
        password=password,
        role_id=admin_role.id,
        logger=logger
    )