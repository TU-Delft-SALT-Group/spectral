# Dockerfile for Svelte Frontend
FROM node:20-alpine

# Set the working directory
WORKDIR /frontend

# Copy package.json and pnpm lock
COPY package.json pnpm-lock.yaml ./

RUN corepack enable && corepack prepare pnpm@latest-9 --activate

# Install dependencies
RUN pnpm install

# Expose port 5173 for the service
EXPOSE 5173

CMD pnpm run dev --host
