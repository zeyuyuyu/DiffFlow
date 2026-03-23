import random
import time
import asyncio
from typing import List, Tuple

class Agent:
    def __init__(self, id: str):
        self.id = id
        self.neighbors = set()
        self.state = 'idle'
        self.task = None

    def add_neighbor(self, neighbor: 'Agent'):
        self.neighbors.add(neighbor)
        neighbor.neighbors.add(self)

    async def coordinate(self):
        while True:
            if self.state == 'idle':
                await self.find_task()
            elif self.state == 'working':
                await self.execute_task()
            else:
                raise ValueError(f'Invalid state: {self.state}')
            await asyncio.sleep(random.uniform(0.1, 1.0))

    async def find_task(self):
        self.state = 'searching'
        task = None
        for neighbor in self.neighbors:
            if neighbor.state == 'working' and neighbor.task is not None:
                task = neighbor.task
                break
        if task is None:
            self.state = 'idle'
        else:
            self.state = 'working'
            self.task = task

    async def execute_task(self):
        print(f'Agent {self.id} executing task: {self.task}')
        await asyncio.sleep(random.uniform(1.0, 5.0))
        self.state = 'idle'
        self.task = None

async def run_simulation(num_agents: int, num_tasks: int):
    agents: List[Agent] = [Agent(str(i)) for i in range(num_agents)]

    # Connect agents randomly
    for i in range(num_agents):
        for j in range(i + 1, num_agents):
            if random.random() < 0.5:
                agents[i].add_neighbor(agents[j])

    # Assign tasks to random agents
    for _ in range(num_tasks):
        agent = random.choice(agents)
        agent.task = f'Task {len(agent.task_history) + 1}'
        agent.state = 'working'

    # Run coordination protocol
    await asyncio.gather(*[agent.coordinate() for agent in agents])

if __name__ == '__main__':
    asyncio.run(run_simulation(10, 5))