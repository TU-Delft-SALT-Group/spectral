/**
 * Entry point for communicating with the Python engine
 */

import { env } from '$env/dynamic/public';
import { unwrap } from '$lib/utils';
import { modeDataValidator, type Mode, type ModeData } from '$lib/analysis/modes';
import type { Frame } from '$lib/analysis/engine/framing';
import { error } from '@sveltejs/kit';

const ORIGIN = unwrap(
	env.PUBLIC_KERNEL_ORIGIN,
	'Python kernel origin not given (example: `https://192.168.0.5:6942`, without a trailing slash)'
);

/**
 * Main way to fetch stuff for backend
 */
export function getURL(path: string): URL {
	// Remove leading slash
	if (path.startsWith('/')) {
		path = path.slice(1);
	}

	return new URL(`${ORIGIN}/${path}`);
}

/**
 * Fetches the data for a specific mode
 */
export async function getData({
	// eslint-disable-next-line
	fileId,
	// eslint-disable-next-line
	mode,
	// eslint-disable-next-line
	frame
}: {
	mode: Mode;
	fileId: string;
	frame: Frame | null;
}): Promise<ModeData> {
	const url = getURL(`analyze/${mode}/${fileId}`);

	url.searchParams.set('frame', JSON.stringify(frame));

	const response = await fetch(url);

	const result = modeDataValidator.safeParse(await response.json());

	if (!result.success) {
		const { error: zodError } = result;

		throw error(500, zodError);
	}

	const { data } = result;

	return {
		...data,
		fileId
	};
}
