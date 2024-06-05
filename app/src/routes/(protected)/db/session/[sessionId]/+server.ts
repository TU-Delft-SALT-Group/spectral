import { db } from '$lib/database';
import { sessionTable } from '$lib/database/schema';
import { error, type RequestHandler } from '@sveltejs/kit';
import { sessionState } from '../../../session/[sessionId]/workspace';
import { eq } from 'drizzle-orm';
import { logger } from '$lib/logger';
import { deepEqual } from '$lib/utils';

export const POST: RequestHandler = async ({ params, request }) => {
	const json = await request.json();
	const state = sessionState.parse(json);
	if (params.sessionId === undefined) throw error(400, `Failed to be given a session ID.`);

	const id: string = params.sessionId;

	const previousState = await db.query.sessionTable.findFirst({
		where: eq(sessionTable.id, id),
		columns: {
			state: true
		}
	});

	if (deepEqual(state, previousState?.state)) {
		logger.trace('Not updating state since it has not been modified.');
		return new Response();
	}

	try {
		await db
			.update(sessionTable)
			.set({
				state,
				modifiedTime: new Date()
			})
			.where(eq(sessionTable.id, id));
	} catch (e) {
		logger.trace(`Failed to make POST request, error: ${e}.`);
		throw error(400, `Failed with error message: ${e}.`);
	}

	return new Response();
};
