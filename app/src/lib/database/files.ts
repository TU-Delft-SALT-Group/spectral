import { db } from '.';
import { fileTable } from './schema';
import { generateIdFromEntropySize } from 'lucia';
import { logger } from '$lib/logger';

export async function uploadFile(file: File, sessionId: string, userId: string) {
	const arrayBuffer = await file.arrayBuffer();
	const buffer = Buffer.from(arrayBuffer);

	await uploadFileAsBuffer(buffer, file.name, sessionId, userId, '', '');
	logger.trace(`File ${file.name} uploaded as buffer`);
}

export async function uploadFileAsBuffer(
	buffer: Buffer,
	name: string,
	sessionId: string,
	userId: string,
	groundTruth: string,
	note: string
) {
	await db.insert(fileTable).values({
		name,
		id: generateIdFromEntropySize(10),
		uploader: userId,
		data: buffer,
		session: sessionId,
		groundTruth,
		note
	});
}
