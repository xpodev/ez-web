from sandbox.applications import Application


class PluginApplication(Application):
    def __init__(self, oid, permissions):
        super().__init__(oid, permissions)

    def __repr__(self):
        return f"<Plugin {self.oid}>"
