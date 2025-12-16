import { NestFactory } from '@nestjs/core';
import { AppModule } from './app.module';
import Redis from 'ioredis'; 

async function bootstrap() {
  const app = await NestFactory.create(AppModule);

const redisSubscriber = new Redis({ 
    host: process.env.REDIS_HOST || 'localhost', 
    port: 6379 
  });  
  redisSubscriber.subscribe('job_result', (err) => {
    if (err) console.error('Failed to subscribe: %s', err.message);
  });

  redisSubscriber.on('message', (channel, message) => {
    console.log(`🔔 NestJS Notification: Received result from Python!`);
    console.log(`Packet: ${message}`);
  });

  await app.listen(3000);
}
bootstrap();