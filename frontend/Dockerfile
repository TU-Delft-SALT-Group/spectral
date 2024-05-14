# Dockerfile for Svelte Frontend
FROM node:20-alpine

# Set the working directory
WORKDIR /app

# Copy package.json and package-lock.json
COPY package*.json ./

RUN corepack enable && corepack prepare pnpm@latest-9 --activate

# Install dependencies
RUN pnpm install

# Copy the rest of the frontend code
COPY . .

# Build the application
RUN pnpm build

# Expose port 5173 for the service
EXPOSE 5173

# Serve the application
CMD pnpm dev --host

