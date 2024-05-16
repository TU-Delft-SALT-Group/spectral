/**
 * Entry point for communicating with the Python engine
 */

import { modeDataValidator, type Mode, type ModeData } from '$lib/analysis/modes';
import type { Frame } from '$lib/analysis/engine/framing';
import { error } from '@sveltejs/kit';
import { browser } from '$app/environment';

/**
 * Main way to fetch stuff for backend
 */
export function getURL(path: string): URL {
	if (!browser) {
		throw Error('This function is only available in the browser');
	}
	// Remove leading slash
	if (path.startsWith('/')) {
		path = path.slice(1);
	}

	return new URL(`api/${path}`, window.location.origin);
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
	const url = getURL(`signals/modes/${mode}/${fileId}`);
	url.searchParams.set('frame', JSON.stringify(frame));

	const response = await fetch(url);

	const json = await response.json();
	const result = modeDataValidator.safeParse({ ...json, mode });

	if (!result.success) {
		const { error: zodError } = result;
		console.error(zodError);
		throw error(500, zodError);
	}
	console.log(result);
	const { data } = result;

	return {
		...data,
		fileId
	};
}
