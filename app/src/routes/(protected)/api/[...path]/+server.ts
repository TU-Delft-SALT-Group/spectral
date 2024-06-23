import { error } from '@sveltejs/kit';
import type { RequestHandler } from './$types';
import { db } from '$lib/database';
import { and, eq } from 'drizzle-orm';
import { fileTable } from '$lib/database/schema';

function getUrlFromPath(path: string) {
	return new URL(path, PUBLIC_KERNEL_ORIGIN);
}

function verifyFileOwnership(fileId: string, userId: string) {
	const file = db.query.fileTable.findFirst({
		where: and(eq(fileTable.id, fileId), eq(fileTable.uploader, userId)),
		columns: { id: true }
	});

	if (!file) {
		error(404, `File not found (id: ${fileId})`);
	}
}

function getFileId(request: Request) {
	const fileId = request.headers.get('file-id');
	if (!fileId) {
		error(400, 'No file-id header');
	}

	return fileId;
}

const handleRequest: RequestHandler = async ({
	fetch,
	request,
	params: { path },
	locals: { user }
}) => {
	if (!user) {
		error(401, 'Not logged in');
	}

	const fileId = getFileId(request);
	verifyFileOwnership(fileId, user.id);

	const url = getUrlFromPath(path);
	// undici doesn't support the connection header
	request.headers.delete('connection');

	// Forward the request as-is to the kernel
	return await fetch(new Request(url, request));
};

export const GET = handleRequest;
export const POST = handleRequest;
