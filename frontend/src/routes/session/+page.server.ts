import { db } from '$lib/database';
import { eq } from 'drizzle-orm';
import type { Actions, PageServerLoad } from './$types';
import { sessionTable } from '$lib/database/schema';
import { error, redirect } from '@sveltejs/kit';
import { generateIdFromEntropySize } from 'lucia';

export const load: PageServerLoad = async () => {
	// TODO: Change this when we have auth and user-sessions
	const userId = 'sample-user';

	return {
		sessions: await db.query.sessionTable.findMany({
			where: eq(sessionTable.owner, userId)
		})
	};
};

export const actions: Actions = {
	default: async ({ request }) => {
		const formData = await request.formData();
		const sessionName = formData.get('sessionName');

		if (typeof sessionName !== 'string') {
			error(400, { message: '`sessionName` is not a string' });
		}

		// TODO: Change this when we have auth and user-sessions
		const userId = 'sample-user';

		const sessionId = generateIdFromEntropySize(10);

		await db.insert(sessionTable).values({
			id: sessionId,
			name: sessionName,
			owner: userId
		});

		redirect(301, `session/${sessionId}`);
	}
};
