/**
 * Entry point for communicating with the Python kernel
 */

import { modes, type mode as modeType } from '$lib/analysis/modes';
import type { Frame } from '$lib/analysis/kernel/framing';
import { browser } from '$app/environment';

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
	url.searchParams.set('frame', JSON.stringify(frame));

	const response = await fetch(url);
	const jsonResponse = (await response.json()) as unknown;
	return modes[mode].computedFileData.parse(jsonResponse);
}
