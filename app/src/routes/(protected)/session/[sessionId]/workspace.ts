import { paneState } from '$lib/analysis/analysis-pane';
import { z } from 'zod';

export const sessionState = z
	.object({
		panes: z.record(z.string(), paneState)
	})
	.default({
		panes: { 'broken-pane-id': paneState.parse(undefined) }
	});

export type SessionState = z.infer<typeof sessionState>;
