/**
 * Entry point for communicating with the Python kernel
 */

import { modes, type mode as modeType } from '$lib/analysis/modes';
import { browser } from '$app/environment';
import { error } from '@sveltejs/kit';
import { todo } from '$lib/utils';
import { logger } from '$lib/logger';

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
 * Fetches data from the kernel. It has the exact same API as fetch, but with an additional fileId parameter.
 *
 * This is needed to verify that the file being accessed is owned by the user.
 */
export async function fetchKernel(input: RequestInfo | URL, fileId: string, init?: RequestInit) {
	return fetch(input, {
		...init,
		headers: {
			...init?.headers,
			'file-id': fileId
		}
	});
}

/**
 * Fetches the data for a specific mode
 */
export async function getComputedFileData<M extends modeType.Name>({
	mode,
	fileState
}: {
	mode: M;
	fileState: modeType.FileState<M>;
}): Promise<modeType.ComputedData<M>> {
	const url = getURL(`signals/modes/${mode}`);
	// url.searchParams.set('fileState', JSON.stringify(fileState));

	const response = await fetchKernel(url, fileState.id, {
		method: 'POST',
		headers: {
			'Content-Type': 'application/json'
		},
		body: JSON.stringify({ fileState })
	});

	const jsonResponse = (await response.json()) as unknown;
	const result = modes[mode].computedFileData.safeParse(jsonResponse);

	if (!result.success) {
		logger.error(
			`Kernel response could not be parsed (response was ${JSON.stringify(jsonResponse)})`
		);
		error(500, `Kernel response couldn't be parsed (response was ${JSON.stringify(jsonResponse)})`);
	}

	return result.data;
}
