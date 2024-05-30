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
	let groundTruth = formData.get('groundTruth') as string | null;

	const buffer = await blob.arrayBuffer();

	if (groundTruth === '') {
		groundTruth = null;
	}

	await uploadFileAsBuffer(Buffer.from(buffer), fileName, sessionId, user.id, groundTruth);

	return new Response();
};
