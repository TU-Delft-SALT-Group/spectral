/**
 * Entry point for communicating with the Python kernel
 */

import { modes, type mode as modeType } from '$lib/analysis/modes';
import type { Frame } from '$lib/analysis/kernel/framing';
import { browser } from '$app/environment';
import { error } from '@sveltejs/kit';
import { todo } from '$lib/utils';

/**
 * Gets the URL for the backend API
 */
export function getURL(path: string, base = 'api/'): URL {
	if (!browser) {
		throw Error('This function is only available in the browser');
	}
	// Remove leading slash
	if (path.startsWith('/')) {
		path = path.slice(1);
	}

	return new URL(base + path, window.location.origin);
}

/**
 * Fetches the data for a specific mode
 */
export async function getComputedFileData<M extends modeType.Name>({
	fileId,
	mode,
	frame
}: {
	mode: M;
	fileId: string;
	frame: Frame | null;
}): Promise<modeType.ComputedData<M>> {
	const url = getURL(`signals/modes/${mode}/${fileId}`);
	if (frame) {
		url.searchParams.set('startIndex', frame.startIndex.toString());
		url.searchParams.set('endIndex', frame.endIndex.toString());
	}

	const response = await fetch(url);
	console.log({ response });
	const jsonResponse = (await response.json()) as unknown;
	console.log({ jsonResponse });
	const result = modes[mode].computedFileData.safeParse(jsonResponse);

	if (!result.success) {
		console.log(jsonResponse);
		console.log(result.error);
		error(400, todo());
	}

	return result.data;
}
