from core import plugin, model

class _local(plugin._plugin):
    version = 1.0

    def install(self):
        # Register models
        model.registerModel("localDelete","_localDelete","_action","plugins.local.models.action")
        return True

    def uninstall(self):
        # deregister models
        model.deregisterModel("localDelete","_localDelete","_action","plugins.local.models.action")
        return True

    def upgrade(self,LatestPluginVersion):
        return True
