import { lucia } from '$lib/server/auth';
import { fail, redirect } from '@sveltejs/kit';
import type { Actions, PageServerLoad } from './$types';
import { db } from '$lib/database';
import { count, eq } from 'drizzle-orm';
import { fileTable, sessionTable, userTable } from '$lib/database/schema';
import { formSchema, deleteFormSchema } from './schema';
import { setError, superValidate } from 'sveltekit-superforms';
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
	let [{ key: apiKeysUnsafe }] = await db
		.select({ key: userTable.apiKeys })
		.from(userTable)
		.where(eq(userTable.id, user.id));

	// we don't want to pass the actual api keys to the client: unsafe!!
	// so we strip the keys, so the user gets only a list of already sat up 
	// api keys, like instead of {'deepgram': key1, 'whisper': key2}
	// user get the ['deepgram', 'whisper']
	const keyData = apiKeysUnsafe.map(({ key, ...rest }) => (rest));

	return {
		user,
		fileCount,
		sessionCount,
		keyData,
		form: await superValidate(zod(formSchema))
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
	},

	addkey: async (event) => {
		const form = await superValidate(event, zod(formSchema));
		if (event.locals.user !== null) {
			// get the keys
			let oldKeys = event.locals.user.apiKeys || [];
			let newKeys = [...oldKeys, form.data];

			// check there is no other key for the same model
			if (oldKeys.some((el) => (el.model === form.data.model))) {
				setError(form, "model", "Key for this model already exists.");
				return fail(400, { form });
			}

			// check there is no old key with the same name
			if (oldKeys.some((el) => (el.name === form.data.name))) {
				setError(form, "name", "Key with such name already exists, choose another name");
				return fail(400, { form });
			}

			await db.update(userTable)
				.set({ apiKeys: newKeys })
				.where(eq(userTable.id, event.locals.user.id));
		}
	},

	deletekey: async (event) => {
		const form = await superValidate(event, zod(deleteFormSchema));
		if (event.locals.user !== null) {
			let oldKeys = event.locals.user.apiKeys || [];
			let newKeys = oldKeys.filter((el) => (el.name !== form.data.name))

			await db.update(userTable)
				.set({ apiKeys: newKeys })
				.where(eq(userTable.id, event.locals.user.id));
		}
	}
};
