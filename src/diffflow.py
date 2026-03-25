import os
import torch
import torch.distributed as dist
from torch.nn.parallel import DistributedDataParallel as DDP

class DistributedDiffusionTrainer:
    def __init__(self, model, optimizer, device='cuda'):
        self.model = model
        self.optimizer = optimizer
        self.device = device
        
        # Initialize distributed training
        dist.init_process_group(backend='nccl')
        self.rank = dist.get_rank()
        self.world_size = dist.get_world_size()
        
        # Wrap the model with DistributedDataParallel
        self.model = DDP(self.model.to(self.device), device_ids=[self.rank])
        
    def train_step(self, input_data, target_data):
        self.optimizer.zero_grad()
        output = self.model(input_data)
        loss = F.mse_loss(output, target_data)
        loss.backward()
        self.optimizer.step()
        return loss.item()
    
    def save_checkpoint(self, save_path):
        if self.rank == 0:
            torch.save(self.model.state_dict(), save_path)
            
    def load_checkpoint(self, load_path):
        self.model.load_state_dict(torch.load(load_path, map_location=f'cuda:{self.rank}'))
