import { paneState } from '$lib/analysis/analysis-pane';
import { z } from 'zod';

export const workspaceState = z
	.object({
		panes: z.array(paneState)
	})
	.default({
		panes: [paneState.parse(undefined)]
	});

export type WorkspaceState = z.infer<typeof workspaceState>;
