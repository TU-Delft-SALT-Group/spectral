import { db } from '$lib/database';
import { filesTable } from '$lib/database/schema';
import { error, json } from '@sveltejs/kit';
import type { RequestHandler } from './$types';
import { eq } from 'drizzle-orm';

async function fetchName(fileId: string): Promise<Response> {
	try {
		const row = await db.query.filesTable.findFirst({
			columns: {
				id: true,
				name: true
			},
			where: eq(filesTable.id, fileId)
		});

		if (row === undefined) {
			throw error(404, `${fileId} not found.`);
		}

		return json(row.name);
	} catch (e) {
		throw error(400, `Failed with error: ${e}.`);
	}
}

async function fetchData(fileId: string): Promise<Response> {
	try {
		const row = await db.query.filesTable.findFirst({
			columns: {
				id: true,
				data: true
			},
			where: eq(filesTable.id, fileId)
		});

		if (row === undefined) {
			error(404, `${fileId} not found.`);
		}

		return new Response(row.data, {
			headers: {
				'Content-Type': 'audio'
			}
		});
	} catch (e) {
		error(400, `Failed with error: ${e}.`);
	}
}

export const GET: RequestHandler = async ({ params, url }) => {
	console.log(url);

	if (url.searchParams.has('name')) {
		return fetchName(params.fileId);
	} else {
		return fetchData(params.fileId);
	}
};
