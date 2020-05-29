# nameko-vault

Extension for [Nameko](https://www.nameko.io/) that integrates with [Vault](https://www.vaultproject.io/).

To use this tool it is necessary to configure the following parameters in your nameko config.yml file:

```
VAULT_URL: <vault_api_url>
VAULT_TOKEN: <authentication_token>
```

Up to the present moment there is only support for the key_value backend, to use it just inform the path where the keys are located as in the example below:

```
vault = VaultProvider()
vault.get_kv_secret(mount_point="example", path="path/test")
```
