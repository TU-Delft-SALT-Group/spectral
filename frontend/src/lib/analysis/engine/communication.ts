/**
 * Entry point for communicating with the Python engine
 */

import { env } from '$env/dynamic/public';
import { todo, unwrap } from '$lib/utils';
import type { Mode, ModeData } from '$lib/analysis/modes';
import type { Frame } from '$lib/analysis/engine/framing'

const ORIGIN = unwrap(
	env.PUBLIC_ENGINE_ORIGIN,
	'engine origin not given (example: `https://192.168.0.5:6942`, without a trailing slash)'
);

/**
 * Main way to fetch stuff for backend
 */
export async function fetchEngine(path: string): Promise<Response> {
	// Remove leading slash
	if (path.startsWith('/')) {
		path = path.slice(1);
	}

	const url = new URL(`${ORIGIN}/${path}`);
	return fetch(url);
}

/**
 * Fetches the data for a specific mode
 */
export async function getData({
	fileId,
	mode,
	frame,
}: {
	mode: Mode;
	fileId: string;
	frame: Frame;
}): Promise<ModeData> {
	// TODO: Actually implement this
	return todo("Python bridge not implemented");
}
