from core import plugin, model

class _local(plugin._plugin):
    version = 1.1

    def install(self):
        # Register models
        model.registerModel("localDelete","_localDelete","_action","plugins.local.models.action")
        model.registerModel("localWrite","_localWrite","_action","plugins.local.models.action")
        return True

    def uninstall(self):
        # deregister models
        model.deregisterModel("localDelete","_localDelete","_action","plugins.local.models.action")
        model.deregisterModel("localWrite","_localWrite","_action","plugins.local.models.action")
        return True

    def upgrade(self,LatestPluginVersion):
        if self.version < 1.1:
            model.registerModel("localWrite","_localWrite","_action","plugins.local.models.action")
        return True