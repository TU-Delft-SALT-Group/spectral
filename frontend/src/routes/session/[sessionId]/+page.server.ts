import type { PageServerLoad, Actions } from './$types';
import { sampleTorgo } from '$lib/files/samples';
import type { FilebrowserFile } from '$lib/files';
import type { WorkspaceState } from './workspace';
import { db } from '$lib/server/database';
import { filesTable } from '$lib/server/database/schema';
import { eq } from 'drizzle-orm';
import { fail } from '@sveltejs/kit';
import { uploadFile } from '$lib/server/database/files';

const sampleState: WorkspaceState = {

	panes: [
		{
			mode: 'waveform',
			files: sampleTorgo.slice(0, 3).map((id) => ({
				id,
				name: id,
				frame: null
			}))
		}
	]
}

async function getFilesAndState(sessionId: string): Promise<{
	files: FilebrowserFile[],
	state: WorkspaceState,
}> {
	const result = await db.query.filesTable.findMany({
		where: eq(filesTable.session, sessionId)
	});

	const files: FilebrowserFile[] = result.map((row) => ({
		id: row.id,
		name: row.name,
		type: 'file'
	}));

	// TODO: Get workspace state from database
	return { files, state: sampleState };
}

export const load = (async ({
	params: { sessionId }
}) => {
	const { files, state } = await getFilesAndState(sessionId);

	return {
		files,
		state,
	}
}) satisfies PageServerLoad;


export const actions = {
	default: async ({ request, params: { sessionId } }) => {
		const formData = await request.formData();

		const file = formData.get('file');
		if (!(file instanceof File)) {
			return fail(400, { message: 'No file provided' })
		}

		uploadFile(file, sessionId);
	},
} satisfies Actions;
