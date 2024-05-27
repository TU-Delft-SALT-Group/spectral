# Dockerfile for Svelte app
FROM node:20-alpine

# Set the working directory
WORKDIR /app

RUN corepack enable

# Copy package.json and pnpm lock
COPY package.json pnpm-lock.yaml ./

RUN pnpm fetch

# Install dependencies
RUN pnpm install -r --offline

# Expose port 5173 for the service
EXPOSE 5173

RUN pnpm install -r --offline --frozen-lockfile

CMD pnpm run dev --host | pnpm exec pino-pretty
