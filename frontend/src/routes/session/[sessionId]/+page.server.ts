import type { PageServerLoad } from './$types';
import { sampleTorgo } from '$lib/files/samples';
import type { FilebrowserFile } from '$lib/files';
import type { WorkspaceState } from './workspace';
import { todo } from '$lib/utils';

export const load = (async ({
	params: { sessionId }
}): Promise<{ files: FilebrowserFile[]; state: WorkspaceState }> => {
	if (sessionId === 'sample-torgo') {
		return {
			files: sampleTorgo.map((id) => ({
				id,
				name: id,
				type: 'file'
			})),

			state: {
				panes: [
					{
						mode: 'simple-info',
						files: sampleTorgo.slice(0, 3).map((id) => ({
							id,
							name: id,
							frame: null
						}))
					}
				]
			}
		};
	}

	// TODO: Get files from session from database
	return { files: [], state: todo() };
}) satisfies PageServerLoad;
