import type { Mode } from '$lib/analysis/modes';
import type { AnalysisFile } from '$lib/files';

export type PaneState = {
	mode: Mode;
	files: AnalysisFile[];
};
