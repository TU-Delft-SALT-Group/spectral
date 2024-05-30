<script lang="ts">
	import { Button } from '$lib/components/ui/button';
	import * as ContextMenu from '$lib/components/ui/context-menu';
	import FileIcon from 'lucide-svelte/icons/file';
	import type { FileState } from '$lib/analysis/modes/file-state';

	export let file: FileState;
	export let onDeleteFile: (fileId: string) => void = () => {};

	// Manual fetch because it's a hassle to set up the form
	async function deleteFile(fileId: string) {
		onDeleteFile(fileId);
		await fetch('?/deleteFile', { method: 'POST', body: JSON.stringify({ fileId }) });
	}
</script>

<ContextMenu.Root>
	<ContextMenu.Trigger>
		<Button class="flex-2 w-full justify-start gap-2 rounded" variant="ghost">
			<FileIcon class="h-6 w-6"></FileIcon>
			<span class="overflow-hidden text-ellipsis">
				{file.name}
			</span>
		</Button>
	</ContextMenu.Trigger>

	<ContextMenu.Content>
		<ContextMenu.Item on:click={() => deleteFile(file.id)}>
			<span> Delete </span>
		</ContextMenu.Item>
	</ContextMenu.Content>
</ContextMenu.Root>
