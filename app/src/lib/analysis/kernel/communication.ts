/**
 * Entry point for communicating with the Python kernel
 */

import { modes, type mode as modeType } from '$lib/analysis/modes';
import { browser } from '$app/environment';
import { error } from '@sveltejs/kit';
import { todo } from '$lib/utils';

/**
 * Gets the URL for the backend API
 */
export function getURL(path: string, base = 'api/'): URL {
	if (!browser) {
		todo('Make getURL work on the server');
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
	fileState
}: {
	mode: M;
	fileId: string;
	fileState: modeType.FileState<M>;
}): Promise<modeType.ComputedData<M>> {
	const url = getURL(`signals/modes/${mode}/${fileId}`);
	url.searchParams.set('fileState', JSON.stringify(fileState));

	const response = await fetch(url);
	const jsonResponse = (await response.json()) as unknown;
	const result = modes[mode].computedFileData.safeParse(jsonResponse);

	if (!result.success) {
		error(500, `Kernel response couldn't be parsed (response was ${JSON.stringify(jsonResponse)})`);
	}

	return result.data;
}
