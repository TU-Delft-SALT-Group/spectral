import type { Config } from 'drizzle-kit';

export default {
	driver: 'pg',
	schema: './src/lib/server/database/schema.ts',
	dbCredentials: {
		connectionString: process.env.PG_CONNECTION_STRING ?? ""
	},
	out: './drizzle'
} satisfies Config;
