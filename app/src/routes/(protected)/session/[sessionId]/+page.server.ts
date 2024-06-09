import type { PageServerLoad, Actions } from './$types';
import { sessionState, type SessionState } from './workspace';
import { db } from '$lib/database';
import { fileTable, sessionTable } from '$lib/database/schema';
import { eq } from 'drizzle-orm';
import { error, fail } from '@sveltejs/kit';
import { uploadFile } from '$lib/database/files';
import { fileState, type FileState } from '$lib/analysis/modes/file-state';
import { logger } from '$lib/logger';

export const load = (async ({ params: { sessionId } }) => {
	const result = await db.query.sessionTable.findFirst({
		where: eq(sessionTable.id, sessionId),
		columns: {
			state: true,
			name: true
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
		logger.trace(`Session ${sessionId} not found`);
		error(404, 'Session not found');
	}

	const [files, state] = await Promise.all([getFiles(result), getState(result)]);
	const name = result.name;

	return {
		files,
		state,
		sessionId,
		name
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

			logger.trace(`File ${file.id} found`);
			return fileState.parse({
				...file.state,
				id: file.id,
				name: file.name
			});
		} catch (err) {
			logger.trace(`File ${file.id} not found`);
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
		const check = sessionState.parse(result.state);
		return check;
	} catch (e) {
		logger.warn('Found invalid state in database, resetting to default');
		const defaultState = sessionState.parse(undefined);

		await db.update(sessionTable).set({
			state: defaultState
		});

		return defaultState;
	}
}

export const actions = {
	renameFile: async ({ request }) => {
		const json = await request.json();
		if (
			!('fileId' in json || 'name' in json) ||
			typeof json.fileId !== 'string' ||
			typeof json.name !== 'string'
		) {
			logger.trace('File to be renamed has invalid fileId/no name');
			return fail(400, { message: 'Invalid fileId/name' });
		}

		await db.update(fileTable).set(json).where(eq(fileTable.id, json.fileId));
		logger.trace(`File ${json.fileId} successfully renamed to ${json.name}`);
	},
	uploadFile: async ({ request, params: { sessionId }, locals }) => {
		const { user } = locals;
		if (!user) {
			error(401, 'Not logged in');
		}

		const formData = await request.formData();

		const file = formData.get('file');
		if (!(file instanceof File)) {
			logger.trace('No proper file was provided');
			return fail(400, { message: 'No file provided' });
		}

		await uploadFile(file, sessionId, user.id);
		logger.trace(`File ${file.name} successfully uploaded`);
	},

	deleteFile: async ({ request }) => {
		const json = await request.json();
		if (!('fileId' in json) || typeof json.fileId !== 'string') {
			logger.trace('File to be deleted has invalid fileId');
			return fail(400, { message: 'Invalid fileId' });
		}

		await db.delete(fileTable).where(eq(fileTable.id, json.fileId));
		logger.trace(`File ${json.fileId} successfully deleted`);
	}
} satisfies Actions;
