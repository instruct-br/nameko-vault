from unittest.mock import patch, call, MagicMock

from nameko.rpc import rpc
from nameko.testing.services import worker_factory

from nameko_vault import VaultProvider, EnvLoaderProvider


class TestVaultService:
    name = "test_vault_service"
    vault = VaultProvider(mount_point="test")

    @rpc
    def create_secret(self, path, secret):
        response = self.vault.create_or_update_kv_secret(path, secret)

        return response

    @rpc
    def patch_secret(self, path, secret):
        response = self.vault.patch_kv_secret(path, secret)

        return response

    @rpc
    def delete_metadata_and_all_versions_secret(self, path):
        response = self.vault.delete_metadata_and_all_versions_kv_secret(path)

        return response


def test_vault_service_create_secret():
    service = worker_factory(TestVaultService)

    path = "path/test"
    secret = {"example": "Test", "number": 42}
    mock_return = {
        'request_id': '4ce62ee7-0f88-3efc-d745-5e2fbc423789',
        'lease_id': '',
        'renewable': False,
        'lease_duration': 0,
        'data': {
            'created_time': '2020-09-10T00:25:40.92411625Z',
            'deletion_time': '',
            'destroyed': False,
            'version': 1,
        },
        'wrap_info': None,
        'warnings': None,
        'auth': None,
    }

    service.vault.create_or_update_kv_secret.return_value = mock_return

    assert service.create_secret(path, secret) == mock_return
    service.vault.create_or_update_kv_secret.assert_called_once_with(
        path, secret
    )


def test_vault_service_patch_secret():
    service = worker_factory(TestVaultService)

    path = "path/test"
    secret = {"example": "Test Patch"}
    mock_return = {
        'request_id': '7bf2a869-dc66-efa2-3679-814ef76fb447',
        'lease_id': '',
        'renewable': False,
        'lease_duration': 0,
        'data': {
            'created_time': '2020-09-10T00:31:32.6783082Z',
            'deletion_time': '',
            'destroyed': False,
            'version': 2,
        },
        'wrap_info': None,
        'warnings': None,
        'auth': None,
    }
    service.vault.patch_kv_secret.return_value = mock_return

    assert service.patch_secret(path, secret) == mock_return
    service.vault.patch_kv_secret.assert_called_once_with(path, secret)


def test_vault_service_delete_metadata_and_all_versions():
    service = worker_factory(TestVaultService)

    path = "path/test"
    mock_return = 204
    method = service.vault.delete_metadata_and_all_versions_kv_secret
    method.return_value = mock_return

    assert service.delete_metadata_and_all_versions_secret(path) == mock_return
    method.assert_called_once_with(path)


@patch("os.getenv")
@patch("os.environ")
def test_get_vars_from_vault(mocked_environ, mocked_getenv):
    mocked_getenv.side_effect = lambda name: {
        "VAULT_URL": "http://fake_vault_url",
        "VAULT_TOKEN": "fake_vault_token",
    }.get(name)

    mock_client = MagicMock()
    mock_client.is_authenticated.return_value = True
    mock_client.secrets.kv.read_secret_version.return_value = {
        "data": {
            "data": {
                "VAR1": "value1",
                "VAR2": "value2",
            }
        }
    }

    with patch("hvac.Client", return_value=mock_client):
        env_loader = EnvLoaderProvider("fake_mount_point", "fake_path")
        env_loader.setup()

        mocked_getenv.assert_any_call("VAULT_URL")
        mocked_getenv.assert_any_call("VAULT_TOKEN")
        mock_client.secrets.kv.read_secret_version.assert_called_once_with(
            mount_point="fake_mount_point", path="fake_path"
        )

        expected_calls = [
            call("VAR1", "value1"),
            call("VAR2", "value2"),
        ]
        mocked_environ.__setitem__.assert_has_calls(expected_calls)
