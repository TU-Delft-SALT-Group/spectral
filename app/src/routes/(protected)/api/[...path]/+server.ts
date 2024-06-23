import { PUBLIC_KERNEL_ORIGIN } from '$env/static/public';
import { error } from '@sveltejs/kit';
import type { RequestHandler } from './$types';
import { z } from 'zod';
import { db } from '$lib/database';
import { and, eq } from 'drizzle-orm';
import { fileTable } from '$lib/database/schema';

export const POST: RequestHandler = async ({ request, params: { path }, locals: { user } }) => {
	if (!user) {
		error(401, 'Not logged in');
	}

	const json = (await request.json()) as unknown;

	const jsonShape = z.object({
		fileState: z.object({
			id: z.string()
		})
	});

	const result = jsonShape.safeParse(json);

	if (!result.success) {
		error(400, 'Invalid JSON or no fileState.id');
	}

	const {
		fileState: { id }
	} = result.data;

	const dbFile = await db.query.fileTable.findFirst({
		where: and(eq(fileTable.id, id), eq(fileTable.uploader, user.id)),
		columns: { id: true }
	});

	if (!dbFile) {
		error(404, `File not found (id: ${id})`);
	}

	const url = new URL(path, PUBLIC_KERNEL_ORIGIN);
	return await fetch(url, {
		method: 'POST',
		headers: {
			'Content-Type': 'application/json'
		},
		body: JSON.stringify(json)
	});
};
