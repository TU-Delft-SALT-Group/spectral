# Dockerfile for Svelte app
FROM node:20-alpine

# Set the working directory
WORKDIR /app

RUN corepack enable

# Copy package.json and pnpm lock
COPY package.json pnpm-lock.yaml ./

RUN pnpm fetch

# Install dependencies
RUN pnpm install -r --offline --frozen-lockfile

# Expose port 5173 for the service
EXPOSE 5173

CMD (sleep 3; pnpm db:push) & pnpm run dev --host | pnpm exec pino-pretty
