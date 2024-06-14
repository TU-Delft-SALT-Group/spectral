import { db } from '$lib/database';
import { desc, eq } from 'drizzle-orm';
import type { Actions, PageServerLoad } from './$types';
import { sessionTable, fileTable } from '$lib/database/schema';
import { error, redirect } from '@sveltejs/kit';
import { generateIdFromEntropySize } from 'lucia';
import { unwrap } from '$lib/utils';

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
			const sessionWithBlobs = {
				name: session.name,
				status: session.state,
				files: session.files.map((file) => ({
					id: file.id,
					name: file.name,
					state: file.state,
					groundTruth: file.groundTruth,
					data: file.data.toString('base64')
				}))
			};

			console.log(JSON.stringify(sessionWithBlobs));

			return JSON.stringify(sessionWithBlobs);
		}
		return null;
	},
	importSession: async ({ request, locals }) => {
		const sessionJSON = await JSON.parse(await request.json());
		// console.log(JSON.stringify(sessionJSON))

		const userId = unwrap(locals.user).id;

		const sessionId = await createSession(userId, sessionJSON.name);

		const newIdDict = [];

		for (const file of sessionJSON.files) {
			const fileId = generateIdFromEntropySize(10);
			newIdDict.push({ oldId: file.id, newId: fileId });
			db.insert(fileTable).values({
				...file,
				id: fileId
			});
		}

		for (const key in sessionJSON.status.panes) {
			for (const file in sessionJSON.status.panes[key].files) {
				sessionJSON.status.panes[key].files[file].id = newIdDict.filter(
					(x) => x.oldId == sessionJSON.status.panes[key].files[file].id
				)[0].newId;
			}
		}

		for (const key in sessionJSON.status.panels) {
			for (const file in sessionJSON.status.panels[key].params.files) {
				sessionJSON.status.panels[key].params.files[file].id = newIdDict.filter(
					(x) => x.oldId == sessionJSON.status.panes[key].files[file].id
				)[0].newId;
			}
		}

		console.log(sessionJSON);

		await db.update(sessionTable).set(sessionJSON).where(eq(sessionTable.id, sessionId));
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
