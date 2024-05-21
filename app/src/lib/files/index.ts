import type { Frame } from '$lib/analysis/kernel/framing';
import { FileIcon, FolderIcon } from 'lucide-svelte';
import type { ComponentType } from 'svelte';

/**
 * A file that appears in the file browser.
 */
export type FilebrowserFile = {
	name: string;
	id: string;
	type: 'file' | 'folder';
};

export function getFileIcon(type: FilebrowserFile['type']): ComponentType {
	switch (type) {
		case 'file':
			return FileIcon;
		case 'folder':
			return FolderIcon;
	}
}

/**
 * A file that is being analyzed.
 */
// TODO: Try to find a better name for "FilebrowserFile" and "AnalysisFile"
export type AnalysisFile = {
	id: string;
	name: string;
	frame: Frame | null;
};
