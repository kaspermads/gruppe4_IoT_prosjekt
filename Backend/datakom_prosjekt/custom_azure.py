from storages.backends.azure_storage import AzureStorage
import os
AZURE_ACCOUNT_KEY = os.environ.get("AZURE_ACCOUNT_KEY")


class AzureMediaStorage(AzureStorage):
    # Must be replaced by your <storage_account_name>
    account_name = os.environ.get("AZURE_ACCOUNT_NAME")
    account_key = AZURE_ACCOUNT_KEY  # Must be replaced by your <storage_account_key>
    azure_container = 'media'
    expiration_secs = None


class AzureStaticStorage(AzureStorage):
    # Must be replaced by your storage_account_name
    account_name = os.environ.get("AZURE_ACCOUNT_NAME")
    account_key = AZURE_ACCOUNT_KEY  # Must be replaced by your <storage_account_key>
    azure_container = 'static'
    expiration_secs = None
