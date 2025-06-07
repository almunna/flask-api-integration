def _call_instagram_api(endpoint: str, params: dict = None, method: str = "GET", filter_func=None) -> dict:
    from flask import current_app
    import requests

    access_token = current_app.config.get("INSTAGRAM_ACCESS_TOKEN")
    api_base_url = current_app.config.get("INSTAGRAM_API_BASE_URL")

    if params is None:
        params = {}
    params["access_token"] = access_token

    url = f"{api_base_url}/{endpoint}"

    try:
        response = requests.request(method, url, params=params)
        response.raise_for_status()
        data = response.json()

        if filter_func and "data" in data:
            data["data"] = filter_func(data["data"])

        return data
    except requests.RequestException as e:
        return {
            "error": str(e),
            "details": getattr(e.response, "text", None)
        }
