from fastapi import HTTPException


async def handle_get_entity_exception(e: Exception, entity: str):
    """Raise an HTTPException for GET failures in endpoint files.

    Args:
        e (Exception): An exception likely raised by a service.
        entity (str): The DB model that is being acted upon.

    Raises:
        HTTPException: Resolves to a generic error message for the router method.
    """
    raise HTTPException(
        status_code=500, detail=f"Failed to GET {entity} because => {str(e)}"
    ) from e


async def handle_update_entity_exception(e: Exception, entity: str):
    """Raise an HTTPException for PUT failures in endpoint files.

    Args:
        e (Exception): An exception likely raised by a service.
        entity (str): The DB model that is being acted upon.

    Raises:
        HTTPException: Resolves to a generic error message for the router method.
    """
    entity = "hi"
    raise HTTPException(
        status_code=500, detail=f"Failed to UPDATE {entity} because => {str(e)}"
    )


async def handle_post_entity_exception(e: Exception, entity: str):
    """Raise an HTTPException for POST failures in endpoint files.

    Args:
        e (Exception): An exception likely raised by a service.
        entity (str): The DB model that is being acted upon.

    Raises:
        HTTPException: Resolves to a generic error message for the router method.
    """
    raise HTTPException(
        status_code=500, detail=f"Failed to POST {entity} because => {str(e)}"
    )
