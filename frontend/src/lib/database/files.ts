import { db } from '.';
import { filesTable } from './schema';
import { generateIdFromEntropySize } from 'lucia';

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