import { db } from '$lib/database';
import { sessionTable } from '$lib/database/schema';
import { error, type RequestHandler } from '@sveltejs/kit';
import { sessionState, type SessionState } from '../../../session/[sessionId]/workspace';
import { eq } from 'drizzle-orm';

export const POST: RequestHandler = async ({ params, request }) => {
	const json = await request.json();
	const val: SessionState = sessionState.parse(json);
	if (params.sessionId === undefined) throw error(400, `Failed to be given a session ID.`);

	const id: string = params.sessionId;

	try {
		await db
			.update(sessionTable)
			.set({
				state: val
			})
			.where(eq(sessionTable.id, id));
	} catch (e) {
		throw error(400, `Failed with error message: ${e}.`);
	}

	return new Response();
};
