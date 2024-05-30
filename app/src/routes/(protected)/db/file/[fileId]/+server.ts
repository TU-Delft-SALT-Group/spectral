import { db } from '$lib/database';
import { fileTable } from '$lib/database/schema';
import { error, json } from '@sveltejs/kit';
import type { RequestHandler } from './$types';
import { and, eq } from 'drizzle-orm';
import { logger } from '$lib/logger';

async function fetchName(fileId: string, userId: string): Promise<Response> {
	try {
		const row = await db.query.fileTable.findFirst({
			columns: {
				id: true,
				name: true
			},
			where: and(eq(fileTable.id, fileId), eq(fileTable.uploader, userId))
		});

		if (row === undefined) {
			throw error(404, `${fileId} not found.`);
		}

		logger.trace(`File ${fileId} found`);
		return json(row.name);
	} catch (e) {
		logger.trace(`File ${fileId} not found`);
		throw error(400, `Failed with error: ${e}.`);
	}
}

async function fetchData(fileId: string, userId: string): Promise<Response> {
	try {
		const row = await db.query.fileTable.findFirst({
			columns: {
				id: true,
				data: true
			},
			where: and(eq(fileTable.id, fileId), eq(fileTable.uploader, userId))
		});

		if (row === undefined) {
			error(404, `${fileId} not found.`);
		}

		logger.trace(`File ${fileId} found`);
		return new Response(row.data, {
			headers: {
				'Content-Type': 'audio'
			}
		});
	} catch (e) {
		logger.trace(`File ${fileId} not found`);
		error(400, `Failed with error: ${e}.`);
	}
}

export const GET: RequestHandler = async ({ params: { fileId }, url, locals }) => {
	const { user } = locals;

	if (user === null) {
		error(404, `${fileId} not found.`);
	}

	if (url.searchParams.has('name')) {
		return fetchName(fileId, user.id);
	} else {
		return fetchData(fileId, user.id);
	}
};
