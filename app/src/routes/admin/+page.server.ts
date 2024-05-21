import { db } from '$lib/database';
import { count } from 'drizzle-orm';
import type { Actions, PageServerLoad } from './$types';
import { filesTable, sessionTable, userTable } from '$lib/database/schema';
import { seedSampleUser, seedSampleSession, seedSampleTorgo } from '$lib/database/seeding';

export const load: PageServerLoad = async () => {
	return {
		counts: {
			userTable: await db.select({ value: count() }).from(userTable),
			sessionTable: await db.select({ value: count() }).from(sessionTable),
			filesTable: await db.select({ value: count() }).from(filesTable)
		}
	};
};

export const actions = {
	seedSampleSession,
	seedSampleUser,
	seedSampleTorgo,
	deleteAllData: async () => {
		await db.delete(filesTable);
		await db.delete(sessionTable);
		await db.delete(userTable);
	}
} satisfies Actions;
