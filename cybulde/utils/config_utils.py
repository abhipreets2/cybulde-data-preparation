from cybulde.config_schemas import config_schema
import yaml
import logging
import logging.config
from typing import Any, Optional
from hydra.types import TaskFunction
from omegaconf import DictConfig, OmegaConf
import hydra
import importlib
from dataclasses import asdict

def custom_instantiate(config: Any) -> Any:
    config_as_dict = asdict(config)
    if "_target_" not in config_as_dict:
        raise ValueError("Config does not have _target_ key")

    _target_ = config_as_dict["_target_"]
    _partial_ = config_as_dict.get("_partial_", False)

    config_as_dict.pop("_target_", None)
    config_as_dict.pop("_partial_", None)

    splitted_target = _target_.split(".")
    module_name, class_name = ".".join(splitted_target[:-1]), splitted_target[-1]

    module = importlib.import_module(module_name)
    _class = getattr(module, class_name)
    if _partial_:
        return partial(_class, **config_as_dict)
    return _class(**config_as_dict)

def get_config(config_path: str, config_name: str):
    setup_config()
    setup_logger()
    def main_decorator(task_function: TaskFunction) -> Any:
        @hydra.main(config_path=config_path, config_name=config_name, version_base=None)
        def decorated_main(dict_config: Optional[DictConfig] = None) -> Any:
            config = OmegaConf.to_object(dict_config)
            return task_function(config)
        return decorated_main

    return main_decorator


    
def setup_config() -> None:
    config_schema.setup_config()

def setup_logger() -> None:
    with open("./cybulde/configs/hydra/job_logging/custom.yaml", "r") as stream:
        config = yaml.load(stream, Loader=yaml.FullLoader)
    logging.config.dictConfig(config)
