import { db } from '.';
import { filesTable } from './schema';
import { generateIdFromEntropySize } from 'lucia';

export async function uploadFile(file: File, sessionId: string) {
	const arrayBuffer = await file.arrayBuffer();
	const buffer = Buffer.from(arrayBuffer);

	await uploadFileAsBuffer(buffer, file.name, sessionId, null);
}

export async function uploadFileAsBuffer(buffer: Buffer, name: string, sessionId: string, groundTruth: string | null) {
	await db.insert(filesTable).values({
		name,
		id: generateIdFromEntropySize(10),
		data: buffer,
		session: sessionId,
		groundTruth: groundTruth,
	});
}
