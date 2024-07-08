from abc import  ABC, abstractmethod
from cybulde.utils.utils import get_logger
from cybulde.utils.data_utils import get_repo_address_with_access_token

class DatasetReader(ABC):
    required_columns = {"text", "label", "split", "dataset_name"}
    split_names = {"train", "dev", "test"}

    def __init__(
            self,
            dataset_dir: str,
            dataset_name: str,
            gcp_project_id: str,
            gcp_github_access_token_scret_id: str,
            dvc_remote_repo: str,
            github_user_name: str,
            version: str
            ) -> None:
        self.logger = get_logger(self.__class__.__name__)
        self.dataset_dir = dataset_dir
        self.dataset_name = dataset_name
        self.dvc_remote_repo = get_repo_address_with_access_token(
            gcp_project_id, gcp_github_access_token_secret_id, dvc_remote_repo, github_user_name
        ) 
        self.version = version

