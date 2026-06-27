import logging
import asyncio
from typing import List, Dict

logger = logging.getLogger("BackgroundQueueManager")

class BackgroundQueueManager:
    """Manages the background execution of embedding jobs to prevent blocking."""
    
    def __init__(self):
        self.embedding_queue: asyncio.Queue = asyncio.Queue()
        self.failed_jobs: List[Dict] = []
        self.is_processing = False
        
    async def enqueue_job(self, job: Dict):
        """Adds an embedding job to the queue."""
        await self.embedding_queue.put(job)
        logger.debug(f"Job added to embedding queue. Queue size: {self.embedding_queue.qsize()}")
        
    async def start_worker(self, embedding_engine):
        """Starts the background processing worker."""
        if self.is_processing:
            return
            
        self.is_processing = True
        logger.info("Background embedding worker started.")
        
        while True:
            try:
                job = await self.embedding_queue.get()
                # Simulate processing time
                await asyncio.sleep(0.1) 
                
                # In production: 
                # await embedding_engine.generate_embedding(job["text"])
                
                self.embedding_queue.task_done()
            except Exception as e:
                logger.error(f"Error in background worker: {e}")
                self.failed_jobs.append(job)
                self.embedding_queue.task_done()
