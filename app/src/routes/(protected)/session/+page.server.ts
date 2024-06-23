import { db } from '$lib/database';
import { desc, eq } from 'drizzle-orm';
import type { Actions, PageServerLoad } from './$types';
import { sessionTable, fileTable } from '$lib/database/schema';
import { error, redirect } from '@sveltejs/kit';
import { generateIdFromEntropySize } from 'lucia';
import { unwrap } from '$lib/utils';

export const ssr = false;

export const load: PageServerLoad = async ({ parent }) => {
	const { user } = await parent();

	return {
		sessions: await db.query.sessionTable.findMany({
			where: eq(sessionTable.owner, user.id),
			orderBy: [
				desc(sessionTable.modifiedTime),
				desc(sessionTable.creationTime),
				desc(sessionTable.name)
			]
		})
	};
};

export const actions: Actions = {
	exportSession: async ({ request }) => {
		const sessionId = await request.json();
		const session = await db.query.sessionTable.findFirst({
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
						state: true,
						groundTruth: true,
						data: true
					}
				}
			}
		});
		if (session) {
			return JSON.stringify(session);
		}
		// if something went wrong,
		throw new Error('Bad request');
	},
	importSession: async ({ request, locals }) => {
		const sessionJSON = await request.json();

		const userId = unwrap(locals.user).id;

		// create new 'blank' session with new id and correct name
		const sessionId = await createSession(userId, sessionJSON.name);
		try {
			const newIdDict = [];

			// loop to store the files again
			for (const file of sessionJSON.files) {
				const data = Buffer.from(file.data.data);
				const fileId = generateIdFromEntropySize(10);
				newIdDict.push({ oldId: file.id, newId: fileId });
				await db.insert(fileTable).values({
					...file,
					id: fileId,
					uploader: userId,
					session: sessionId,
					data
				});
			}

			// loop to update the old file id's to the new ones in the panes
			for (const key in sessionJSON.state.panes) {
				for (const file in sessionJSON.state.panes[key].files) {
					sessionJSON.state.panes[key].files[file].id = newIdDict.filter(
						(x) => x.oldId == sessionJSON.state.panes[key].files[file].id
					)[0].newId;
				}
			}

			// loop to update the old file id's to the new ones in the panels
			for (const key in sessionJSON.state.panels) {
				for (const file in sessionJSON.state.panels[key].params.files) {
					sessionJSON.state.panels[key].params.files[file].id = newIdDict.filter(
						(x) => x.oldId == sessionJSON.state.panes[key].files[file].id
					)[0].newId;
				}
			}

			sessionJSON.id = sessionId;
			const state = sessionJSON;

			// update database with new state
			await db.update(sessionTable).set(state).where(eq(sessionTable.id, sessionId));
		} catch {
			// in case of error delete created session from database
			await db.delete(sessionTable).where(eq(sessionTable.id, sessionId));
			throw new Error('Something went wrong will importing');
		}
		redirect(301, `session/${sessionId}`);
	},
	deleteSession: async ({ request }) => {
		const sessionId = await request.json();
		await db.delete(sessionTable).where(eq(sessionTable.id, sessionId));
	},
	createSession: async ({ request, locals }) => {
		const formData = await request.formData();
		const sessionName = formData.get('sessionName');

		if (typeof sessionName !== 'string') {
			error(400, { message: '`sessionName` is not a string' });
		}

		const userId = unwrap(locals.user).id;

		if (sessionName.length < 1) {
			error(400, { message: "`sessionName` can't be empty" });
		}

		const sessionId = await createSession(userId, sessionName);

		redirect(301, `session/${sessionId}`);
	}
};

async function createSession(userId: string, sessionName: string) {
	const sessionId = generateIdFromEntropySize(10);

	await db.insert(sessionTable).values({
		id: sessionId,
		name: sessionName,
		owner: userId
	});

	return sessionId;
}
