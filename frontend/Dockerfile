# Dockerfile for Svelte Frontend
FROM node:20-alpine

# Set the working directory
WORKDIR /frontend

# Copy package.json and package-lock.json
COPY package*.json ./

RUN corepack enable && corepack prepare pnpm@latest-9 --activate

# Install dependencies
CMD pnpm install

# Expose port 5173 for the service
EXPOSE 5173

# Build the application
CMD pnpm build

# Serve the application
CMD pnpm dev --host

