import { redirect } from '@sveltejs/kit';
import type { LayoutServerLoad } from './$types';

export const load: LayoutServerLoad = async ({ parent, url, cookies }) => {
	const { user } = await parent();

	if (user === null) {
		cookies.set('redirect-after-login', url.toString(), {
			path: '/'
		});

		redirect(302, '/login');
	}

	return {
		user
	};
};
