import hvac
from nameko.extensions import DependencyProvider


class VaultProvider(DependencyProvider):
    def setup(self):
        url = self.container.config.get("VAULT_URL", "")
        self.client = hvac.Client(url=url)

    def get_dependency(self, worker_ctx):
        if self.client.is_sealed():
            keys = worker_ctx.container.config.get("VAULT_KEYS", "")
            self.client.sys.submit_unseal_keys(
                keys.split(",")
            )

        if self.client.is_authenticated() is False:
            self.client.token = worker_ctx.container.config.\
                get("VAULT_TOKEN", "")

        return self.client.secrets.kv.read_secret_version
