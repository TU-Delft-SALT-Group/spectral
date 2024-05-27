import { db } from '$lib/database';
import { desc, eq } from 'drizzle-orm';
import type { Actions, PageServerLoad } from './$types';
import { sessionTable } from '$lib/database/schema';
import { error, redirect } from '@sveltejs/kit';
import { generateIdFromEntropySize } from 'lucia';
import { unwrap } from '$lib/utils';

export const load: PageServerLoad = async ({ parent }) => {
	const { user } = await parent();

	return {
		sessions: await db.query.sessionTable.findMany({
			where: eq(sessionTable.owner, user.id),
			orderBy: [
				desc(sessionTable.modifiedTime),
				desc(sessionTable.creationTime),
				desc(sessionTable.name)
			]
		})
	};
};

export const actions: Actions = {
	default: async ({ request, locals }) => {
		const formData = await request.formData();
		const sessionName = formData.get('sessionName');

		if (typeof sessionName !== 'string') {
			error(400, { message: '`sessionName` is not a string' });
		}

		if (sessionName.length < 1) {
			error(400, { message: "`sessionName` can't be empty" });
		}

		const userId = unwrap(locals.user).id;

		const sessionId = generateIdFromEntropySize(10);

		await db.insert(sessionTable).values({
			id: sessionId,
			name: sessionName,
			owner: userId
		});

		redirect(301, `session/${sessionId}`);
	}
};
