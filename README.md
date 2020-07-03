# nameko-vault

Extension for [Nameko](https://www.nameko.io/) that integrates with
[Vault](https://www.vaultproject.io/).

To use this tool it is necessary to configure the following parameters in your
nameko config.yml file:

```
VAULT_URL: <vault_api_url>
VAULT_TOKEN: <authentication_token>
```

## Usage

To use the tool it's needed inform the mount point of the path in which you want
to obtain any secrets. This mount point can be informed when instantiating the
provider or passing this information directly to the method being used.

### Example 1:
```python
# path: example/path/secret
vault = VaultProvider(mount_point="example")
vault.get_kv_secret(path="path/secret")
```

### Example 2:
```python
# path: example/path/secret
vault = VaultProvider()
vault.get_kv_secret(mount_point="example", path="path/secret")
```

## List Secrets

The method `get_kv_secrets_list` returns a list of secrets contained in a given
path

```python
vault = VaultProvider()
vault.get_kv_secrets_list(mount_point="example", path="path")
```
```
['path/test1', 'path/test2']
```


## KV Secret Data

The method `get_kv_secret` returns the content cotained in a given path

```python
vault = VaultProvider()
vault.get_kv_secret(mount_point="example", path="path/test")
```
```
[
   {
      "data":{
         "pass":"test",
         "user":"sample"
      },
      "metadata":{
         "created_time":"2020-07-01T17:44:48.054175763Z",
         "deletion_time":"",
         "destroyed":False,
         "version":1
      }
   }
]
```
