import { db } from '$lib/database';
import { sessionTable } from '$lib/database/schema';
import { error, type RequestHandler } from '@sveltejs/kit';
import { workspaceState, type WorkspaceState } from '../../../session/[sessionId]/workspace';

export const POST: RequestHandler = async ({ params, request }) => {
	const json = await request.json();
	const val: WorkspaceState = workspaceState.parse(json);

	try {
		await db.update(sessionTable).set({
			id: params.sessionId,
			...val
		});
	} catch (e) {
		throw error(400, `Failed with error message: ${e}.`);
	}

	return new Response();
};
