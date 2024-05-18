# Dockerfile for Svelte Frontend
FROM node:20-alpine

# Set the working directory
WORKDIR /frontend

RUN corepack enable

# Copy package.json and pnpm lock
COPY package.json pnpm-lock.yaml ./
 
RUN pnpm fetch 

# Install dependencies
RUN pnpm install -r --offline

# Expose port 5173 for the service
EXPOSE 5173

CMD pnpm run dev --host
