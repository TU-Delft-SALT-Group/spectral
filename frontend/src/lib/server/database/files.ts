import { sampleTorgo } from '$lib/files/samples';
import { db } from '.';
import { filesTable, sessionTable, userTable } from './schema';
import { generateIdFromEntropySize } from 'lucia';
import { readFile } from 'node:fs/promises';

export async function uploadFile(file: File, sessionId: string) {
	const arrayBuffer = await file.arrayBuffer();
	const buffer = Buffer.from(arrayBuffer);

	await db.insert(filesTable).values({
		name: file.name,
		id: generateIdFromEntropySize(10),
		data: buffer,
		session: sessionId
	});
}

export async function seedSampleTorgo() {
	console.log('Seeding sample torgo');

	await db.insert(userTable).values({
		id: 'sample-user',
		email: '',
		hashedPassword: '',
		username: 'Sample User'
	});

	await db.insert(sessionTable).values({
		id: 'sample-torgo',
		name: 'Sample Torgo',
		owner: 'sample-user'
	});

	for (const filename of sampleTorgo) {
		const buffer = await readFile(`./static/samples/torgo-dataset/${filename}.wav`);

		await db.insert(filesTable).values({
			id: filename,
			name: filename,
			session: 'sample-torgo',
			data: buffer
		});
	}

	console.log('Finished');
}
