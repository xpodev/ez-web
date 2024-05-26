import ez


router = ez.web.http.router("/plugins")

@router.get("/")
def get_plugins(_):
    return [
        {
            **plugin.info.model_dump(),
            "enabled": plugin.enabled,
        }
        for plugin in ez.plugins.get_plugins()
    ]


@router.post("/{plugin_id}/enable")
def enable_plugin(request):
    # TODO: implement correctly
    # plugin_id = request.path_params["plugin_id"]
    # ez.plugins.enable_plugin(plugin_id)
    # return "Plugin enabled!"
    raise NotImplementedError


@router.post("/{plugin_id}/disable")
def disable_plugin(request):
    # TODO: implement correctly
    # plugin_id = request.path_params["plugin_id"]
    # ez.plugins.disable_plugin(plugin_id)
    # return "Plugin disabled!"
    raise NotImplementedError
