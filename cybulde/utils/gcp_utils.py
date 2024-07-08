from google.cloud import secretmanager



def access_secret_version(
        gcp_project_id: str,
        gcp_secret_id: str,
        version_id: str = "1"
        ) -> str:
            client = secretmanager.SecretManagerServiceClient()
            name = f"projects/{gcp_project_id}/secrets/{gcp_secret_id}/versions/{version_id}"
            response = client.access_secret_version(request={"name":name})
            payload = response.payload.data.decode('UTF-8')
            return payload
