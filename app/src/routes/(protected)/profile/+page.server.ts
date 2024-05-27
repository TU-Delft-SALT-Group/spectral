import { lucia } from '$lib/server/auth';
import { fail, redirect } from '@sveltejs/kit';
import type { Actions, PageServerLoad } from './$types';
import { db } from '$lib/database';
import { count, eq } from 'drizzle-orm';
import { fileTable, sessionTable } from '$lib/database/schema';

export const load: PageServerLoad = async ({ parent }) => {
	const { user } = await parent();

	const [{ value: fileCount }] = await db
		.select({ value: count() })
		.from(fileTable)
		.where(eq(fileTable.uploader, user.id));
	const [{ value: sessionCount }] = await db
		.select({ value: count() })
		.from(sessionTable)
		.where(eq(sessionTable.owner, user.id));

	return {
		user,
		fileCount,
		sessionCount
	};
};

export const actions: Actions = {
	logout: async ({ locals, cookies }) => {
		if (!locals.session) {
			return fail(401);
		}

		await lucia.invalidateSession(locals.session.id);
		const sessionCookie = lucia.createBlankSessionCookie();
		cookies.set(sessionCookie.name, sessionCookie.value, {
			path: '.',
			...sessionCookie.attributes
		});

		redirect(302, '/login');
	}
};
