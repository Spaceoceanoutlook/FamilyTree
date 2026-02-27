from fastapi import Request


def get_client_info(request: Request) -> tuple[str, str]:
    forwarded = request.headers.get("x-forwarded-for")
    ip = (
        forwarded.split(",")[0].strip()
        if forwarded
        else (request.client.host if request.client else "-")
    )
    ua = request.headers.get("user-agent", "")[:200]
    return ip, ua
