import type { PageServerLoad, Actions } from './$types';
import { sessionState, type SessionState } from './workspace';
import { db } from '$lib/database';
import { fileTable, sessionTable } from '$lib/database/schema';
import { eq } from 'drizzle-orm';
import { error, fail } from '@sveltejs/kit';
import { uploadFile } from '$lib/database/files';
import { fileState, type FileState } from '$lib/analysis/modes/file-state';

export const load = (async ({ params: { sessionId } }) => {
	const result = await db.query.sessionTable.findFirst({
		where: eq(sessionTable.id, sessionId),
		columns: {
			state: true
		},
		with: {
			files: {
				columns: {
					id: true,
					name: true,
					state: true
				}
			}
		}
	});

	if (result === undefined) {
		error(404, 'Session not found');
	}

	const [files, state] = await Promise.all([getFiles(result), getState(result)]);

	return {
		files,
		state,
		sessionId
	};
}) satisfies PageServerLoad;

async function getFiles(result: {
	files: { id: string; name: string; state: unknown }[];
}): Promise<FileState[]> {
	const promises = result.files.map(async (file) => {
		try {
			if (typeof file.state !== 'object') {
				throw new Error('Invalid file state');
			}

			return fileState.parse({
				...file.state,
				id: file.id,
				name: file.name
			});
		} catch (err) {
			const defaultState = fileState.parse(undefined);

			return {
				...defaultState,
				id: file.id,
				name: file.name
			};
		}
	});

	return await Promise.all(promises);
}

async function getState(result: { state: unknown }): Promise<SessionState> {
	if (!result) {
		error(404, 'Session not found');
	}

	try {
		return sessionState.parse(result.state);
	} catch (e) {
		console.warn('Found invalid state in database, resetting to default');
		const defaultState = sessionState.parse(undefined);

		await db.update(sessionTable).set({
			state: defaultState
		});

		return defaultState;
	}
}

export const actions = {
	uploadFile: async ({ request, params: { sessionId }, locals }) => {
		const { user } = locals;
		if (!user) {
			error(401, 'Not logged in');
		}

		const formData = await request.formData();

		const file = formData.get('file');
		if (!(file instanceof File)) {
			return fail(400, { message: 'No file provided' });
		}

		await uploadFile(file, sessionId, user.id);
	},

	deleteFile: async ({ request }) => {
		const json = await request.json();
		if (!('fileId' in json) || typeof json.fileId !== 'string') {
			return fail(400, { message: 'Invalid fileId' });
		}

		await db.delete(fileTable).where(eq(fileTable.id, json.fileId));
	}
} satisfies Actions;
