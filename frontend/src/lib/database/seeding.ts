import { sampleTorgo } from '$lib/files/samples';
import { readFile } from 'node:fs/promises';
import { db } from '.';
import { filesTable, sessionTable, userTable } from './schema';
import { eq } from 'drizzle-orm';

export async function seedSampleUser() {
	const isSampleUserSeeded = await db.query.userTable.findFirst({
		where: eq(userTable.id, 'sample-user')
	});

	if (!isSampleUserSeeded) {
		await db.insert(userTable).values({
			id: 'sample-user',
			email: '',
			hashedPassword: '',
			username: 'Sample User'
		});
	}

	return { isSampleUserSeeded };
}

export async function seedSampleSession() {
	const { isSampleUserSeeded } = await seedSampleUser();

	const isSampleSessionSeeded = await db.query.sessionTable.findFirst({
		where: eq(sessionTable.id, 'sample-session')
	});

	if (!isSampleSessionSeeded) {
		await db.insert(sessionTable).values({
			id: 'sample-session',
			name: 'Sample Session',
			owner: 'sample-user'
		});
	}

	return { isSampleUserSeeded, isSampleSessionSeeded };
}

export async function seedSampleTorgo() {
	const { isSampleUserSeeded, isSampleSessionSeeded } = await seedSampleSession();

	for (const filename of sampleTorgo) {
		const isFileSeeded = await db.query.filesTable.findFirst({
			where: eq(filesTable.id, filename)
		});

		if (isFileSeeded) {
			continue;
		}

		const buffer = await readFile(`./static/samples/torgo-dataset/${filename}.wav`);

		await db.insert(filesTable).values({
			id: filename,
			name: filename,
			session: 'sample-session',
			data: buffer
		});
	}

	return { isSampleUserSeeded, isSampleSessionSeeded, isSampleTorgoSeeded: true };
}
