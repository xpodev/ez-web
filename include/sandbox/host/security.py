from ..security import Permission


class AppHostPermission(Permission):
    CreateApplications = 1
    ManageApplications = 2
    RegisterEvents = 4
    InvokeEvents = 8
