import wandb


def new_wandb_project(project: str, entity: str):
    wandb.init(project, entity)
