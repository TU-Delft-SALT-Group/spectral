import { uploadFileAsBuffer } from '$lib/database/files';
import { error } from '@sveltejs/kit';
import type { RequestHandler } from './$types';

export const POST: RequestHandler = async ({
	request,
	params: { sessionId, fileName },
	locals
}) => {
	const { user } = locals;
	if (user === null) {
		error(401, 'Unauthorized');
	}

	const formData = await request.formData();
	const blob = formData.get('recording') as Blob;
	const groundTruth = formData.get('groundTruth') as string;

	const buffer = await blob.arrayBuffer();

	await uploadFileAsBuffer(Buffer.from(buffer), fileName, sessionId, user.id, groundTruth, '');

	return new Response();
};
