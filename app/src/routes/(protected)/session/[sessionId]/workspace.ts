import { paneState } from '$lib/analysis/analysis-pane';
import { z } from 'zod';

export const sessionState = z
	.object({
		panes: z.array(paneState)
	})
	.default({
		panes: [paneState.parse(undefined)]
	});

export type SessionState = z.infer<typeof sessionState>;
