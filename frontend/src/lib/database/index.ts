import { drizzle } from 'drizzle-orm/postgres-js';
import pg from 'pg';

const pool = new pg.Pool();
export const db = drizzle(pool);
