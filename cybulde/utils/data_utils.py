from cybulde.utils.gcp_utils import access_secret_version




def get_repo_address_with_access_token(
        gcp_project_id: str,
        gcp_github_access_token_secret_id: str,
        dvc_remote_repo: str,
        github_user_name: str
        ) -> str:
    access_token = access_secret_version(gcp_project_id, gcp_github_access_token_secret_id)
    repo_address = dvc_remote_repo.replace("https://", "")
    return f"https://{github_user_name}:{access_token}@{repo_address}"
