import type { Config } from 'drizzle-kit';

export default {
	dialect: 'postgresql',
	schema: './src/lib/database/schema.ts',
	dbCredentials: {
		url: process.env.PG_CONNECTION_STRING ?? ''
	},
	out: './drizzle'
} satisfies Config;
