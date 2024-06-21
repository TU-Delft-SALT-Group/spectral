import { lucia } from '$lib/server/auth';
import { fail, redirect } from '@sveltejs/kit';
import type { Actions, PageServerLoad } from './$types';
import { db } from '$lib/database';
import { count, eq } from 'drizzle-orm';
import { fileTable, sessionTable, userTable } from '$lib/database/schema';
import { formSchema, type FormSchema } from './schema';
import { superValidate } from 'sveltekit-superforms';
import { zod } from 'sveltekit-superforms/adapters';

export const load: PageServerLoad = async ({ parent }) => {
	const { user } = await parent();

	// some random info from the profile
	const [{ value: fileCount }] = await db
		.select({ value: count() })
		.from(fileTable)
		.where(eq(fileTable.uploader, user.id));
	const [{ value: sessionCount }] = await db
		.select({ value: count() })
		.from(sessionTable)
		.where(eq(sessionTable.owner, user.id));
	let apiKeysUnsafe = await db
		.select({ keysJSON: userTable.apiKeys })
		.from(userTable)
		.where(eq(userTable.id, user.id));

	// we don't want to pass the actual api keys to the client: unsafe!!
	// so we strip the keys, so the user gets only a list of already sat up 
	// api keys, like instead of {'deepgram': key1, 'whisper': key2}
	// user get the ['deepgram', 'whisper']
	const apiKeys = Object.keys(apiKeysUnsafe[0]?.keysJSON || {});

	const possibleApis = ["deepgram"];

	const forms = await possibleApis.map((name: string) => { return superValidate(zod(formSchema)); })

	return {
		user,
		fileCount,
		sessionCount,
		apiKeys,
		forms
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
