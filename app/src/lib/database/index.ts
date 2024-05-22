import { env } from '$env/dynamic/private';
import { drizzle } from 'drizzle-orm/node-postgres';
import pg from 'pg';
import * as schema from './schema';

const pool = new pg.Pool({
	connectionString: env.PG_CONNECTION_STRING
});

export const db = drizzle(pool, { schema });
