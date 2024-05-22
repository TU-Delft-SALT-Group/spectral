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
