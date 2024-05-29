import { modes, type mode } from '$lib/analysis/modes';
import { z } from 'zod';
import { fileState } from './modes/file-state';

// Black magic taken from https://github.com/colinhacks/zod/discussions/839#discussioncomment-4335236
function zodEnumFromObjKeys<K extends string>(obj: Record<K, unknown>): z.ZodEnum<[K, ...K[]]> {
	const [firstKey, ...otherKeys] = Object.keys(obj) as K[];
	return z.enum([firstKey, ...otherKeys]);
}

const modeState = z
	.object({
		...Object.fromEntries(Object.entries(modes).map(([mode, { modeState }]) => [mode, modeState]))
	})
	.default(
		Object.fromEntries(
			Object.entries(modes).map(([mode, { modeState }]) => {
				return [mode, modeState.parse(undefined)];
			})
		)
	);

// Type casting because typescript doesn't understand the type
const parseModeState = (state: unknown) =>
	modeState.parse(state) as { [M in mode.Name]: mode.ModeState<M> };

export const paneState = z
	.object({
		id: z.string().default('broken-pane-id'),
		title: z.string().default('default'),
		mode: zodEnumFromObjKeys(modes).default('waveform'),
		// Using type casted transform to have correct inferred type
		modeState: z.unknown().transform(parseModeState),
		files: z.array(fileState)
	})
	.default({
		mode: 'waveform',
		modeState: parseModeState(undefined),
		files: []
	});

export type PaneState = z.infer<typeof paneState>;
