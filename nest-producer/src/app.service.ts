import { Injectable } from '@nestjs/common';
import Redis from 'ioredis';

@Injectable()
export class AppService {
 private readonly redis = new Redis({ 
    host: process.env.REDIS_HOST || 'localhost', 
    port: 6379 
  });
  async addJob(data: any) {
    // LPUSH adds a task to the head of the list
    // We stringify the data to send it as a JSON string
    await this.redis.lpush('job_queue', JSON.stringify(data));
    return { status: 'queued', data };
  }
}