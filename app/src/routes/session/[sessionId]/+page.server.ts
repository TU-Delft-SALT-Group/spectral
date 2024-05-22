import type { PageServerLoad, Actions } from './$types';
import type { FilebrowserFile } from '$lib/files';
import { workspaceState, type WorkspaceState } from './workspace';
import { db } from '$lib/database';
import { filesTable, sessionTable } from '$lib/database/schema';
import { eq } from 'drizzle-orm';
import { error, fail } from '@sveltejs/kit';
import { uploadFile } from '$lib/database/files';

async function getFiles(sessionId: string): Promise<FilebrowserFile[]> {
	const result = await db.query.filesTable.findMany({
		where: eq(filesTable.session, sessionId)
	});

	return result.map((row) => ({
		id: row.id,
		name: row.name,
		type: 'file'
	}));
}

async function getState(sessionId: string): Promise<WorkspaceState> {
	const result = await db.query.sessionTable.findFirst({
		where: eq(sessionTable.id, sessionId),
		columns: {
			state: true
		}
	});

	if (!result) {
		error(404, 'Session not found');
	}

	try {
		return workspaceState.parse(result.state);
	} catch (e) {
		console.warn('Found invalid state in database, resetting to default');
		console.log('State found: ', result.state);
		const defaultState = workspaceState.parse(undefined);

		await db.update(sessionTable).set({
			state: defaultState
		});

		return defaultState;
	}
}

export const load = (async ({ params: { sessionId } }) => {
	const [files, state] = await Promise.all([getFiles(sessionId), getState(sessionId)]);

	return {
		files,
		state,
		sessionId
	};
}) satisfies PageServerLoad;

export const actions = {
	uploadFile: async ({ request, params: { sessionId } }) => {
		const formData = await request.formData();

		const file = formData.get('file');
		if (!(file instanceof File)) {
			return fail(400, { message: 'No file provided' });
		}

		await uploadFile(file, sessionId);
	},

	deleteFile: async ({ request }) => {
		const json = await request.json();
		if (!('fileId' in json) || typeof json.fileId !== 'string') {
			return fail(400, { message: 'Invalid fileId' });
		}

		await db.delete(filesTable).where(eq(filesTable.id, json.fileId));
	}
} satisfies Actions;
