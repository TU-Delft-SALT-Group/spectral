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
		if (!user) {
			error(401, 'Not logged in');
		}

		const formData = await request.formData();
		const sessionName = formData.get('sessionName');
		const userId = unwrap(locals.user).id;
		const sessionId = generateIdFromEntropySize(10);

		if (typeof sessionName !== 'string') {
			error(400, { message: '`sessionName` is not a string' });
		}

		if (sessionName.length < 1) {
			error(400, { message: "`sessionName` can't be empty" });
		}

		await db.insert(sessionTable).values({
			id: sessionId,
			name: sessionName,
			owner: userId
		});

		// TODO: check out if this ! assertion is valid or not
		const fileInfo = JSON.parse(formData.get('data')!.toString()!);

		for (const file of fileInfo) {
			const data = formData.get(file['name']);

			if (data === null) {
				continue;
			}

			const buffer = await (data as File).arrayBuffer();
			await uploadFileAsBuffer(
				Buffer.from(buffer),
				file['name'],
				sessionId,
				userId,
				file['groundTruth']
			);
		}

		return sessionId;
	}
} satisfies Actions;
