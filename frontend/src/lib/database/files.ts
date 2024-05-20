import { db } from '.';
import { filesTable } from './schema';
import { generateIdFromEntropySize } from 'lucia';

export async function uploadFile(file: File, sessionId: string) {
	const arrayBuffer = await file.arrayBuffer();
	const buffer = Buffer.from(arrayBuffer);

	await uploadFileAsBuffer(buffer, file.name, sessionId);
}

export async function uploadFileAsBuffer(buffer: Buffer, name: string, sessionId: string) {
	await db.insert(filesTable).values({
		name,
		id: generateIdFromEntropySize(10),
		data: buffer,
		session: sessionId
	});
}
