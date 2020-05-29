import hvac
from nameko.extensions import DependencyProvider


class VaultProvider(DependencyProvider):
    def setup(self):
        url = self.container.config.get("VAULT_URL", "")
        self.client = hvac.Client(url=url)
        if self.client.is_sealed():
            keys = self.container.config.get("VAULT_KEYS", "")
            self.client.sys.submit_unseal_keys(
                keys.split(",")
            )

        if self.client.is_authenticated() is False:
            self.client.token = self.container.config.\
                get("VAULT_TOKEN", "")

    def get_kv_secret(self, mount_point="", path=""):
        try:
            secret = self.client.secrets.kv.\
                read_secret_version(mount_point=mount_point, path=path)
            return secret["data"]
        except Exception:
            return None

    def get_dependency(self, worker_ctx):
        return self
