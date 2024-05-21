import { uploadFileAsBuffer } from '$lib/database/files';
import type { RequestHandler } from './$types';

export const POST: RequestHandler = async ({ request, params: { sessionId, fileName } }) => {
	const blob = await request.blob();
	const buffer = await blob.arrayBuffer();

	await uploadFileAsBuffer(Buffer.from(buffer), fileName, sessionId);

	return new Response();
};
