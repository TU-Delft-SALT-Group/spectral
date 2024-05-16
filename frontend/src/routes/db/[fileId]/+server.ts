import { db } from '$lib/server/database';
import { filesTable } from '$lib/server/database/schema';
import { error } from '@sveltejs/kit';
import type { RequestHandler } from './$types';
import { eq } from 'drizzle-orm';

export const GET: RequestHandler = async ({ params }) => {
	try {
		const row = await db.query.filesTable.findFirst({
			columns: {
				id: true,
				data: true
			},
			where: eq(filesTable.id, params.fileId)
		});

		if (row === undefined) {
			error(404, `${params.fileId} not found.`);
		}

		return new Response(row.data, {
			headers: {
				'Content-Type': 'audio/wav'
			}
		});
	} catch (e) {
		error(400, {
			message: `Failed with error: ${e}`
		});
	}
};
