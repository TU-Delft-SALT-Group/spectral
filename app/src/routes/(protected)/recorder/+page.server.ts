import type { Actions } from './$types';
import { error } from '@sveltejs/kit';
import { unwrap } from '$lib/utils';
import { sessionTable } from '$lib/database/schema';
import { db } from '$lib/database';
import { generateIdFromEntropySize } from 'lucia';
import { uploadFileAsBuffer } from '$lib/database/files';

export const actions: Actions = {
	importAudio: async ({ request, locals }) => {
		const user = locals['user'];
		console.log(user);
		if (!user) {
			error(401, 'Not logged in');
		}

		const formData = await request.formData();

		const sessionName = formData.get('fileName');

		const userId = unwrap(locals.user).id;

		const sessionId = generateIdFromEntropySize(10);

		await db.insert(sessionTable).values({
			id: sessionId,
			name: sessionName,
			owner: userId
		});

		const fileInfo = JSON.parse(formData.get('data'));

		for (const file of fileInfo) {
			const buffer = await formData.get(file['name']).arrayBuffer();
			await uploadFileAsBuffer(
				Buffer.from(buffer),
				file['name'],
				sessionId,
				userId,
				file['groundTruth']
			);
		}
	}
} satisfies Actions;
