import type { PageServerLoad, Actions } from './$types';
import { setError, superValidate } from 'sveltekit-superforms';
import { formSchema } from './schema';
import { zod } from 'sveltekit-superforms/adapters';
import { createUser } from '$lib/database/users';
import { fail, redirect } from '@sveltejs/kit';
import { lucia } from '$lib/server/auth';

export const load: PageServerLoad = async ({ locals }) => {
	if (locals.user) {
		redirect(302, '/profile');
	}

	return {
		form: await superValidate(zod(formSchema))
	};
};

export const actions: Actions = {
	default: async (event) => {
		const form = await superValidate(event, zod(formSchema));
		if (!form.valid) {
			return fail(400, {
				form
			});
		}
		console.log(form.data);

		const result = await createUser(form.data);

		if (!result.success) {
			switch (result.reason) {
				case 'email-in-use':
					setError(form, 'email', 'Email is already in use');
					return fail(400, {
						form
					});
				case 'username-in-use':
					setError(form, 'username', 'Username is already in use');
					return fail(400, {
						form
					});
				case 'unread-policy':
					setError(form, 'privacyAck', 'Did not acknowledge privacy policy');
					return fail(400, {
						form
					});
			}
		}

		const { userId } = result;

		const session = await lucia.createSession(userId, {});
		const sessionCookie = lucia.createSessionCookie(session.id);
		event.cookies.set(sessionCookie.name, sessionCookie.value, {
			path: '.',
			...sessionCookie.attributes
		});

		const redirectUrl = event.cookies.get('redirect-after-login') ?? '/profile';
		redirect(302, redirectUrl);
	}
};
