# Use a Node.js base image
FROM node:20-alpine

# Set the working directory
WORKDIR /app

# Copy package files
COPY package*.json ./

# Install dependencies (pnpm is modern, let's use it)
RUN npm install -g pnpm && pnpm install

# Copy source code
COPY . .

# Build the NestJS app
RUN pnpm run build

# Command to run the built application
CMD ["node", "dist/main"]